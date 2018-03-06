from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from comics.models import (Publisher, Series, Creator,
                           Character, Team, Arc)

HTML_OK_CODE = 200

PAGINATE_TEST_VAL = 35
PAGINATE_DEFAULT_VAL = 30
PAGINATE_DIFF_VAL = (PAGINATE_TEST_VAL - PAGINATE_DEFAULT_VAL)


class PublisherSearchViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='brian')
        user.set_password('1234')
        user.save()

        for pub_num in range(PAGINATE_TEST_VAL):
            Publisher.objects.create(
                name='Publisher %s' % pub_num,
                slug='publisher-%s' % pub_num,
                logo='images/1.jpg')

    def setUp(self):
        self.client.login(username='brian', password='1234')

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/publisher/search/page1/')
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('publisher:search', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('publisher:search', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comics/publisher_list.html')

    def test_pagination_is_thirty(self):
        resp = self.client.get('/publisher/search/page1/?q=pub')
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['publisher_list']) == PAGINATE_DEFAULT_VAL)

    def test_lists_all_publishers(self):
        # Get second page and confirm it has (exactly) remaining 7 items
        resp = self.client.get('/publisher/search/page2/?q=pub')
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['publisher_list']) == PAGINATE_DIFF_VAL)


class SeriesSearchViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='brian')
        user.set_password('1234')
        user.save()

        pub = Publisher.objects.create(name='Marvel', slug='marvel')

        for ser_num in range(PAGINATE_TEST_VAL):
            Series.objects.create(
                name='Series %s' % ser_num,
                slug='series-%s' % ser_num,
                publisher=pub,
                cvid=ser_num)

    def setUp(self):
        self.client.login(username='brian', password='1234')

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/series/search/page1/')
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('series:search', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('series:search', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comics/series_list.html')

    def test_pagination_is_thirty(self):
        resp = self.client.get('/series/search/page1/?q=ser')
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['series_list']) == PAGINATE_DEFAULT_VAL)

    def test_lists_all_series(self):
        resp = self.client.get('/series/search/page2/?q=ser')
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['series_list']) == PAGINATE_DIFF_VAL)


class CreatorSearchViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='brian')
        user.set_password('1234')
        user.save()

        for creator in range(PAGINATE_TEST_VAL):
            Creator.objects.create(
                name='Creator %s' % creator,
                slug='creator-%s' % creator,
                cvid=creator)

    def setUp(self):
        self.client.login(username='brian', password='1234')

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/creator/search/page1/')
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('creator:search', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('creator:search', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comics/creator_list.html')

    def test_pagination_is_thirty(self):
        resp = self.client.get('/creator/search/page1/?q=creat')
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['creator_list']) == PAGINATE_DEFAULT_VAL)

    def test_lists_all_creators(self):
        resp = self.client.get('/creator/search/page2/?q=creat')
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['creator_list']) == PAGINATE_DIFF_VAL)


class CharacterSearchViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='brian')
        user.set_password('1234')
        user.save()

        for character in range(PAGINATE_TEST_VAL):
            Character.objects.create(
                name='Character %s' % character,
                slug='character-%s' % character,
                cvid=character)

    def setUp(self):
        self.client.login(username='brian', password='1234')

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/character/search/page1/')
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('character:search', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('character:search', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comics/character_list.html')

    def test_pagination_is_thirty(self):
        resp = self.client.get('/character/search/page1/?q=chara')
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['character_list']) == PAGINATE_DEFAULT_VAL)

    def test_lists_all_characters(self):
        resp = self.client.get('/character/search/page2/?q=chara')
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['character_list']) == PAGINATE_DIFF_VAL)


class TeamSearchViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='brian')
        user.set_password('1234')
        user.save()

        for team in range(PAGINATE_TEST_VAL):
            Team.objects.create(
                name='Team %s' % team,
                slug='team-%s' % team,
                cvid=team)

    def setUp(self):
        self.client.login(username='brian', password='1234')

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/team/search/page1/')
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('team:search', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('team:search', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comics/team_list.html')

    def test_pagination_is_thirty(self):
        resp = self.client.get('/team/search/page1/?q=tea')
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['team_list']) == PAGINATE_DEFAULT_VAL)

    def test_lists_all_teams(self):
        resp = self.client.get('/team/search/page2/?q=tea')
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['team_list']) == PAGINATE_DIFF_VAL)


class ArcSearchViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='brian')
        user.set_password('1234')
        user.save()

        for arc in range(PAGINATE_TEST_VAL):
            Arc.objects.create(
                name='Arc %s' % arc,
                slug='arc-%s' % arc,
                cvid=arc)

    def setUp(self):
        self.client.login(username='brian', password='1234')

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/arc/search/page1/')
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('arc:search', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('arc:search', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comics/arc_list.html')

    def test_pagination_is_thirty(self):
        resp = self.client.get('/arc/search/page1/?q=ar')
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['arc_list']) == PAGINATE_DEFAULT_VAL)

    def test_lists_all_teams(self):
        resp = self.client.get('/arc/search/page2/?p=ar')
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['arc_list']) == PAGINATE_DIFF_VAL)
