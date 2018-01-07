from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify

from comics.models import (Publisher, Arc, Team, Character,
                           Creator, Series, Issue)


class IssueTest(TestCase):

    @classmethod
    def setUpTestData(self):
        issue_date = timezone.now().date()
        mod_time = timezone.now()
        publisher = Publisher.objects.create(
            name='DC Comics', slug='dc-comics')
        series = Series.objects.create(
            cvid='1234', name='Batman', slug='batman', publisher=publisher)
        self.issue = Issue.objects.create(cvid='4321', cvurl='http://2.com', slug='batman-1',
                                          file='/home/b.cbz', mod_ts=mod_time, date=issue_date, number='1', series=series)

    def test_string_representation(self):
        self.assertEqual(str(self.issue), 'Batman #1')

    def test_verbose_name_plural(self):
        self.assertEqual(
            str(self.issue._meta.verbose_name_plural), "issues")


class PublisherTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.name = 'DC Comics'
        self.slug = slugify(self.name)
        self.cvid = 1234
        self.desc = 'Home of Superman'

        self.publisher = Publisher.objects.create(
            name=self.name, slug=self.slug, cvid=self.cvid, desc=self.desc)

    def test_string_representation(self):
        self.assertEqual(str(self.publisher), self.name)

    def test_verbose_name_plural(self):
        self.assertEqual(
            str(self.publisher._meta.verbose_name_plural), "publishers")


class ArcTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.name = 'World without Superman'
        self.slug = slugify(self.name)
        self.cvid = 1234

        self.arc = Arc.objects.create(
            name=self.name, slug=self.slug, cvid=self.cvid)

    def test_string_representation(self):
        self.assertEqual(str(self.arc), self.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(self.arc._meta.verbose_name_plural), "arcs")


class TeamTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.name = 'Justice League'
        self.slug = slugify(self.name)
        self.cvid = 1234

        self.team = Team.objects.create(
            name=self.name, slug=self.slug, cvid=self.cvid)

    def test_string_representation(self):
        self.assertEqual(str(self.team), self.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(self.team._meta.verbose_name_plural), "teams")


class CharacterTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.name = 'Superman'
        self.slug = slugify(self.name)
        self.cvid = 1234

        self.character = Character.objects.create(
            name=self.name, slug=self.slug, cvid=self.cvid)

    def test_string_representation(self):
        self.assertEqual(str(self.character), self.name)

    def test_verbose_name_plural(self):
        self.assertEqual(
            str(self.character._meta.verbose_name_plural), "characters")


class CreatorTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.name = 'Jason Aaron'
        self.slug = slugify(self.name)
        self.cvid = 1234

        self.creator = Creator.objects.create(
            name=self.name, slug=self.slug, cvid=self.cvid)

    def test_string_representation(self):
        self.assertEqual(str(self.creator), self.name)

    def test_verbose_name_plural(self):
        self.assertEqual(
            str(self.creator._meta.verbose_name_plural), "creators")


class SeriesTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.name = 'The Avengers'
        self.sort = 'Avengers, The'
        self.slug = slugify(self.name)
        self.cvid = 1234

        pub = Publisher.objects.create(name='DC Comics', slug='dc-comics')

        self.series = Series.objects.create(
            name=self.name, slug=self.slug, cvid=self.cvid, sort_title=self.sort, publisher=pub)

    def test_string_representation(self):
        self.assertEqual(str(self.series), self.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(self.series._meta.verbose_name_plural), "Series")

#     TODO: Add test for issue count & unread count.
