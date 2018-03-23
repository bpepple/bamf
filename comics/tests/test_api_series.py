from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from comics.models import Series, Publisher
from comics.serializers import SeriesSerializer


class TestCaseBase(TestCase):

    def _create_user(self):
        user = User.objects.create(username='brian')
        user.set_password('1234')
        user.save()

        return user

    def _client_login(self):
        self.client.login(username='brian', password='1234')


class GetAllSeriesTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        cls._create_user(cls)

        publisher_obj = Publisher.objects.create(
            name='DC Comics', slug='dc-comics')
        Series.objects.create(cvid='1234', cvurl='http://1.com',
                              name='Superman', slug='superman', publisher=publisher_obj)
        Series.objects.create(cvid='4321', cvurl='http://2.com',
                              name='Batman', slug='batman', publisher=publisher_obj)

    def setUp(self):
        self._client_login()

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('api:series-list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_unauthorized_view_url(self):
        self.client.logout()
        resp = self.client.get(reverse('api:series-list'))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)


class GetSingleSeriesTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        cls._create_user(cls)

        factory = APIRequestFactory()
        request = factory.get('/')

        cls.serializer_context = {
            'request': Request(request),
        }

        publisher_obj = Publisher.objects.create(name='Marvel', slug='marvel')
        cls.thor = Series.objects.create(cvid='1234', cvurl='https://comicvine.com',
                                         name='The Mighty Thor', slug='the-mighty-thor',
                                         publisher=publisher_obj)

    def setUp(self):
        self._client_login()

    def test_get_valid_single_issue(self):
        resp = self.client.get(
            reverse('api:series-detail', kwargs={'slug': self.thor.slug}))
        series = Series.objects.get(slug=self.thor.slug)
        serializer = SeriesSerializer(series, context=self.serializer_context)
        self.assertEqual(resp.data, serializer.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_unauthorized_view_url(self):
        self.client.logout()
        response = self.client.get(
            reverse('api:series-detail', kwargs={'slug': self.thor.slug}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
