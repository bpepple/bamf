from datetime import datetime
import os

from django.conf import settings
from django.test import TestCase
from django.utils import timezone

from comics.models import (Settings, Issue, Publisher,
                           Creator, Series, Team, Arc,
                           Character)
from comics.utils.comicimporter import ComicImporter


class TestImportComics(TestCase):

    @classmethod
    def setUpTestData(cls):
        issue_date = timezone.now().date()
        mod_time = timezone.now()

        cls.pub_cvid = 10
        cls.ser_cvid = 796
        cls.team_cvid = 27589
        cls.arc_cvid = 56504
        cls.creator_cvid = 41468
        cls.issue_cvid = 286879
        cls.character_cvid = 2357

        cls.dc = Publisher.objects.create(
            cvid=cls.pub_cvid, name='DC Comics', slug='dc-comics')
        cls.bat = Series.objects.create(
            cvid=cls.ser_cvid, name='Batman', slug='batman', publisher=cls.dc)
        cls.jsa = Team.objects.create(cvid=cls.team_cvid, name='Justice Society of America',
                                      slug='justice-society-of-america')
        cls.arc = Arc.objects.create(cvid=cls.arc_cvid, name='The Death of Captain America',
                                     slug='the-death-of-captain-america')
        cls.creator = Creator.objects.create(cvid=cls.creator_cvid, name='Ed Brubaker',
                                             slug='ed-brubaker')
        cls.issue = Issue.objects.create(series=cls.bat, cvid=cls.issue_cvid,
                                         slug='batman-713', mod_ts=mod_time, date=issue_date,
                                         number='713')
        cls.aquaman = Character.objects.create(cvid=cls.character_cvid, name='Aquaman',
                                               slug='aquaman')

        test_data_dir = settings.BASE_DIR + os.sep + 'comics/fixtures'
        Settings.objects.create(comics_directory=test_data_dir,
                                api_key='27431e6787042105bd3e47e169a624521f89f3a4')

    def tearDown(self):
        # Clean up all the images that were downloaded.
        for publisher in Publisher.objects.all():
            publisher.delete()

        for creator in Creator.objects.all():
            creator.delete()

    def test_refresh_character(self):
        ci = ComicImporter()
        ci.refreshCharacterData(self.character_cvid)
        self.aquaman.refresh_from_db()

        self.assertTrue(self.aquaman.desc)

    def test_refresh_publisher(self):
        ci = ComicImporter()
        ci.refreshPublisherData(self.pub_cvid)
        self.dc.refresh_from_db()

        self.assertTrue(self.dc.desc)

    def test_refresh_series(self):
        ci = ComicImporter()
        ci.refreshSeriesData(self.ser_cvid)
        self.bat.refresh_from_db()

        self.assertTrue(self.bat.desc)
        self.assertEqual(self.bat.year, 1940)

    def test_refresh_team(self):
        ci = ComicImporter()
        ci.refreshTeamData(self.team_cvid)
        self.jsa.refresh_from_db()

        self.assertTrue(self.jsa.desc)

    def test_refresh_arc(self):
        ci = ComicImporter()
        ci.refreshArcData(self.arc_cvid)
        self.arc.refresh_from_db()

        self.assertTrue(self.arc.desc)

    def test_refresh_creator(self):
        ci = ComicImporter()
        ci.refreshCreatorData(self.creator_cvid)
        self.creator.refresh_from_db()

        self.assertTrue(self.creator.desc)

    def test_refresh_issue(self):
        ci = ComicImporter()
        ci.refreshIssueData(self.issue_cvid)
        self.issue.refresh_from_db()

        self.assertTrue(self.issue.desc)
        self.assertTrue(self.issue.name)

    def test_import_comic(self):
        ci = ComicImporter()
        ci.import_comic_files()

        cover_date = datetime.strptime('December 01, 1965', '%B %d, %Y')
        issue = Issue.objects.get(cvid=8192)

        self.assertEqual(str(issue), 'Captain Atom #078')
        self.assertEqual(issue.date, datetime.date(cover_date))
        self.assertTrue(issue.cover)
