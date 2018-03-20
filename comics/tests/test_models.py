import os

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify

from comics.models import (Publisher, Arc, Team, Character,
                           Creator, Series, Issue, Settings)


HTML_OK_CODE = 200


class TestCaseBase(TestCase):

    def _create_user(self):
        user = User.objects.create(username='brian')
        user.set_password('1234')
        user.save()

        return user

    def _client_login(self):
        self.client.login(username='brian', password='1234')


class SettingsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_data_dir = settings.BASE_DIR + os.sep + 'comics/fixtures'
        cls.settings = Settings.objects.create(comics_directory=test_data_dir,
                                               api_key='27431e6787042105bd3e47e169a624521f89f3a4')

    def test_settings_creation(self):
        self.assertTrue(isinstance(self.settings, Settings))
        self.assertTrue(str(self.settings), 'Settings')

    def test_verbose_name_plural(self):
        self.assertEqual(
            str(self.settings._meta.verbose_name_plural), "Settings")


class IssueTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        cls._create_user(cls)

        issue_date = timezone.now().date()
        mod_time = timezone.now()
        publisher = Publisher.objects.create(
            name='DC Comics', slug='dc-comics')
        series = Series.objects.create(
            cvid='1234', name='Batman', slug='batman', publisher=publisher)
        cls.issue = Issue.objects.create(cvid='4321', cvurl='http://2.com', slug='batman-1',
                                         file='/home/b.cbz', mod_ts=mod_time, date=issue_date, number='1', series=series)

    def setUp(self):
        self._client_login()

    def test_issue_creation(self):
        self.assertTrue(isinstance(self.issue, Issue))
        self.assertEqual(str(self.issue), 'Batman #1')

    def test_verbose_name_plural(self):
        self.assertEqual(
            str(self.issue._meta.verbose_name_plural), "issues")

    def test_absolute_url(self):
        resp = self.client.get(self.issue.get_absolute_url())
        self.assertEqual(resp.status_code, HTML_OK_CODE)


class PublisherTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        cls._create_user(cls)

        cls.name = 'DC Comics'
        cls.slug = slugify(cls.name)
        cls.cvid = 1234
        cls.desc = 'Home of Superman'

        cls.publisher = Publisher.objects.create(name=cls.name, slug=cls.slug,
                                                 cvid=cls.cvid, desc=cls.desc)

        Series.objects.create(name='Batman', slug='batman', cvid='1234',
                              sort_title='Batman', publisher=cls.publisher)

    def setUp(self):
        self._client_login()

    def test_series_count(self):
        self.assertEqual(self.publisher.series_count(), 1)

    def test_publisher_creation(self):
        self.assertTrue(isinstance(self.publisher, Publisher))
        self.assertEqual(str(self.publisher), self.name)

    def test_verbose_name_plural(self):
        self.assertEqual(
            str(self.publisher._meta.verbose_name_plural), "publishers")

    def test_absolute_url(self):
        resp = self.client.get(self.publisher.get_absolute_url())
        self.assertEqual(resp.status_code, HTML_OK_CODE)


class ArcTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        cls._create_user(cls)

        cls.name = 'World without Superman'
        cls.slug = slugify(cls.name)
        cls.cvid = 1234

        cls.arc = Arc.objects.create(
            name=cls.name, slug=cls.slug, cvid=cls.cvid)

    def setUp(self):
        self._client_login()

    def test_arc_creation(self):
        self.assertTrue(isinstance(self.arc, Arc))
        self.assertEqual(str(self.arc), self.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(self.arc._meta.verbose_name_plural), "arcs")

    def test_absolute_url(self):
        resp = self.client.get(self.arc.get_absolute_url())
        self.assertEqual(resp.status_code, HTML_OK_CODE)


class TeamTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        cls._create_user(cls)

        cls.name = 'Justice League'
        cls.slug = slugify(cls.name)
        cls.cvid = 1234

        cls.team = Team.objects.create(
            name=cls.name, slug=cls.slug, cvid=cls.cvid)

    def setUp(self):
        self._client_login()

    def test_team_creation(self):
        self.assertTrue(isinstance(self.team, Team))
        self.assertEqual(str(self.team), self.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(self.team._meta.verbose_name_plural), "teams")

    def test_absolute_url(self):
        resp = self.client.get(self.team.get_absolute_url())
        self.assertEqual(resp.status_code, HTML_OK_CODE)


class CharacterTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        cls._create_user(cls)

        cls.name = 'Superman'
        cls.slug = slugify(cls.name)
        cls.cvid = 1234

        cls.character = Character.objects.create(
            name=cls.name, slug=cls.slug, cvid=cls.cvid)

    def setUp(self):
        self._client_login()

    def test_character_creation(self):
        self.assertTrue(isinstance(self.character, Character))
        self.assertEqual(str(self.character), self.name)

    def test_verbose_name_plural(self):
        self.assertEqual(
            str(self.character._meta.verbose_name_plural), "characters")

    def test_absolute_url(self):
        resp = self.client.get(self.character.get_absolute_url())
        self.assertEqual(resp.status_code, HTML_OK_CODE)


class CreatorTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        cls._create_user(cls)

        cls.name = 'Jason Aaron'
        cls.slug = slugify(cls.name)
        cls.cvid = 1234

        cls.creator = Creator.objects.create(
            name=cls.name, slug=cls.slug, cvid=cls.cvid)

    def setUp(self):
        self._client_login()

    def test_creator_creation(self):
        self.assertTrue(isinstance(self.creator, Creator))
        self.assertEqual(str(self.creator), self.name)

    def test_verbose_name_plural(self):
        self.assertEqual(
            str(self.creator._meta.verbose_name_plural), "creators")

    def test_absolute_url(self):
        resp = self.client.get(self.creator.get_absolute_url())
        self.assertEqual(resp.status_code, HTML_OK_CODE)


class SeriesTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        cls._create_user(cls)

        cls.name = 'The Avengers'
        cls.sort = 'Avengers, The'
        cls.slug = slugify(cls.name)
        cls.cvid = 1234

        issue_date = timezone.now().date()
        mod_time = timezone.now()

        pub = Publisher.objects.create(name='DC Comics', slug='dc-comics')
        cls.series = Series.objects.create(name=cls.name, slug=cls.slug,
                                           cvid=cls.cvid, sort_title=cls.sort,
                                           publisher=pub)

        # Create 9 issues to test unread counts.
        for i in range(9):
            slug = slugify(cls.name + ' ' + str(i))
            tst_file = '/home/b-' + str(i) + '.cbz'
            Issue.objects.create(cvid=str(i), cvurl='http://2.com', slug=slug,
                                 file=tst_file, mod_ts=mod_time, date=issue_date,
                                 number=str(i), series=cls.series)

        # Create the 10th issue as read.
        Issue.objects.create(cvid='1234', cvurl='http://2.com', slug='test', file='/home/test.cbz',
                             mod_ts=mod_time, date=issue_date, number='50', status=2, series=cls.series)

    def setUp(self):
        self._client_login()

    def test_series_creation(self):
        self.assertTrue(isinstance(self.series, Series))
        self.assertEqual(str(self.series), self.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(self.series._meta.verbose_name_plural), "Series")

    def test_unread_issue_count(self):
        unread_count = self.series.unread_issue_count
        self.assertEqual(unread_count, 9)

    def test_issue_count(self):
        issue_count = self.series.issue_count
        self.assertEqual(issue_count, 10)

    def test_absolute_url(self):
        resp = self.client.get(self.series.get_absolute_url())
        self.assertEqual(resp.status_code, HTML_OK_CODE)
