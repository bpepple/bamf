from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from comics.models import Character
from comics.serializers import CharacterSerializer


# initialize the APIClient app
client = Client()


class GetAllCharactersTest(TestCase):

    def setUp(self):
        for character in range(105):
            Character.objects.create(
                name='Character %s' % character,
                slug='character-%s' % character,
                cvid=character)

    def test_view_url_accessible_by_name(self):
        resp = client.get(reverse('api:character-list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


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
