from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from comics.models import (Publisher, Series, Creator,
                           Character, Team, Arc)


HTML_OK_CODE = 200
HTML_REDIRECT_FOUND_CODE = 302
PAGINATE_TEST_VAL = 35
PAGINATE_DEFAULT_VAL = 30
PAGINATE_DIFF_VAL = (PAGINATE_TEST_VAL - PAGINATE_DEFAULT_VAL)


class PublisherListViewTest(TestCase):

    def setUp(self):
        user = User.objects.create(username='brian')
        user.set_password('1234')
        user.save()

        self.client.login(username='brian', password='1234')

        for pub_num in range(PAGINATE_TEST_VAL):
            Publisher.objects.create(
                name='Publisher %s' % pub_num,
                slug='publisher-%s' % pub_num,
                logo='images/1.jpg')

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/publisher/page1/')
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('publisher:list', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('publisher:list', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comics/publisher_list.html')

    def test_pagination_is_twenty_eight(self):
        resp = self.client.get(reverse('publisher:list', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['publisher_list']) == PAGINATE_DEFAULT_VAL)

    def test_lists_all_publishers(self):
        # Get second page and confirm it has (exactly) remaining 7 items
        resp = self.client.get(reverse('publisher:list', args=(2,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['publisher_list']) == PAGINATE_DIFF_VAL)


class SeriesListViewTest(TestCase):

    def setUp(self):
        user = User.objects.create(username='brian')
        user.set_password('1234')
        user.save()

        self.client.login(username='brian', password='1234')

        pub = Publisher.objects.create(name='Marvel', slug='marvel')

        for ser_num in range(PAGINATE_TEST_VAL):
            Series.objects.create(
                name='Series %s' % ser_num,
                slug='series-%s' % ser_num,
                publisher=pub,
                cvid=ser_num)

    def test_view_redirect(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, HTML_REDIRECT_FOUND_CODE)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/series/page1/')
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('series:list', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('series:list', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comics/series_list.html')

    def test_pagination_is_twenty_eight(self):
        resp = self.client.get(reverse('series:list', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['series_list']) == PAGINATE_DEFAULT_VAL)

    def test_lists_all_series(self):
        resp = self.client.get(reverse('series:list', args=(2,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['series_list']) == PAGINATE_DIFF_VAL)


class CreatorListViewTest(TestCase):

    def setUp(self):
        user = User.objects.create(username='brian')
        user.set_password('1234')
        user.save()

        self.client.login(username='brian', password='1234')

        for creator in range(PAGINATE_TEST_VAL):
            Creator.objects.create(
                name='Creator %s' % creator,
                slug='creator-%s' % creator,
                cvid=creator)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/creator/page1/')
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('creator:list', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('creator:list', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comics/creator_list.html')

    def test_pagination_is_twenty_eight(self):
        resp = self.client.get(reverse('creator:list', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['creator_list']) == PAGINATE_DEFAULT_VAL)

    def test_lists_all_creators(self):
        resp = self.client.get(reverse('creator:list', args=(2,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['creator_list']) == PAGINATE_DIFF_VAL)


class CharacterListViewTest(TestCase):

    def setUp(self):
        user = User.objects.create(username='brian')
        user.set_password('1234')
        user.save()

        self.client.login(username='brian', password='1234')

        for character in range(PAGINATE_TEST_VAL):
            Character.objects.create(
                name='Character %s' % character,
                slug='character-%s' % character,
                cvid=character)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/character/page1/')
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('character:list', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('character:list', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comics/character_list.html')

    def test_pagination_is_twenty_eight(self):
        resp = self.client.get(reverse('character:list', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['character_list']) == PAGINATE_DEFAULT_VAL)

    def test_lists_all_characters(self):
        resp = self.client.get(reverse('character:list', args=(2,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['character_list']) == PAGINATE_DIFF_VAL)


class TeamListViewTest(TestCase):

    def setUp(self):
        user = User.objects.create(username='brian')
        user.set_password('1234')
        user.save()

        self.client.login(username='brian', password='1234')

        for team in range(PAGINATE_TEST_VAL):
            Team.objects.create(
                name='Team %s' % team,
                slug='team-%s' % team,
                cvid=team)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/team/page1/')
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('team:list', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('team:list', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comics/team_list.html')

    def test_pagination_is_twenty_eight(self):
        resp = self.client.get(reverse('team:list', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['team_list']) == PAGINATE_DEFAULT_VAL)

    def test_lists_all_teams(self):
        resp = self.client.get(reverse('team:list', args=(2,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['team_list']) == PAGINATE_DIFF_VAL)


class ArcListViewTest(TestCase):

    def setUp(self):
        user = User.objects.create(username='brian')
        user.set_password('1234')
        user.save()

        self.client.login(username='brian', password='1234')

        for arc in range(PAGINATE_TEST_VAL):
            Arc.objects.create(
                name='Arc %s' % arc,
                slug='arc-%s' % arc,
                cvid=arc)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/arc/page1/')
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('arc:list', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('arc:list', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comics/arc_list.html')

    def test_pagination_is_twenty_eight(self):
        resp = self.client.get(reverse('arc:list', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['arc_list']) == PAGINATE_DEFAULT_VAL)

    def test_lists_all_teams(self):
        resp = self.client.get(reverse('arc:list', args=(2,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['arc_list']) == PAGINATE_DIFF_VAL)
