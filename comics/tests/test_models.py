from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify

from comics.models import (Publisher, Arc, Team, Character,
                           Creator, Series, Issue)


class IssueTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        issue_date = timezone.now().date()
        mod_time = timezone.now()
        publisher = Publisher.objects.create(
            name='DC Comics', slug='dc-comics')
        series = Series.objects.create(
            cvid='1234', name='Batman', slug='batman', publisher=publisher)
        cls.issue = Issue.objects.create(cvid='4321', cvurl='http://2.com', slug='batman-1',
                                         file='/home/b.cbz', mod_ts=mod_time, date=issue_date, number='1', series=series)

    def test_issue_creation(self):
        self.assertTrue(isinstance(self.issue, Issue))
        self.assertEqual(str(self.issue), 'Batman #1')

    def test_verbose_name_plural(self):
        self.assertEqual(
            str(self.issue._meta.verbose_name_plural), "issues")


class PublisherTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.name = 'DC Comics'
        cls.slug = slugify(cls.name)
        cls.cvid = 1234
        cls.desc = 'Home of Superman'

        cls.publisher = Publisher.objects.create(
            name=cls.name, slug=cls.slug, cvid=cls.cvid, desc=cls.desc)

    def test_publisher_creation(self):
        self.assertTrue(isinstance(self.publisher, Publisher))
        self.assertEqual(str(self.publisher), self.name)

    def test_verbose_name_plural(self):
        self.assertEqual(
            str(self.publisher._meta.verbose_name_plural), "publishers")


class ArcTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.name = 'World without Superman'
        cls.slug = slugify(cls.name)
        cls.cvid = 1234

        cls.arc = Arc.objects.create(
            name=cls.name, slug=cls.slug, cvid=cls.cvid)

    def test_arc_creation(self):
        self.assertTrue(isinstance(self.arc, Arc))
        self.assertEqual(str(self.arc), self.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(self.arc._meta.verbose_name_plural), "arcs")


class TeamTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.name = 'Justice League'
        cls.slug = slugify(cls.name)
        cls.cvid = 1234

        cls.team = Team.objects.create(
            name=cls.name, slug=cls.slug, cvid=cls.cvid)

    def test_team_creation(self):
        self.assertTrue(isinstance(self.team, Team))
        self.assertEqual(str(self.team), self.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(self.team._meta.verbose_name_plural), "teams")


class CharacterTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.name = 'Superman'
        cls.slug = slugify(cls.name)
        cls.cvid = 1234

        cls.character = Character.objects.create(
            name=cls.name, slug=cls.slug, cvid=cls.cvid)

    def test_character_creation(self):
        self.assertTrue(isinstance(self.character, Character))
        self.assertEqual(str(self.character), self.name)

    def test_verbose_name_plural(self):
        self.assertEqual(
            str(self.character._meta.verbose_name_plural), "characters")


class CreatorTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.name = 'Jason Aaron'
        cls.slug = slugify(cls.name)
        cls.cvid = 1234

        cls.creator = Creator.objects.create(
            name=cls.name, slug=cls.slug, cvid=cls.cvid)

    def test_creator_creation(self):
        self.assertTrue(isinstance(self.creator, Creator))
        self.assertEqual(str(self.creator), self.name)

    def test_verbose_name_plural(self):
        self.assertEqual(
            str(self.creator._meta.verbose_name_plural), "creators")


class SeriesTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.name = 'The Avengers'
        cls.sort = 'Avengers, The'
        cls.slug = slugify(cls.name)
        cls.cvid = 1234

        issue_date = timezone.now().date()
        mod_time = timezone.now()

        pub = Publisher.objects.create(name='DC Comics', slug='dc-comics')
        cls.series = Series.objects.create(
            name=cls.name, slug=cls.slug, cvid=cls.cvid, sort_title=cls.sort, publisher=pub)

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
