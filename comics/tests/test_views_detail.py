from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from comics.models import (Publisher, Series, Creator,
                           Character, Team, Arc, Issue)


HTML_OK_CODE = 200


class TestCaseBase(TestCase):

    def _create_user(self):
        user = User.objects.create(username='brian')
        user.set_password('1234')
        user.save()

        return user

    def _client_login(self):
        self.client.login(username='brian', password='1234')


class IssueDetailViewTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        cls._create_user(cls)

        issue_date = timezone.now().date()
        mod_time = timezone.now()

        publisher = Publisher.objects.create(
            name='DC Comics', slug='dc-comics')

        series = Series.objects.create(
            cvid='1234', name='Batman', slug='batman', publisher=publisher)

        cls.issue = Issue.objects.create(cvid='4321', cvurl='http://2.com', slug='batman-1',
                                         file='/home/b.cbz', mod_ts=mod_time, date=issue_date, number='1', series=series)

    def setUp(self):
        self._client_login()

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


class PublisherDetailViewTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        cls._create_user(cls)

        cls.publisher = Publisher.objects.create(
            name='DC Comics',
            slug='dc-comics')

    def setUp(self):
        self._client_login()

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


class SeriesDetailViewTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        cls._create_user(cls)

        pub = Publisher.objects.create(name='DC Comics', slug='dc-comics',)

        cls.series = Series.objects.create(
            publisher=pub, name='Superman', slug='superman', cvid=1234,)

    def setUp(self):
        self._client_login()

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


class CreatorDetailViewTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        cls._create_user(cls)

        cls.creator = Creator.objects.create(
            name='Jack Kirby', slug='jack-kirby', cvid=4321)

    def setUp(self):
        self._client_login()

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


class CharacterDetailViewTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        cls._create_user(cls)

        cls.character = Character.objects.create(
            name='Captain America', slug='captain-america', cvid=1234)

    def setUp(self):
        self._client_login()

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


class TeamDetailViewTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        cls._create_user(cls)

        cls.team = Team.objects.create(
            name='The Fantastic Four', slug='the-fantastic-four', cvid=4444)

    def setUp(self):
        self._client_login()

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


class ArcDetailViewTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        cls._create_user(cls)

        cls.arc = Arc.objects.create(
            name='Death of Superman', slug='death-of-superman', cvid=4444)

    def setUp(self):
        self._client_login()

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
