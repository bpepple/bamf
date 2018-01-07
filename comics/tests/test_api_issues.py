from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from comics.models import Issue, Publisher, Series
from comics.serializers import IssueSerializer


# initialize the APIClient app
client = Client()

issue_date = timezone.now().date()
mod_time = timezone.now()


class GetAllIssueTest(TestCase):

    def setUp(self):
        publisher_obj = Publisher.objects.create(
            name='DC Comics', slug='dc-comics')
        series_obj = Series.objects.create(
            cvid='1234', cvurl='http://1.com', name='Superman', slug='superman', publisher=publisher_obj)
        Issue.objects.create(cvid='1234', cvurl='http://1.com', slug='superman-1',
                             file='/home/a.cbz', mod_ts=mod_time, date=issue_date, number='1', series=series_obj)
        Issue.objects.create(cvid='4321', cvurl='http://2.com', slug='batman-1',
                             file='/home/b.cbz', mod_ts=mod_time, date=issue_date, number='1', series=series_obj)

    def test_get_all_series(self):
        # get API response
        response = client.get(reverse('api:issue-list'))
        # get data from db
        issues = Issue.objects.all()
        serializer = IssueSerializer(issues, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleIssueTest(TestCase):

    def setUp(self):
        publisher_obj = Publisher.objects.create(
            name='DC Comics', slug='dc-comics')
        series_obj = Series.objects.create(
            cvid='1234', cvurl='http://1.com', name='Superman', slug='superman', publisher=publisher_obj)
        self.superman = Issue.objects.create(cvid='1234', cvurl='http://1.com', slug='superman-1',
                                             file='/home/a.cbz', mod_ts=mod_time, date=issue_date, number='1', series=series_obj)
        self.batman = Issue.objects.create(cvid='4321', cvurl='http://2.com', slug='batman-1',
                                           file='/home/b.cbz', mod_ts=mod_time, date=issue_date, number='1', series=series_obj)

    def test_get_valid_single_series(self):
        response = client.get(
            reverse('api:issue-detail', kwargs={'slug': self.batman.slug}))
        issue = Issue.objects.get(slug=self.batman.slug)
        serializer = IssueSerializer(issue)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_series(self):
        response = client.get(
            reverse('api:issue-detail', kwargs={'slug': 'teen-titans-1'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
