from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from comics.models import Publisher
from comics.serializers import PublisherSerializer


# initialize the APIClient app
client = Client()


class GetAllPublisherTest(TestCase):

    def setUp(self):
        Publisher.objects.create(
            name='DC Comics', slug='dc-comics', logo='images/1.jpg')
        Publisher.objects.create(
            name='Marvel', slug='marvel', logo='images/2.jpg')

    def test_view_url_accessible_by_name(self):
        resp = client.get(reverse('api:publisher-list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


class GetSinglePublisherTest(TestCase):

    def setUp(self):
        self.dc = Publisher.objects.create(
            name='DC Comics', slug='dc-comics', logo='images/1.jpg')
        self.marvel = Publisher.objects.create(
            name='Marvel', slug='marvel', logo='images/2.jpg')

    def test_get_valid_single_publisher(self):
        response = client.get(
            reverse('api:publisher-detail', kwargs={'slug': self.dc.slug}))
        publisher = Publisher.objects.get(slug=self.dc.slug)
        serializer = PublisherSerializer(publisher)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_publisher(self):
        response = client.get(
            reverse('api:publisher-detail', kwargs={'slug': 'dark-horse'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
