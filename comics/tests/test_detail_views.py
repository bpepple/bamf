from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify

from comics.models import (Publisher, Series)


HTML_OK_CODE = 200


class PublisherDetailViewTest(TestCase):

    def setUp(self):
        self.publisher = Publisher.objects.create(
            name='DC Comics',
            slug='dc-comics')

    def test_view_url_accessible_by_name(self):
        url = reverse('publisher:detail', args=(self.publisher.slug,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        url = reverse('publisher:detail', args=(self.publisher.slug,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comics/publisher_detail.html')


class SeriesDetailViewTest(TestCase):

    def setUp(self):
        pub, p_create = Publisher.objects.get_or_create(
            name='DC Comics',
            slug='dc-comics',)

        self.series = Series.objects.create(
            publisher=pub,
            name='Superman',
            slug='superman',
            cvid=1234,)

    def test_view_url_accessible_by_name(self):
        url = reverse('series:detail', args=(self.series.slug,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        url = reverse('series:detail', args=(self.series.slug,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comics/series_detail.html')
