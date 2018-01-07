from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from comics.models import Series, Publisher
from comics.serializers import SeriesSerializer


# initialize the APIClient app
client = Client()


class GetAllSeriesTest(TestCase):

    def setUp(self):
        publisher_obj, p_create = Publisher.objects.get_or_create(
            name='DC Comics', slug='dc-comics')
        Series.objects.create(cvid='1234', cvurl='http://1.com',
                              name='Superman', slug='superman', publisher=publisher_obj)
        Series.objects.create(cvid='4321', cvurl='http://2.com',
                              name='Batman', slug='batman', publisher=publisher_obj)

    def test_get_all_series(self):
        # get API response
        response = client.get(reverse('api:series-list'))
        # get data from db
        series = Series.objects.all()
        serializer = SeriesSerializer(series, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleSeriesTest(TestCase):

    def setUp(self):
        publisher_obj, p_create = Publisher.objects.get_or_create(
            name='DC Comics', slug='dc-comics')
        self.superman = Series.objects.create(
            cvid='1234', cvurl='http://1.com', name='Superman', slug='superman', publisher=publisher_obj)
        self.batman = Series.objects.create(
            cvid='4321', cvurl='http://2.com', name='Batman', slug='batman', publisher=publisher_obj)

    def test_get_valid_single_series(self):
        response = client.get(
            reverse('api:series-detail', kwargs={'slug': self.batman.slug}))
        series = Series.objects.get(slug=self.batman.slug)
        serializer = SeriesSerializer(series)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_series(self):
        response = client.get(
            reverse('api:series-detail', kwargs={'slug': 'teen-titans'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
