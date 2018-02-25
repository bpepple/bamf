from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from comics.models import Team
from comics.serializers import TeamSerializer


class GetAllTeamsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Team.objects.create(cvid='1234', cvurl='http://1.com',
                            name='Teen Titans', slug='teen-titans')
        Team.objects.create(cvid='4321', cvurl='http://2.com',
                            name='The Avengers', slug='the-avengers')

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('api:team-list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


class GetSingleTeamTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.titans = Team.objects.create(
            cvid='1234', cvurl='http://1.com', name='Teen Titans', slug='teen-titans')
        cls.avengers = Team.objects.create(
            cvid='4321', cvurl='http://2.com', name='The Avengers', slug='the-avengers')

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
