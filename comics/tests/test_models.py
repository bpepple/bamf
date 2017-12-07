from django.test import TestCase
from django.utils.text import slugify

from comics.models import Publisher


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
