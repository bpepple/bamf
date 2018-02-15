from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from comics.models import Series, Publisher
from comics.serializers import SeriesSerializer


class GetAllSeriesTest(TestCase):

    def setUp(self):
        self.client = Client()
        publisher_obj = Publisher.objects.create(
            name='DC Comics', slug='dc-comics')
        Series.objects.create(cvid='1234', cvurl='http://1.com',
                              name='Superman', slug='superman', publisher=publisher_obj)
        Series.objects.create(cvid='4321', cvurl='http://2.com',
                              name='Batman', slug='batman', publisher=publisher_obj)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('api:series-list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


class GetSingleSeriesTest(TestCase):

    def setUp(self):
        factory = APIRequestFactory()
        request = factory.get('/')

        self.serializer_context = {
            'request': Request(request),
        }

        self.client = Client()
        publisher_obj = Publisher.objects.create(name='Marvel', slug='marvel')
        self.thor = Series.objects.create(cvid='1234', cvurl='https://comicvine.com',
                                          name='The Mighty Thor', slug='the-mighty-thor',
                                          publisher=publisher_obj)

    def test_get_valid_single_issue(self):
        resp = self.client.get(
            reverse('api:series-detail', kwargs={'slug': self.thor.slug}))
        series = Series.objects.get(slug=self.thor.slug)
        serializer = SeriesSerializer(series, context=self.serializer_context)
        self.assertEqual(resp.data, serializer.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
