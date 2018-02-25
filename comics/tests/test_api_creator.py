from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from comics.models import Creator
from comics.serializers import CreatorSerializer


class GetAllCreatorsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Creator.objects.create(
            cvid='1234', cvurl='http://1.com', name='John Byrne', slug='john-byrne')
        Creator.objects.create(cvid='4321', cvurl='http://2.com',
                               name='Walter Simonson', slug='walter-simonson')

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('api:creator-list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


class GetSingleCreatorTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.john = Creator.objects.create(
            cvid='1234', cvurl='http://1.com', name='John Byrne', slug='john-byrne')
        cls.walter = Creator.objects.create(
            cvid='4321', cvurl='http://2.com', name='Walter Simonson', slug='walter-simonson')

    def test_get_valid_single_creator(self):
        response = self.client.get(
            reverse('api:creator-detail', kwargs={'slug': self.walter.slug}))
        creator = Creator.objects.get(slug=self.walter.slug)
        serializer = CreatorSerializer(creator)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_creator(self):
        response = self.client.get(
            reverse('api:creator-detail', kwargs={'slug': 'art-adams'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
