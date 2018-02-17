from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from comics.models import (Publisher, Series, Creator,
                           Character, Team, Arc, Issue)


HTML_OK_CODE = 200


class IssueDetailViewTest(TestCase):

    def setUp(self):
        user = User.objects.create(username='brian')
        user.set_password('1234')
        user.save()

        self.client.login(username='brian', password='1234')

        issue_date = timezone.now().date()
        mod_time = timezone.now()
        publisher = Publisher.objects.create(
            name='DC Comics', slug='dc-comics')
        series = Series.objects.create(
            cvid='1234', name='Batman', slug='batman', publisher=publisher)
        self.issue = Issue.objects.create(cvid='4321', cvurl='http://2.com', slug='batman-1',
                                          file='/home/b.cbz', mod_ts=mod_time, date=issue_date, number='1', series=series)

    def test_view_url_accessible_by_name(self):
        url = reverse('issue:detail', args=(self.issue.slug,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        url = reverse('issue:detail', args=(self.issue.slug,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comics/issue_detail.html')

    def test_redirects_to_login_page_on_not_loggedin(self):
        self.client.logout()
        resp = self.client.get(
            reverse('issue:detail', args=(self.issue.slug,)))
        self.assertRedirects(resp, '/accounts/login/?next=/issue/batman-1/')


class PublisherDetailViewTest(TestCase):

    def setUp(self):
        user = User.objects.create(username='brian')
        user.set_password('1234')
        user.save()

        self.client.login(username='brian', password='1234')

        self.publisher = Publisher.objects.create(
            name='DC Comics',
            slug='dc-comics')

    def test_view_url_accessible_by_name(self):
        url = reverse('publisher:detail', args=(self.publisher.slug,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        url = reverse('publisher:detail', args=(self.publisher.slug,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comics/publisher_detail.html')

    def test_redirects_to_login_page_on_not_loggedin(self):
        self.client.logout()
        resp = self.client.get(
            reverse('publisher:detail', args=(self.publisher.slug,)))
        self.assertRedirects(
            resp, '/accounts/login/?next=/publisher/dc-comics/')


class SeriesDetailViewTest(TestCase):

    def setUp(self):
        user = User.objects.create(username='brian')
        user.set_password('1234')
        user.save()

        self.client.login(username='brian', password='1234')

        pub = Publisher.objects.create(name='DC Comics', slug='dc-comics',)

        self.series = Series.objects.create(
            publisher=pub, name='Superman', slug='superman', cvid=1234,)

    def test_view_url_accessible_by_name(self):
        url = reverse('series:detail', args=(self.series.slug,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        url = reverse('series:detail', args=(self.series.slug,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comics/series_detail.html')

    def test_redirects_to_login_page_on_not_loggedin(self):
        self.client.logout()
        resp = self.client.get(
            reverse('series:detail', args=(self.series.slug,)))
        self.assertRedirects(resp, '/accounts/login/?next=/series/superman/')


class CreatorDetailViewTest(TestCase):

    def setUp(self):
        user = User.objects.create(username='brian')
        user.set_password('1234')
        user.save()

        self.client.login(username='brian', password='1234')

        self.creator = Creator.objects.create(
            name='Jack Kirby', slug='jack-kirby', cvid=4321)

    def test_view_url_accessible_by_name(self):
        url = reverse('creator:detail', args=(self.creator.slug,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        url = reverse('creator:detail', args=(self.creator.slug,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comics/creator_detail.html')

    def test_redirects_to_login_page_on_not_loggedin(self):
        self.client.logout()
        resp = self.client.get(
            reverse('creator:detail', args=(self.creator.slug,)))
        self.assertRedirects(
            resp, '/accounts/login/?next=/creator/jack-kirby/')


class CharacterDetailViewTest(TestCase):

    def setUp(self):
        user = User.objects.create(username='brian')
        user.set_password('1234')
        user.save()

        self.client.login(username='brian', password='1234')

        self.character = Character.objects.create(
            name='Captain America', slug='captain-america', cvid=1234)

    def test_view_url_accessible_by_name(self):
        url = reverse('character:detail', args=(self.character.slug,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        url = reverse('character:detail', args=(self.character.slug,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comics/character_detail.html')

    def test_redirects_to_login_page_on_not_loggedin(self):
        self.client.logout()
        resp = self.client.get(
            reverse('character:detail', args=(self.character.slug,)))
        self.assertRedirects(
            resp, '/accounts/login/?next=/character/captain-america/')


class TeamDetailViewTest(TestCase):

    def setUp(self):
        user = User.objects.create(username='brian')
        user.set_password('1234')
        user.save()

        self.client.login(username='brian', password='1234')

        self.team = Team.objects.create(
            name='The Fantastic Four', slug='the-fantastic-four', cvid=4444)

    def test_view_url_accessible_by_name(self):
        url = reverse('team:detail', args=(self.team.slug,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        url = reverse('team:detail', args=(self.team.slug,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comics/team_detail.html')

    def test_redirects_to_login_page_on_not_loggedin(self):
        self.client.logout()
        resp = self.client.get(reverse('team:detail', args=(self.team.slug,)))
        self.assertRedirects(
            resp, '/accounts/login/?next=/team/the-fantastic-four/')


class ArcDetailViewTest(TestCase):

    def setUp(self):
        user = User.objects.create(username='brian')
        user.set_password('1234')
        user.save()

        self.client.login(username='brian', password='1234')

        self.arc = Arc.objects.create(
            name='Death of Superman', slug='death-of-superman', cvid=4444)

    def test_view_url_accessible_by_name(self):
        url = reverse('arc:detail', args=(self.arc.slug,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        url = reverse('arc:detail', args=(self.arc.slug,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comics/arc_detail.html')

    def test_redirects_to_login_page_on_not_loggedin(self):
        self.client.logout()
        resp = self.client.get(reverse('arc:detail', args=(self.arc.slug,)))
        self.assertRedirects(
            resp, '/accounts/login/?next=/arc/death-of-superman/')
