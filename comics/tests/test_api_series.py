from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from comics.models import Series, Publisher


# initialize the APIClient app
client = Client()


class GetAllSeriesTest(TestCase):

    def setUp(self):
        publisher_obj = Publisher.objects.create(
            name='DC Comics', slug='dc-comics')
        Series.objects.create(cvid='1234', cvurl='http://1.com',
                              name='Superman', slug='superman', publisher=publisher_obj)
        Series.objects.create(cvid='4321', cvurl='http://2.com',
                              name='Batman', slug='batman', publisher=publisher_obj)

    def test_view_url_accessible_by_name(self):
        resp = client.get(reverse('api:series-list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
