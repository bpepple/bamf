from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from comics.models import Creator
from comics.serializers import CreatorSerializer


# initialize the APIClient app
client = Client()


class GetAllCreatorsTest(TestCase):

    def setUp(self):
        Creator.objects.create(
            cvid='1234', cvurl='http://1.com', name='John Byrne', slug='john-byrne')
        Creator.objects.create(cvid='4321', cvurl='http://2.com',
                               name='Walter Simonson', slug='walter-simonson')

    def test_get_all_creators(self):
        # get API response
        response = client.get(reverse('api:creator-list'))
        # get data from db
        creators = Creator.objects.all()
        serializer = CreatorSerializer(creators, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleCreatorTest(TestCase):

    def setUp(self):
        self.john = Creator.objects.create(
            cvid='1234', cvurl='http://1.com', name='John Byrne', slug='john-byrne')
        self.walter = Creator.objects.create(
            cvid='4321', cvurl='http://2.com', name='Walter Simonson', slug='walter-simonson')

    def test_get_valid_single_creator(self):
        response = client.get(
            reverse('api:creator-detail', kwargs={'slug': self.walter.slug}))
        creator = Creator.objects.get(slug=self.walter.slug)
        serializer = CreatorSerializer(creator)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_creator(self):
        response = client.get(
            reverse('api:creator-detail', kwargs={'slug': 'art-adams'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
