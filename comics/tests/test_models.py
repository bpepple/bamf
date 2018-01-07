from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify

from comics.models import (Publisher, Arc, Team, Character,
                           Creator, Series, Issue)


class IssueTest(TestCase):

    def setUp(self):
        issue_date = timezone.now().date()
        mod_time = timezone.now()
        publisher = Publisher.objects.create(
            name='DC Comics', slug='dc-comics')
        series = Series.objects.create(
            cvid='1234', name='Batman', slug='batman', publisher=publisher)
        self.issue = Issue.objects.create(cvid='4321', cvurl='http://2.com', slug='batman-1',
                                          file='/home/b.cbz', mod_ts=mod_time, date=issue_date, number='1', series=series)

    def test_issue_creation(self):
        self.assertTrue(isinstance(self.issue, Issue))
        self.assertEqual(str(self.issue), 'Batman #1')

    def test_verbose_name_plural(self):
        self.assertEqual(
            str(self.issue._meta.verbose_name_plural), "issues")


class PublisherTest(TestCase):

    def setUp(self):
        self.name = 'DC Comics'
        self.slug = slugify(self.name)
        self.cvid = 1234
        self.desc = 'Home of Superman'

        self.publisher = Publisher.objects.create(
            name=self.name, slug=self.slug, cvid=self.cvid, desc=self.desc)

    def test_publisher_creation(self):
        self.assertTrue(isinstance(self.publisher, Publisher))
        self.assertEqual(str(self.publisher), self.name)

    def test_verbose_name_plural(self):
        self.assertEqual(
            str(self.publisher._meta.verbose_name_plural), "publishers")


class ArcTest(TestCase):

    def setUp(self):
        self.name = 'World without Superman'
        self.slug = slugify(self.name)
        self.cvid = 1234

        self.arc = Arc.objects.create(
            name=self.name, slug=self.slug, cvid=self.cvid)

    def test_arc_creation(self):
        self.assertTrue(isinstance(self.arc, Arc))
        self.assertEqual(str(self.arc), self.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(self.arc._meta.verbose_name_plural), "arcs")


class TeamTest(TestCase):

    def setUp(self):
        self.name = 'Justice League'
        self.slug = slugify(self.name)
        self.cvid = 1234

        self.team = Team.objects.create(
            name=self.name, slug=self.slug, cvid=self.cvid)

    def test_team_creation(self):
        self.assertTrue(isinstance(self.team, Team))
        self.assertEqual(str(self.team), self.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(self.team._meta.verbose_name_plural), "teams")


class CharacterTest(TestCase):

    def setUp(self):
        self.name = 'Superman'
        self.slug = slugify(self.name)
        self.cvid = 1234

        self.character = Character.objects.create(
            name=self.name, slug=self.slug, cvid=self.cvid)

    def test_character_creation(self):
        self.assertTrue(isinstance(self.character, Character))
        self.assertEqual(str(self.character), self.name)

    def test_verbose_name_plural(self):
        self.assertEqual(
            str(self.character._meta.verbose_name_plural), "characters")


class CreatorTest(TestCase):

    def setUp(self):
        self.name = 'Jason Aaron'
        self.slug = slugify(self.name)
        self.cvid = 1234

        self.creator = Creator.objects.create(
            name=self.name, slug=self.slug, cvid=self.cvid)

    def test_creator_creation(self):
        self.assertTrue(isinstance(self.creator, Creator))
        self.assertEqual(str(self.creator), self.name)

    def test_verbose_name_plural(self):
        self.assertEqual(
            str(self.creator._meta.verbose_name_plural), "creators")


class SeriesTest(TestCase):

    def setUp(self):
        self.name = 'The Avengers'
        self.sort = 'Avengers, The'
        self.slug = slugify(self.name)
        self.cvid = 1234

        pub = Publisher.objects.create(name='DC Comics', slug='dc-comics')
        self.series = Series.objects.create(
            name=self.name, slug=self.slug, cvid=self.cvid, sort_title=self.sort, publisher=pub)

    def test_series_creation(self):
        self.assertTrue(isinstance(self.series, Series))
        self.assertEqual(str(self.series), self.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(self.series._meta.verbose_name_plural), "Series")

#     TODO: Add test for issue count & unread count.
