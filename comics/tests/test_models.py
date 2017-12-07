from django.test import TestCase
from django.utils.text import slugify

from comics.models import Publisher, Arc, Team, Character


class PublisherTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.name = 'DC Comics'
        self.slug = slugify(self.name)
        self.cvid = 1234
        self.desc = 'Home of Superman'

        Publisher.objects.create(name=self.name,
                                 slug=self.slug,
                                 cvid=self.cvid,
                                 desc=self.desc)

    def test_string_representation(self):
        publisher = Publisher.objects.get(id=1)
        self.assertEqual(str(publisher), self.name)

    def test_verbose_name_plural(self):
        publisher = Publisher.objects.get(id=1)
        self.assertEqual(
            str(publisher._meta.verbose_name_plural), "publishers")


class ArcTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.name = 'World without Superman'
        self.slug = slugify(self.name)
        self.cvid = 1234

        Arc.objects.create(name=self.name,
                           slug=self.slug,
                           cvid=self.cvid)

    def test_string_representation(self):
        arc = Arc.objects.get(id=1)
        self.assertEqual(str(arc), self.name)

    def test_verbose_name_plural(self):
        arc = Arc.objects.get(id=1)
        self.assertEqual(
            str(arc._meta.verbose_name_plural), "arcs")


class TeamTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.name = 'Justice League'
        self.slug = slugify(self.name)
        self.cvid = 1234

        Team.objects.create(name=self.name,
                            slug=self.slug,
                            cvid=self.cvid)

    def test_string_representation(self):
        team = Team.objects.get(id=1)
        self.assertEqual(str(team), self.name)

    def test_verbose_name_plural(self):
        team = Team.objects.get(id=1)
        self.assertEqual(
            str(team._meta.verbose_name_plural), "teams")


class CharacterTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.name = 'Superman'
        self.slug = slugify(self.name)
        self.cvid = 1234

        Character.objects.create(name=self.name,
                                 slug=self.slug,
                                 cvid=self.cvid)

    def test_string_representation(self):
        character = Character.objects.get(id=1)
        self.assertEqual(str(character), self.name)

    def test_verbose_name_plural(self):
        character = Character.objects.get(id=1)
        self.assertEqual(
            str(character._meta.verbose_name_plural), "characters")
