from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from comics.models import Issue, Publisher, Series


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

    def test_view_url_accessible_by_name(self):
        resp = client.get(reverse('api:issue-list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
