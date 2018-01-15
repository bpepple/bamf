from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from comics.models import Arc
from comics.serializers import ArcSerializer


# initialize the APIClient app
client = Client()


class GetAllArcsTest(TestCase):

    def setUp(self):
        Arc.objects.create(cvid='1234', cvurl='http://1.com',
                           name='World War Hulk', slug='world-war-hulk')
        Arc.objects.create(cvid='4321', cvurl='http://2.com',
                           name='Final Crisis', slug='final-crisis')

    def test_view_url_accessible_by_name(self):
        resp = client.get(reverse('api:arc-list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


class GetSingleArcTest(TestCase):

    def setUp(self):
        self.hulk = Arc.objects.create(
            cvid='1234', cvurl='http://1.com', name='World War Hulk', slug='world-war-hulk')
        self.crisis = Arc.objects.create(
            cvid='4321', cvurl='http://2.com', name='Final Crisis', slug='final-crisis')

    def test_get_valid_single_arc(self):
        response = client.get(
            reverse('api:arc-detail', kwargs={'slug': self.hulk.slug}))
        arc = Arc.objects.get(slug=self.hulk.slug)
        serializer = ArcSerializer(arc)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_publisher(self):
        response = client.get(
            reverse('api:arc-detail', kwargs={'slug': 'civil-war'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
