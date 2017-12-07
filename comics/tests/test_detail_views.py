from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify

from comics.models import (Publisher)


HTML_OK_CODE = 200


class PublisherDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.name = 'DC Comics'
        self.slug = slugify(self.name)
        Publisher.objects.create(name=self.name,
                                 slug=self.slug)

    def test_view_url_accessible_by_name(self):
        url = reverse('publisher:detail', args=(self.slug,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        url = reverse('publisher:detail', args=(self.slug,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comics/publisher_detail.html')
