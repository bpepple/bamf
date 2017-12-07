from django.test import TestCase
from django.urls import reverse

from comics.models import (Publisher, Series, Creator, Character, Team)


HTML_OK_CODE = 200
PAGINATE_DEFAULT_VAL = 28
PAGINATE_TEST_VAL = 35
PAGINATE_DIFF_VAL = (PAGINATE_TEST_VAL - PAGINATE_DEFAULT_VAL)


class PublisherListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create 35 test publishers for pagination tests
        number_of_publishers = PAGINATE_TEST_VAL
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
        self.assertTrue(
            len(resp.context['publisher_list']) == PAGINATE_DEFAULT_VAL)

    def test_lists_all_publishers(self):
        # Get second page and confirm it has (exactly) remaining 7 items
        resp = self.client.get(reverse('publisher:list') + '?page=2')
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['publisher_list']) == PAGINATE_DIFF_VAL)


class SeriesListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        pub, p_create = Publisher.objects.get_or_create(
            name='Marvel',
            slug='marvel')
        number_of_series = PAGINATE_TEST_VAL
        for ser_num in range(number_of_series):
            Series.objects.create(
                name='Series %s' % ser_num,
                slug='series-%s' % ser_num,
                publisher=pub,
                cvid=ser_num)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/series/')
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('series:list'))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('series:list'))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comics/series_list.html')

    def test_pagination_is_twenty_eight(self):
        resp = self.client.get(reverse('series:list'))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['series_list']) == PAGINATE_DEFAULT_VAL)

    def test_lists_all_series(self):
        resp = self.client.get(reverse('series:list') + '?page=2')
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['series_list']) == PAGINATE_DIFF_VAL)


class CreatorListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_creators = PAGINATE_TEST_VAL
        for creator in range(number_of_creators):
            Creator.objects.create(
                name='Creator %s' % creator,
                slug='creator-%s' % creator,
                cvid=creator)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/creator/')
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('creator:list'))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('creator:list'))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comics/creator_list.html')

    def test_pagination_is_twenty_eight(self):
        resp = self.client.get(reverse('creator:list'))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['creator_list']) == PAGINATE_DEFAULT_VAL)

    def test_lists_all_creators(self):
        resp = self.client.get(reverse('creator:list') + '?page=2')
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['creator_list']) == PAGINATE_DIFF_VAL)


class CharacterListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_characters = PAGINATE_TEST_VAL
        for character in range(number_of_characters):
            Character.objects.create(
                name='Character %s' % character,
                slug='character-%s' % character,
                cvid=character)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/character/')
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('character:list'))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('character:list'))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comics/character_list.html')

    def test_pagination_is_twenty_eight(self):
        resp = self.client.get(reverse('character:list'))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['character_list']) == PAGINATE_DEFAULT_VAL)

    def test_lists_all_characters(self):
        resp = self.client.get(reverse('character:list') + '?page=2')
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['character_list']) == PAGINATE_DIFF_VAL)


class TeamListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_teams = PAGINATE_TEST_VAL
        for team in range(number_of_teams):
            Team.objects.create(
                name='Team %s' % team,
                slug='team-%s' % team,
                cvid=team)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/team/')
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('team:list'))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('team:list'))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comics/team_list.html')

    def test_pagination_is_twenty_eight(self):
        resp = self.client.get(reverse('team:list'))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['team_list']) == PAGINATE_DEFAULT_VAL)

    def test_lists_all_teams(self):
        resp = self.client.get(reverse('team:list') + '?page=2')
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['team_list']) == PAGINATE_DIFF_VAL)
