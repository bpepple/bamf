from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from comics.models import Issue, Publisher, Series
from comics.serializers import IssueSerializer

issue_date = timezone.now().date()
mod_time = timezone.now()


class GetAllIssueTest(TestCase):

    def setUp(self):
        self.client = Client()
        publisher_obj = Publisher.objects.create(
            name='DC Comics', slug='dc-comics')
        series_obj = Series.objects.create(
            cvid='1234', cvurl='http://1.com', name='Superman', slug='superman', publisher=publisher_obj)
        Issue.objects.create(cvid='1234', cvurl='http://1.com', slug='superman-1',
                             file='/home/a.cbz', mod_ts=mod_time, date=issue_date, number='1', series=series_obj)
        Issue.objects.create(cvid='4321', cvurl='http://2.com', slug='batman-1',
                             file='/home/b.cbz', mod_ts=mod_time, date=issue_date, number='1', series=series_obj)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('api:issue-list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


class GetSingleIssueTest(TestCase):

    def setUp(self):
        factory = APIRequestFactory()
        request = factory.get('/')

        self.serializer_context = {
            'request': Request(request),
        }

        publisher_obj = Publisher.objects.create(
            name='DC Comics', slug='dc-comics')
        series_obj = Series.objects.create(
            cvid='1234', cvurl='http://1.com', name='Superman', slug='superman', publisher=publisher_obj)
        self.superman = Issue.objects.create(cvid='1234', cvurl='http://1.com', slug='superman-1',
                                             file='/home/a.cbz', mod_ts=mod_time, date=issue_date, number='1', series=series_obj)

    def test_get_valid_single_issue(self):
        response = self.client.get(
            reverse('api:issue-detail', kwargs={'slug': self.superman.slug}))
        issue = Issue.objects.get(slug=self.superman.slug)
        serializer = IssueSerializer(issue, context=self.serializer_context)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
