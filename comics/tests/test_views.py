from django.test import TestCase
from django.urls import reverse

from comics.models import Publisher


HTML_OK_CODE = 200


class PublisherListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 35 test publishers for pagination tests
        number_of_publishers = 35
        for pub_num in range(number_of_publishers):
            Publisher.objects.create(
                name='Publisher %s' % pub_num,
                slug='publisher-%s' % pub_num,)

    def test_view_url_exists_at_desired_location(self): 
        resp = self.client.get('/publisher/') 
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('publisher:list'))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('publisher:list'))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comics/publisher_list.html')

    def test_pagination_is_twenty_eight(self):
        resp = self.client.get(reverse('publisher:list'))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['publisher_list']) == 28)

    def test_lists_all_publishers(self):
        # Get second page and confirm it has (exactly) remaining 7 items
        resp = self.client.get(reverse('publisher:list') + '?page=2')
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['publisher_list']) == 7)
