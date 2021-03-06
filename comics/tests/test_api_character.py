from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from comics.models import Character
from comics.serializers import CharacterSerializer


class TestCaseBase(TestCase):

    def _create_user(self):
        user = User.objects.create(username='brian')
        user.set_password('1234')
        user.save()

        return user

    def _client_login(self):
        self.client.login(username='brian', password='1234')


class GetAllCharactersTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        cls._create_user(cls)

        for character in range(105):
            Character.objects.create(
                name='Character %s' % character,
                slug='character-%s' % character,
                cvid=character)

    def setUp(self):
        self._client_login()

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('api:character-list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_unauthorized_view_url(self):
        self.client.logout()
        resp = self.client.get(reverse('api:character-list'))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)


class GetSingleCharacterTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        cls._create_user(cls)

        cls.superman = Character.objects.create(
            cvid='1234', cvurl='http://1.com', name='Superman', slug='superman')
        cls.batman = Character.objects.create(
            cvid='4321', cvurl='http://2.com', name='Batman', slug='batman')

    def setUp(self):
        self._client_login()

    def test_get_valid_single_character(self):
        response = self.client.get(
            reverse('api:character-detail', kwargs={'slug': self.batman.slug}))
        character = Character.objects.get(slug=self.batman.slug)
        serializer = CharacterSerializer(character)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_character(self):
        response = self.client.get(
            reverse('api:character-detail', kwargs={'slug': 'wonder-woman'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_view_url(self):
        self.client.logout()
        response = self.client.get(
            reverse('api:character-detail', kwargs={'slug': self.batman.slug}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
