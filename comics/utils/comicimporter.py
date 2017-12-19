from datetime import datetime
from json.decoder import JSONDecodeError
import logging
import os
import re
from urllib.parse import unquote_plus
from urllib.request import urlretrieve

from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.text import slugify
import requests
import requests_cache

from comics.models import (Arc, Character, Creator, Issue,
                           Publisher, Roles, Series, Team, Settings)

from . import utils
from .comicapi.comicarchive import MetaDataStyle, ComicArchive
from .comicapi.issuestring import IssueString


IMG_NORMAL_SIZE = "320x487"
IMG_SMALL_SIZE = "200x305"


def get_recursive_filelist(pathlist):
    # Get a recursive list of all files under all path items in the list.
    filelist = []
    if os.path.isdir(pathlist):
        for root, dirs, files in os.walk(pathlist):
            for f in files:
                filelist.append(os.path.join(root, f))
    return filelist


class ComicImporter(object):

    def __init__(self):
        # Configure logging
        logging.getLogger("requests").setLevel(logging.WARNING)
        self.logger = logging.getLogger('bamf')
        # Setup requests caching
        requests_cache.install_cache('./media/CACHE/comicvine-cache',
                                     backend="sqlite",
                                     expire_after=1800)
        requests_cache.core.remove_expired_responses()
        # temporary values until settings view is created.
        self.api_key = Settings.get_solo().api_key
        self.directory_path = Settings.get_solo().comics_directory
        # API Strings
        self.baseurl = 'https://comicvine.gamespot.com/api/'
        self.imageurl = 'https://comicvine.gamespot.com/api/image/'
        self.base_params = {'format': 'json',
                            'api_key': self.api_key}
        self.headers = {'user-agent': 'bamf'}
        # API field strings
        self.arc_fields = 'deck,description,id,image,name,site_detail_url'
        self.character_fields = 'deck,description,id,image,name,site_detail_url'
        self.creator_fields = 'deck,description,id,image,name,site_detail_url'
        self.publisher_fields = 'deck,description,id,image,name,site_detail_url'
        self.series_fields = 'api_detail_url,deck,description,id,name,publisher,site_detail_url,start_year'
        self.issue_fields = 'api_detail_url,character_credits,cover_date,deck,description,id,image,issue_number,name,person_credits,site_detail_url,story_arc_credits,team_credits,volume'
        self.team_fields = 'characters,deck,description,id,image,name,site_detail_url'
        # Initial Comic Book info to search
        self.style = MetaDataStyle.CIX

    def checkIfRemovedOrModified(self, comic, pathlist):
        remove = False

        def inFolderlist(filepath, pathlist):
            for p in pathlist:
                if p in filepath:
                    return True
            return False

        if not (os.path.exists(comic.file)):
            self.logger.info("Removing missing {0}".format(comic.file))
            remove = True
        elif not inFolderlist(comic.file, pathlist):
            self.logger.info("Removing unwanted {0}".format(comic.file))
            remove = True
        else:
            current_timezone = timezone.get_current_timezone()
            c = datetime.utcfromtimestamp(os.path.getmtime(comic.file))
            curr = timezone.make_aware(c, current_timezone)
            prev = comic.mod_ts

            if curr != prev:
                self.logger.info("Removing modified {0}".format(comic.file))
                remove = True

        if remove:
            comic.delete()

    def get_cv_object_data(self, response):
        '''
        Gathers object data from a response and tests each value to make sure
        it exists in the response before trying to set it.

        CVID and CVURL will always exist in a ComicVine response, so there
        is no need to verify this data.

        Returns a dictionary with all the gathered data.
        '''

        # Get Name
        name = ''
        if 'name' in response:
            if response['name']:
                name = response['name']

        # Get Start Year (only exists for Series objects)
        year = ''

        if 'start_year' in response:
            if response['start_year']:
                year = response['start_year']

        # Get Number (only exists for Issue objects)
        number = ''

        if 'issue_number' in response:
            if response['issue_number']:
                number = response['issue_number']

        # Get Description (Favor short description if available)
        desc = ''

        if 'deck' in response:
            if response['deck']:
                desc = response['deck']
            if desc == '':
                if 'description' in response:
                    if response['description']:
                        desc = strip_tags(response['description'])

        # Get Image
        image = ''

        if 'image' in response:
            if response['image']:
                image_url = self.imageurl + \
                    response['image']['super_url'].rsplit('/', 1)[-1]
                image_filename = unquote_plus(image_url.split('/')[-1])
                if image_filename != '1-male-good-large.jpg' and not re.match(".*question_mark_large.*.jpg", image_filename):
                    image = utils.test_image(urlretrieve(
                        image_url, 'media/images/' + image_filename)[0])

        # Create data object
        data = {
            'cvid': response['id'],
            'cvurl': response['site_detail_url'],
            'name': name,
            'year': year,
            'number': number,
            'desc': desc,
            'image': image,
        }

        return data

    def getCVIssue(self, issue_cvid):
        issue_params = self.base_params
        issue_params['field_list'] = self.issue_fields

        try:
            response = requests.get(
                self.baseurl + 'issue/4000-' + str(issue_cvid),
                params=issue_params,
                headers=self.headers,
            ).json()
        except JSONDecodeError:
            response = None
            self.logger.info('No value returned from getCVIssue().')

        return response

    def getIssueCV(self, issue_cvid, response_issue):
        issue_params = self.base_params
        issue_params['field_list'] = self.issue_fields

        api_url = response_issue['results']['api_detail_url']

        response = requests.get(
            api_url,
            params=issue_params,
            headers=self.headers,
        ).json()

        data = self.get_cv_object_data(response['results'])

        issue = Issue.objects.get(cvid=issue_cvid)
        issue.thumb = utils.resize_images(data['image'],
                                          IMG_SMALL_SIZE)
        issue.cover = utils.resize_images(data['image'],
                                          IMG_NORMAL_SIZE)
        issue.desc = data['desc']
        issue.save()
        os.remove(data['image'])

    def getSeriesCV(self, api_url):
        params = self.base_params
        params['field_list'] = self.series_fields

        response = requests.get(
            api_url,
            params=params,
            headers=self.headers,
        ).json()

        data = self.get_cv_object_data(response['results'])

        return data

    def getPubisherCV(self, response_issue):
        series_params = self.base_params
        series_params['field_list'] = 'publisher'

        response_series = requests.get(
            response_issue['results']['volume']['api_detail_url'],
            params=series_params,
            headers=self.headers,
        ).json()

        params = self.base_params
        params['field_list'] = self.publisher_fields

        api_url = response_series['results']['publisher']['api_detail_url']

        response = requests.get(
            api_url,
            params=params,
            headers=self.headers,
        ).json()

        data = self.get_cv_object_data(response['results'])

        return data

    def getCVData(self, db_obj, fields, api_url):
        params = self.base_params
        params['field_list'] = fields

        try:
            response = requests.get(
                api_url,
                params=params,
                headers=self.headers,
            ).json()
        except JSONDecodeError:
            return False

        data = self.get_cv_object_data(response['results'])

        # Year (only exists for Series objects)
        if data['year'] is not None:
            db_obj.year = data['year']
        db_obj.cvurl = data['cvurl']
        db_obj.desc = data['desc']
        db_obj.image = data['image']
        db_obj.save()

        return True

    def getTeamCharactersCV(self, api_url):
        params = self.base_params
        params['field_list'] = self.team_fields

        try:
            response = requests.get(
                api_url,
                params=params,
                headers=self.headers,
            ).json()
        except ValueError:
            response = None

        return response

    def getCreatorCV(self, api_url):
        params = self.base_params
        params['field_list'] = self.creator_fields

        response = requests.get(
            api_url,
            params=params,
            headers=self.headers,
        ).json()

        data = self.get_cv_object_data(response['results'])

        return data

    def getTeamCV(self, api_url):
        params = self.base_params
        params['field_list'] = self.team_fields

        response = requests.get(
            api_url,
            params=params,
            headers=self.headers,
        ).json()

        data = self.get_cv_object_data(response['results'])

        return data

    def getIssueCVID(self, md):
        # Get the issues cvid
        # TODO: Need to clean this up a bit, but for now it works.
        cvID = None
        if md.notes is not None:
            cvID = re.search('\d+]', md.notes)
            if cvID is not None:
                cvID = str(cvID.group(0))
                cvID = cvID[:-1]
                return cvID

        if md.webLink is not None:
            cvID = re.search('/\d+-\d+/', md.webLink)
            if cvID is not None:
                cvID = str(cvID.group(0))
                cvID = cvID.split('-')
                cvID = cvID[1]
                cvID = cvID[:-1]
                return cvID

        return cvID

    def getComicMetadata(self, path):
        # TODO: Need to fix the default image path
        ca = ComicArchive(path, default_image_path=None)
        if ca.seemsToBeAComicArchive():
            self.logger.info(
                "Reading in {0} {1}".format(self.read_count, path))
            self.read_count += 1
            if ca.hasMetadata(MetaDataStyle.CIX):
                style = MetaDataStyle.CIX
            elif ca.hasMetadata(MetaDataStyle.CBI):
                style = MetaDataStyle.CBI
            else:
                style = None

            if style is not None:
                md = ca.readMetadata(style)
            else:
                # No metadata in comic. Make some guesses from filename.
                md = ca.metadataFromFilename()

            md.path = ca.path
            md.page_count = ca.page_count
            md.mod_ts = datetime.utcfromtimestamp(os.path.getmtime(ca.path))

            return md
        return None

    def addComicFromMetadata(self, md):
        if not md.isEmpty:
            # Let's get the issue Comic Vine id from the archive's metadata
            # If it's not there we'll skipp the issue.
            cvID = self.getIssueCVID(md)
            if cvID is None:
                issue_name = md.series + ' #' + md.number
                self.logger.info(
                    'No Comic Vine ID for: %s... skipping.' % issue_name)
                return False

            # let's get the issue info from CV.
            issue_response = self.getCVIssue(cvID)
            if issue_response is None:
                return False

            # Add the Publisher to the database.
            if md.publisher is not None:
                publisher_obj, p_create = Publisher.objects.get_or_create(
                    name=md.publisher,
                    slug=slugify(md.publisher),)

            # Get the series info from CV.
            series_url = issue_response['results']['volume']['api_detail_url']
            data = self.getSeriesCV(series_url)

            if (data['year']) is not None:
                slugy = (data['name'] + ' ' + data['year'])
            else:
                slugy = data['name']
            # Create the series sort name to deal with titles with 'The' in it.
            sort_name = utils.create_series_sortname(data['name'])

            # Alright let's create the series object.
            series_obj, s_create = Series.objects.get_or_create(
                cvid=int(data['cvid']),
                cvurl=data['cvurl'],
                name=data['name'],
                sort_title=sort_name,
                publisher=publisher_obj,
                year=data['year'],
                desc=data['desc'],)

            if s_create:
                if (data['year']) is not None:
                    exist_count = Series.objects.filter(
                        name__iexact=data['name'], year=data['year']).count()
                else:
                    exist_count = Series.objects.filter(
                        name__iexact=data['name']).count()
                if exist_count > 1:
                    # Ok, let's drop the count by one since we're including the
                    # new series in the count.
                    exist_count = exist_count - 1
                    slugy = slugy + ' ' + str(exist_count)

                series_obj.slug = slugify(slugy)
                series_obj.save()
                self.logger.info('Added series: %s' % series_obj)

            # Ugh, deal wih the timezone
            current_timezone = timezone.get_current_timezone()
            tz = timezone.make_aware(md.mod_ts, current_timezone)

            pub_date = None
            if md.year is not None:
                try:
                    day = 1
                    month = 1
                    if md.month is not None:
                        month = int(md.month)
                    if md.day is not None:
                        day = int(md.day)
                    year = int(md.year)
                    pub_date = datetime(year, month, day)
                except:
                    pass

            fixed_number = IssueString(md.issue).asString(pad=3)

            if pub_date is not None:
                slugy = series_obj.name + ' ' + \
                    fixed_number + ' ' + str(pub_date.year)
            else:
                slugy = series_obj.name + ' ' + fixed_number

            # Create the issue
            issue_obj, i_create = Issue.objects.get_or_create(
                file=md.path,
                name=str(md.title),
                slug=slugify(slugy),
                number=fixed_number,
                desc=str(md.comments),
                date=pub_date,
                page_count=md.page_count,
                cvurl=md.webLink,
                cvid=int(cvID),
                mod_ts=tz,
                series=series_obj,)

            # Get the issue image & short description from CV.
            self.getIssueCV(cvID, issue_response)
            self.logger.info("Added: %s" % issue_obj)

            # Adding new publisher we need to grab
            # some additional data from Comic Vine.
            if p_create:
                p = self.getPubisherCV(issue_response)
                publisher_obj.logo = utils.resize_images(p['image'],
                                                         IMG_NORMAL_SIZE)
                publisher_obj.cvid = int(p['cvid'])
                publisher_obj.cvurl = p['cvurl']
                publisher_obj.desc = p['desc']
                publisher_obj.save()
                # Delete the original image
                os.remove(p['image'])

                self.logger.info('Added publisher: %s' % publisher_obj)

            # Add the characters.
            for ch in issue_response['results']['character_credits']:
                character_obj, ch_create = Character.objects.get_or_create(
                    cvid=ch['id'],)
                issue_obj.characters.add(character_obj)

                if ch_create:
                    # Check to see if the slug or name exists already in the
                    # db.
                    test_slug = slugify(ch['name'])

                    slug_count = Character.objects.filter(
                        slug__iexact=test_slug).count()
                    name_count = Character.objects.filter(
                        name__iexact=ch['name']).count()

                    if (slug_count > 0 or name_count > 1):
                        max_count = max(slug_count, name_count)
                        slugy = ch['name'] + ' ' + str(max_count)
                    else:
                        slugy = ch['name']

                    character_obj.name = ch['name']
                    character_obj.slug = slugify(slugy)
                    character_obj.save()
                    # Alright get the detail information now.
                    res = self.getCVData(character_obj,
                                         self.character_fields,
                                         ch['api_detail_url'])

                    if character_obj.image:
                        old_image_path = character_obj.image
                        character_obj.thumb = utils.resize_images(character_obj.image,
                                                                  IMG_SMALL_SIZE)
                        character_obj.image = utils.resize_images(character_obj.image,
                                                                  IMG_NORMAL_SIZE)
                        character_obj.save()
                        os.remove(old_image_path)

                    if res:
                        self.logger.info('Added character: %s' % character_obj)
                    else:
                        self.logger.info('No Character detail info available for: %s'
                                         % character_obj)

            # Add the storyarc.
            for story_arc in issue_response['results']['story_arc_credits']:
                story_obj, s_create = Arc.objects.get_or_create(
                    cvid=story_arc['id'],)
                issue_obj.arcs.add(story_obj)

                if s_create:
                    test_slug = slugify(story_arc['name'])
                    slug_count = Arc.objects.filter(
                        slug__iexact=test_slug).count()
                    if slug_count > 0:
                        slugy = story_arc['name'] + ' ' + str(slug_count)
                    else:
                        slugy = story_arc['name']

                    story_obj.name = story_arc['name']
                    story_obj.slug = slugify(slugy)
                    story_obj.save()

                    res = self.getCVData(story_obj,
                                         self.arc_fields,
                                         story_arc['api_detail_url'])

                    if story_obj.image:
                        old_image_path = story_obj.image
                        story_obj.image = utils.resize_images(story_obj.image,
                                                              IMG_NORMAL_SIZE)
                        story_obj.save()
                        os.remove(old_image_path)

                    if res:
                        self.logger.info('Added storyarc: %s' % story_obj)
                    else:
                        self.logger.info('Not Story Arc detail info available for: %s'
                                         % story_obj)

            # Add the teams
            for team in issue_response['results']['team_credits']:
                team_obj, t_create = Team.objects.get_or_create(
                    cvid=team['id'],)
                issue_obj.teams.add(team_obj)

                # Add any existing character to the team.
                c_response = self.getTeamCharactersCV(team['api_detail_url'])
                if c_response is not None:
                    for character in c_response['results']['characters']:
                        match = Character.objects.filter(cvid=character['id'])
                        if match:
                            match[0].teams.add(team_obj)

                if t_create:
                    test_slug = slugify(team['name'])
                    slug_count = Team.objects.filter(
                        slug__iexact=test_slug).count()
                    if slug_count > 0:
                        slugy = team['name'] + ' ' + str(slug_count)
                    else:
                        slugy = team['name']

                    team_obj.name = team['name']
                    team_obj.slug = slugify(slugy)
                    team_obj.save()

                    res = self.getCVData(team_obj,
                                         self.team_fields,
                                         team['api_detail_url'])

                    if team_obj.image:
                        old_image_path = team_obj.image
                        team_obj.thumb = utils.resize_images(team_obj.image,
                                                             IMG_SMALL_SIZE)
                        team_obj.image = utils.resize_images(team_obj.image,
                                                             IMG_NORMAL_SIZE)
                        team_obj.save()
                        os.remove(old_image_path)

                    if res:
                        self.logger.info('Added team: %s' % team_obj)
                    else:
                        self.logger.info('No Team detail info available for: %s'
                                         % team_obj)

            # Add the creators
            for p in issue_response['results']['person_credits']:
                creator_obj, c_create = Creator.objects.get_or_create(
                    cvid=p['id'],)

                Roles.objects.create(creator=creator_obj,
                                     issue=issue_obj,
                                     roles=re.sub(' ', '', p['role']))

                if c_create:
                    test_slug = slugify(p['name'])
                    slug_count = Creator.objects.filter(
                        slug__iexact=test_slug).count()
                    if slug_count > 0:
                        slugy = p['name'] + ' ' + str(slug_count)
                    else:
                        slugy = p['name']

                    creator_obj.name = p['name']
                    creator_obj.slug = slugify(slugy)
                    creator_obj.save()

                    res = self.getCVData(creator_obj,
                                         self.creator_fields,
                                         p['api_detail_url'])

                    if creator_obj.image:
                        old_image_path = creator_obj.image
                        creator_obj.thumb = utils.resize_images(creator_obj.image,
                                                                IMG_SMALL_SIZE)
                        creator_obj.image = utils.resize_images(creator_obj.image,
                                                                IMG_NORMAL_SIZE)
                        creator_obj.save()
                        os.remove(old_image_path)

                    if res:
                        self.logger.info('Added creator: %s' % creator_obj)
                    else:
                        self.logger.info('No Creator detail info available for: %s'
                                         % creator_obj)

            return True

    def commitMetadataList(self, md_list):
        for md in md_list:
            self.addComicFromMetadata(md)

    def import_comic_files(self):
        filelist = get_recursive_filelist(self.directory_path)
        filelist = sorted(filelist, key=os.path.getmtime)

        # Grab the entire issue table into memory
        comics_list = Issue.objects.all()

        # Remove from the database any missing or changed files
        for comic in comics_list:
            self.checkIfRemovedOrModified(comic, self.directory_path)

        comics_list = None

        # Load the issue table again to take into account any
        # issues remove from the database
        c_list = Issue.objects.all()

        # Make a list of all path string in issue table
        db_pathlist = []
        for comic in c_list:
            db_pathlist.append(comic.file)

        c_list = None

        # Now let's remove any existing files in the database
        # from the directory list of files.
        for f in db_pathlist:
            if f in filelist:
                filelist.remove(f)
        db_pathlist = None

        md_list = []
        self.read_count = 0
        for filename in filelist:
            md = self.getComicMetadata(filename)
            if md is not None:
                md_list.append(md)

            if self.read_count % 100 == 0 and self.read_count != 0:
                if len(md_list) > 0:
                    self.commitMetadataList(md_list)
                    md_list = []

        if len(md_list) > 0:
            self.commitMetadataList(md_list)

        self.logger.info('Finished importing..')
