from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from comics.models import Publisher
from comics.serializers import PublisherSerializer


class GetAllPublisherTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Publisher.objects.create(name='DC Comics', slug='dc-comics')
        Publisher.objects.create(name='Marvel', slug='marvel')

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('api:publisher-list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


class GetSinglePublisherTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.dc = Publisher.objects.create(name='DC Comics', slug='dc-comics')
        cls.marvel = Publisher.objects.create(name='Marvel', slug='marvel')

    def test_get_valid_single_publisher(self):
        response = self.client.get(
            reverse('api:publisher-detail', kwargs={'slug': self.dc.slug}))
        publisher = Publisher.objects.get(slug=self.dc.slug)
        serializer = PublisherSerializer(publisher)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_publisher(self):
        response = self.client.get(
            reverse('api:publisher-detail', kwargs={'slug': 'dark-horse'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
