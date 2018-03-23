from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from comics.models import Team
from comics.serializers import TeamSerializer


class TestCaseBase(TestCase):

    def _create_user(self):
        user = User.objects.create(username='brian')
        user.set_password('1234')
        user.save()

        return user

    def _client_login(self):
        self.client.login(username='brian', password='1234')


class GetAllTeamsTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        cls._create_user(cls)

        Team.objects.create(cvid='1234', cvurl='http://1.com',
                            name='Teen Titans', slug='teen-titans')
        Team.objects.create(cvid='4321', cvurl='http://2.com',
                            name='The Avengers', slug='the-avengers')

    def setUp(self):
        self._client_login()

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('api:team-list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_unauthorized_view_url(self):
        self.client.logout()
        resp = self.client.get(reverse('api:team-list'))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)


class GetSingleTeamTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        cls._create_user(cls)

        cls.titans = Team.objects.create(
            cvid='1234', cvurl='http://1.com', name='Teen Titans', slug='teen-titans')
        cls.avengers = Team.objects.create(
            cvid='4321', cvurl='http://2.com', name='The Avengers', slug='the-avengers')

    def setUp(self):
        self._client_login()

    def test_get_valid_single_team(self):
        response = self.client.get(
            reverse('api:team-detail', kwargs={'slug': self.avengers.slug}))
        team = Team.objects.get(slug=self.avengers.slug)
        serializer = TeamSerializer(team)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_team(self):
        response = self.client.get(
            reverse('api:team-detail', kwargs={'slug': 'justice-league'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_view_url(self):
        self.client.logout()
        response = self.client.get(
            reverse('api:team-detail', kwargs={'slug': self.avengers.slug}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
