from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from comics.models import Creator
from comics.serializers import CreatorSerializer


class TestCaseBase(TestCase):

    def _create_user(self):
        user = User.objects.create(username='brian')
        user.set_password('1234')
        user.save()

        return user

    def _client_login(self):
        self.client.login(username='brian', password='1234')


class GetAllCreatorsTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        cls._create_user(cls)

        Creator.objects.create(
            cvid='1234', cvurl='http://1.com', name='John Byrne', slug='john-byrne')
        Creator.objects.create(cvid='4321', cvurl='http://2.com',
                               name='Walter Simonson', slug='walter-simonson')

    def setUp(self):
        self._client_login()

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('api:creator-list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_unauthorized_view_url(self):
        self.client.logout()
        resp = self.client.get(reverse('api:creator-list'))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)


class GetSingleCreatorTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        cls._create_user(cls)

        cls.john = Creator.objects.create(
            cvid='1234', cvurl='http://1.com', name='John Byrne', slug='john-byrne')
        cls.walter = Creator.objects.create(
            cvid='4321', cvurl='http://2.com', name='Walter Simonson', slug='walter-simonson')

    def setUp(self):
        self._client_login()

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

    def test_unauthorized_view_url(self):
        self.client.logout()
        response = self.client.get(
            reverse('api:creator-detail', kwargs={'slug': self.walter.slug}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
