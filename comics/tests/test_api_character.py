from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from comics.models import Character
from comics.serializers import CharacterSerializer


# initialize the APIClient app
client = Client()


class GetAllCharactersTest(TestCase):

    def setUp(self):
        Character.objects.create(
            cvid='1234', cvurl='http://1.com', name='Superman', slug='superman')
        Character.objects.create(
            cvid='4321', cvurl='http://2.com', name='Batman', slug='batman')

    def test_get_all_characters(self):
        # get API response
        response = client.get(reverse('api:character-list'))
        # get data from db
        characters = Character.objects.all()
        serializer = CharacterSerializer(characters, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleCharacterTest(TestCase):

    def setUp(self):
        self.superman = Character.objects.create(
            cvid='1234', cvurl='http://1.com', name='Superman', slug='superman')
        self.batman = Character.objects.create(
            cvid='4321', cvurl='http://2.com', name='Batman', slug='batman')

    def test_get_valid_single_character(self):
        response = client.get(
            reverse('api:character-detail', kwargs={'slug': self.batman.slug}))
        character = Character.objects.get(slug=self.batman.slug)
        serializer = CharacterSerializer(character)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_character(self):
        response = client.get(
            reverse('api:character-detail', kwargs={'slug': 'wonder-woman'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
