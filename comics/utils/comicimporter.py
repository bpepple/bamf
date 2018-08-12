from datetime import datetime, timedelta
import itertools
import json
import logging
import os
import re
from urllib.parse import unquote_plus
from urllib.request import urlretrieve

from django.conf import settings
from django.db import IntegrityError
from django.utils import timezone
from django.utils.text import slugify
import requests
import requests_cache

from comics.models import (Arc, Character, Creator, Issue,
                           Publisher, Role, Roles, Series,
                           Team, Settings)

from . import utils
from .comicapi.comicarchive import MetaDataStyle, ComicArchive
from .comicapi.issuestring import IssueString


ARCS_FOLDER = 'arcs'
CHARACTERS_FOLDERS = 'characters'
CREATORS_FOLDERS = 'creators'
ISSUES_FOLDER = 'issues'
PUBLISHERS_FOLDER = 'publishers'
TEAMS_FOLDERS = 'teams'


def get_recursive_filelist(pathlist):
    # Get a recursive list of all files under all path items in the list.
    filelist = []
    if os.path.isdir(pathlist):
        for root, dirs, files in os.walk(pathlist):
            for f in files:
                filelist.append(os.path.join(root, f))
    return filelist


class CVTypeID:
    Character = '4005'
    Issue = '4000'
    Person = '4040'
    Publisher = '4010'
    StoryArc = '4045'
    Team = '4060'
    Volume = '4050'


class ComicImporter(object):

    def __init__(self):
        # Configure logging
        logging.getLogger("requests").setLevel(logging.WARNING)
        self.logger = logging.getLogger('bamf')
        # Setup requests caching
        expire_after = timedelta(hours=1)
        requests_cache.install_cache('cv-cache',
                                     backend='redis',
                                     expire_after=expire_after)
        requests_cache.core.remove_expired_responses()
        # temporary values until settings view is created.
        self.api_key = Settings.get_solo().api_key
        self.directory_path = Settings.get_solo().comics_directory
        # API Strings
        self.baseurl = 'https://comicvine.gamespot.com/api'
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
        self.refresh_issue_fields = 'api_detail_url,cover_date,deck,description,id,issue_number,name,site_detail_url,volume'
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
            series = Series.objects.get(id=comic.series.id)
            s_count = series.issue_count
            # If this is the only issue for a series, delete the series.
            if s_count == 1:
                series.delete()
                self.logger.info('Deleting series: %s' % series)
            else:
                comic.delete()

    def getCVObjectData(self, response):
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
                # Check to see if the deck is a space (' ').
                if response['deck'] != ' ':
                    desc = response['deck']
            if desc == '':
                if 'description' in response:
                    if response['description']:
                        desc = response['description']

        # Get Image
        image = ''
        if 'image' in response:
            if response['image']:
                image_url = self.imageurl + \
                    response['image']['super_url'].rsplit('/', 1)[-1]
                image_filename = unquote_plus(image_url.split('/')[-1])
                if image_filename != '1-male-good-large.jpg' and not re.match(".*question_mark_large.*.jpg", image_filename):
                    try:
                        image = utils.test_image(urlretrieve(
                            image_url, 'media/images/' + image_filename)[0])
                    except OSError as e:
                        self.logger.error('%s' % e)
                        image = None

        # Create data object
        data = {
            'cvid': response['id'],
            'cvurl': response['site_detail_url'],
            'name': name,
            'year': year,
            'number': number,
            'desc': utils.cleanup_html(desc, True),
            'image': image,
        }

        return data

    def refreshCharacterData(self, cvid):
        issue_params = self.base_params
        issue_params['field_list'] = self.character_fields

        try:
            resp = requests.get(
                self.baseurl + '/character/' +
                CVTypeID.Character + '-' + str(cvid),
                params=issue_params,
                headers=self.headers,
            ).json()
        except requests.exceptions.RequestException as e:
            self.logger.error('%s' % e)
            return False

        data = self.getCVObjectData(resp['results'])

        # Currently I'm not refreshing the image until the
        # cropping code is refactored, so let's remove the image.
        os.remove(data['image'])

        character = Character.objects.get(cvid=cvid)
        character.desc = data['desc']
        character.save()
        self.logger.info('Refreshed metadata for: %s' % character)

        return True

    def refreshCreatorData(self, cvid):
        issue_params = self.base_params
        issue_params['field_list'] = self.creator_fields

        try:
            resp = requests.get(
                self.baseurl + '/person/' + CVTypeID.Person + '-' + str(cvid),
                params=issue_params,
                headers=self.headers,
            ).json()
        except requests.exceptions.RequestException as e:
            self.logger.error('%s' % e)
            return False

        data = self.getCVObjectData(resp['results'])

        # Currently I'm not refreshing the image until the
        # cropping code is refactored, so let's remove the image.
        os.remove(data['image'])

        creator = Creator.objects.get(cvid=cvid)
        creator.desc = data['desc']
        creator.save()
        self.logger.info('Refresh metadata for: %s' % creator)

        return True

    def refreshIssueData(self, cvid):
        issue_params = self.base_params
        issue_params['field_list'] = self.refresh_issue_fields

        try:
            resp = requests.get(
                self.baseurl + '/issue/' + CVTypeID.Issue + '-' + str(cvid),
                params=issue_params,
                headers=self.headers,
            ).json()
        except requests.exceptions.RequestException as e:
            self.logger.error('%s' % e)
            return False

        data = self.getCVObjectData(resp['results'])

        issue = Issue.objects.get(cvid=cvid)
        issue.desc = data['desc']
        issue.name = data['name']
        issue.save()
        self.logger.info('Refreshed metadata for: %s' % issue)

        return True

    def refreshSeriesData(self, cvid):
        issue_params = self.base_params
        issue_params['field_list'] = self.series_fields

        try:
            resp = requests.get(
                self.baseurl + '/volume/' + CVTypeID.Volume + '-' + str(cvid),
                params=issue_params,
                headers=self.headers,
            ).json()
        except requests.exceptions.RequestException as e:
            self.logger.error('%s' % e)
            return False

        data = self.getCVObjectData(resp['results'])

        series = Series.objects.get(cvid=cvid)
        series.desc = data['desc']
        series.year = data['year']
        series.save()
        self.logger.info('Refreshed metadata for: %s' % series)

        return True

    def refreshPublisherData(self, cvid):
        issue_params = self.base_params
        issue_params['field_list'] = self.publisher_fields

        try:
            resp = requests.get(
                self.baseurl + '/publisher/' +
                CVTypeID.Publisher + '-' + str(cvid),
                params=issue_params,
                headers=self.headers,
            ).json()
        except requests.exceptions.RequestException as e:
            self.logger.error('%s' % e)
            return False

        data = self.getCVObjectData(resp['results'])

        # Currently I'm not refreshing the image until the
        # cropping code is refactored, so let's remove the image.
        os.remove(data['image'])

        publisher = Publisher.objects.get(cvid=cvid)
        publisher.desc = data['desc']
        publisher.save()
        self.logger.info('Refresh metadata for: %s' % publisher)

        return True

    def refreshTeamData(self, cvid):
        issue_params = self.base_params
        issue_params['field_list'] = self.team_fields

        try:
            resp = requests.get(
                self.baseurl + '/team/' + CVTypeID.Team + '-' + str(cvid),
                params=issue_params,
                headers=self.headers,
            ).json()
        except requests.exceptions.RequestException as e:
            self.logger.error('%s' % e)
            return False

        data = self.getCVObjectData(resp['results'])

        # Currently I'm not refreshing the image until the
        # cropping code is refactored, so let's remove the image.
        os.remove(data['image'])

        team = Team.objects.get(cvid=cvid)
        team.desc = data['desc']
        team.save()
        self.logger.info('Refreshed metadata for: %s' % team)

        return True

    def refreshArcData(self, cvid):
        issue_params = self.base_params
        issue_params['field_list'] = self.arc_fields

        try:
            resp = requests.get(
                self.baseurl + '/story_arc/' +
                CVTypeID.StoryArc + '-' + str(cvid),
                params=issue_params,
                headers=self.headers,
            ).json()
        except requests.exceptions.RequestException as e:
            self.logger.error('%s' % e)
            return False

        data = self.getCVObjectData(resp['results'])

        # Currently I'm not refreshing the image until the
        # cropping code is refactored, so let's remove the image.
        os.remove(data['image'])

        arc = Arc.objects.get(cvid=cvid)
        arc.desc = data['desc']
        arc.save()
        self.logger.info('Refreshed metadata for: %s' % arc)

        return True

    def getIssue(self, issue_cvid):
        issue_params = self.base_params
        issue_params['field_list'] = self.issue_fields

        try:
            response = requests.get(
                self.baseurl + '/issue/' +
                CVTypeID.Issue + '-' + str(issue_cvid),
                params=issue_params,
                headers=self.headers,
            ).json()
        except (requests.exceptions.RequestException, json.decoder.JSONDecodeError) as e:
            self.logger.error('%s' % e)
            response = None

        return response

    def setIssueDetail(self, issue_cvid, issue_response):

        data = self.getCVObjectData(issue_response['results'])

        issue = Issue.objects.get(cvid=issue_cvid)
        if data['image'] != None:
            issue.cover = utils.resize_images(data['image'], ISSUES_FOLDER)
            os.remove(data['image'])
        issue.desc = data['desc']
        issue.save()

        return True

    def getSeries(self, api_url):
        params = self.base_params
        params['field_list'] = self.series_fields

        try:
            response = requests.get(
                api_url,
                params=params,
                headers=self.headers,
            ).json()
        except requests.exceptions.RequestException as e:
            self.logger.error('s' % e)
            return None

        data = self.getCVObjectData(response['results'])

        return data

    def getPublisher(self, response_issue):
        series_params = self.base_params
        series_params['field_list'] = 'publisher'

        try:
            response_series = requests.get(
                response_issue['results']['volume']['api_detail_url'],
                params=series_params,
                headers=self.headers,
            ).json()
        except requests.exceptions.RequestException as e:
            self.logger.error('%s' % e)
            return None

        params = self.base_params
        params['field_list'] = self.publisher_fields

        api_url = response_series['results']['publisher']['api_detail_url']

        try:
            response = requests.get(
                api_url,
                params=params,
                headers=self.headers,
            ).json()
        except requests.exceptions.RequestException as e:
            self.logger.error('%s', e)
            return None

        data = self.getCVObjectData(response['results'])

        return data

    def getDetailInfo(self, db_obj, fields, api_url):
        params = self.base_params
        params['field_list'] = fields

        try:
            response = requests.get(
                api_url,
                params=params,
                headers=self.headers,
            ).json()
        except (requests.exceptions.RequestException, json.decoder.JSONDecodeError) as e:
            self.logger.error('%s' % e)
            return False

        data = self.getCVObjectData(response['results'])

        # Year (only exists for Series objects)
        if data['year'] is not None:
            db_obj.year = data['year']
        db_obj.cvurl = data['cvurl']
        db_obj.desc = data['desc']
        # If the image name from Comic Vine is too large, don't save it since it will
        # cause a DB error. Using 132 as the value since that will take into account the
        # upload_to value from the longest models (Characters & Pubishers).
        if (len(data['image']) < 132):
            db_obj.image = data['image']
        db_obj.save()

        return True

    def getTeamCharacters(self, api_url):
        params = self.base_params
        params['field_list'] = self.team_fields

        try:
            response = requests.get(
                api_url,
                params=params,
                headers=self.headers,
            ).json()
        except (requests.exceptions.RequestException, json.decoder.JSONDecodeError) as e:
            self.logger.error('%s' % e)
            response = None

        return response

    def create_images(self, db_obj, img_dir):
        base_name = os.path.basename(db_obj.image.name)
        old_image_path = settings.MEDIA_ROOT + '/images/' + base_name
        db_obj.image = utils.resize_images(db_obj.image, img_dir)
        db_obj.save()
        os.remove(old_image_path)

    def getIssueCVID(self, md):
        # Get the issues cvid
        # TODO: Need to clean this up a bit, but for now it works.
        cvID = None
        if md.notes is not None:
            cvID = re.search(r'\d+]', md.notes)
            if cvID is not None:
                cvID = str(cvID.group(0))
                cvID = cvID[:-1]
                return cvID

        if md.webLink is not None:
            cvID = re.search(r'/\d+-\d+/', md.webLink)
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
            # If it's not there we'll skip the issue.
            cvID = self.getIssueCVID(md)
            if cvID is None:
                issue_name = md.series + ' #' + md.number
                self.logger.info(
                    'No Comic Vine ID for: %s... skipping.' % issue_name)
                return False

            # let's get the issue info from CV.
            issue_response = self.getIssue(cvID)
            if issue_response is None:
                return False

            # Add the Publisher to the database.
            if md.publisher is not None:
                publisher_obj, p_create = Publisher.objects.get_or_create(
                    name=md.publisher,
                    slug=slugify(md.publisher),)

            # Check the series cvid to see if we've already added
            # the series. If not, call the detail api for it.
            series_cvid = issue_response['results']['volume']['id']
            if series_cvid is not None:
                series_obj, s_create = Series.objects.get_or_create(
                    cvid=int(series_cvid),)
                if s_create:
                    series_url = issue_response['results'][
                        'volume']['api_detail_url']
                    data = self.getSeries(series_url)
                    if data is not None:
                        # Create the slug & make sure it's not a duplicate
                        new_slug = orig = slugify(data['name'])
                        for x in itertools.count(1):
                            if not Series.objects.filter(slug=new_slug).exists():
                                break
                            new_slug = '%s-%d' % (orig, x)

                        sort_name = utils.create_series_sortname(data['name'])
                        series_obj.slug = new_slug
                        series_obj.cvurl = data['cvurl']
                        series_obj.name = data['name']
                        series_obj.sort_title = sort_name
                        series_obj.publisher = publisher_obj
                        series_obj.year = data['year']
                        series_obj.desc = data['desc']
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

            new_slug = orig = slugify(slugy)

            for x in itertools.count(1):
                if not Issue.objects.filter(slug=new_slug).exists():
                    break
                new_slug = '%s-%d' % (orig, x)

            try:
                # Create the issue
                issue_obj = Issue.objects.create(
                    file=md.path,
                    name=str(md.title),
                    slug=new_slug,
                    number=fixed_number,
                    date=pub_date,
                    page_count=md.page_count,
                    cvurl=md.webLink,
                    cvid=int(cvID),
                    mod_ts=tz,
                    series=series_obj,)
            except IntegrityError as e:
                self.logger.error('%s' % e)
                self.logger.info('Skipping: %s' % md.path)
                return

            # Set the issue image & short description.
            res = self.setIssueDetail(cvID, issue_response)
            if res:
                self.logger.info("Added: %s" % issue_obj)
            else:
                self.logger.warning(
                    'No detail information was saved for %s' % issue_obj)

            # Adding new publisher we need to grab
            # some additional data from Comic Vine.
            if p_create:
                p = self.getPublisher(issue_response)
                if p is not None:
                    publisher_obj.cvid = int(p['cvid'])
                    publisher_obj.cvurl = p['cvurl']
                    publisher_obj.desc = p['desc']
                    publisher_obj.save()
                    if p['image'] is not '':
                        publisher_obj.logo = utils.resize_images(p['image'],
                                                                 PUBLISHERS_FOLDER)
                        # Delete the original image
                        os.remove(p['image'])
                    self.logger.info('Added publisher: %s' % publisher_obj)

            # Add the characters.
            for ch in issue_response['results']['character_credits']:
                character_obj, ch_create = Character.objects.get_or_create(
                    cvid=ch['id'],)
                issue_obj.characters.add(character_obj)

                if ch_create:
                    new_slug = orig = slugify(ch['name'])
                    for x in itertools.count(1):
                        if not Character.objects.filter(slug=new_slug).exists():
                            break
                        new_slug = '%s-%d' % (orig, x)

                    character_obj.name = ch['name']
                    character_obj.slug = new_slug
                    character_obj.save()
                    # Alright get the detail information now.
                    res = self.getDetailInfo(character_obj,
                                             self.character_fields,
                                             ch['api_detail_url'])

                    if character_obj.image:
                        self.create_images(character_obj, CHARACTERS_FOLDERS)

                    if res:
                        self.logger.info('Added character: %s' % character_obj)
                    else:
                        self.logger.warning(
                            'No Character detail was saved for: %s' % character_obj)

            # Add the storyarc.
            for story_arc in issue_response['results']['story_arc_credits']:
                story_obj, s_create = Arc.objects.get_or_create(
                    cvid=story_arc['id'],)
                issue_obj.arcs.add(story_obj)

                if s_create:
                    new_slug = orig = slugify(story_arc['name'])
                    for x in itertools.count(1):
                        if not Arc.objects.filter(slug=new_slug).exists():
                            break
                        new_slug = '%s-%d' % (orig, x)

                    story_obj.name = story_arc['name']
                    story_obj.slug = new_slug
                    story_obj.save()

                    res = self.getDetailInfo(story_obj,
                                             self.arc_fields,
                                             story_arc['api_detail_url'])

                    if story_obj.image:
                        self.create_images(story_obj, ARCS_FOLDER)

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
                c_response = self.getTeamCharacters(team['api_detail_url'])
                if c_response is not None:
                    for character in c_response['results']['characters']:
                        match = Character.objects.filter(cvid=character['id'])
                        if match:
                            match[0].teams.add(team_obj)

                if t_create:
                    new_slug = orig = slugify(team['name'])
                    for x in itertools.count(1):
                        if not Team.objects.filter(slug=new_slug).exists():
                            break
                        new_slug = '%s-%d' % (orig, x)

                    team_obj.name = team['name']
                    team_obj.slug = new_slug
                    team_obj.save()

                    res = self.getDetailInfo(team_obj,
                                             self.team_fields,
                                             team['api_detail_url'])

                    if team_obj.image:
                        self.create_images(team_obj, TEAMS_FOLDERS)

                    if res:
                        self.logger.info('Added team: %s' % team_obj)
                    else:
                        self.logger.info('No Team detail info available for: %s'
                                         % team_obj)

            # Add the creators
            for p in issue_response['results']['person_credits']:
                creator_obj, c_create = Creator.objects.get_or_create(
                    cvid=p['id'],)

                role_obj = Roles.objects.create(
                    creator=creator_obj, issue=issue_obj)

                roles = p['role'].split(',')
                for role in roles:
                    # Remove any whitespace
                    role = role.strip()
                    r, r_create = Role.objects.get_or_create(name=role.title())
                    role_obj.role.add(r)

                if c_create:
                    new_slug = orig = slugify(p['name'])
                    for x in itertools.count(1):
                        if not Creator.objects.filter(slug=new_slug).exists():
                            break
                        new_slug = '%s-%d' % (orig, x)

                    creator_obj.name = p['name']
                    creator_obj.slug = new_slug
                    creator_obj.save()

                    res = self.getDetailInfo(creator_obj,
                                             self.creator_fields,
                                             p['api_detail_url'])

                    if creator_obj.image:
                        self.create_images(creator_obj, CREATORS_FOLDERS)

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
