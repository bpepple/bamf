from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from comics.models import (Publisher, Series, Creator,
                           Character, Team, Arc, Issue)


HTML_OK_CODE = 200


class IssueDetailViewTest(TestCase):

    def setUp(self):
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


class PublisherDetailViewTest(TestCase):

    def setUp(self):
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


class SeriesDetailViewTest(TestCase):

    def setUp(self):
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


class CreatorDetailViewTest(TestCase):

    def setUp(self):
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


class CharacterDetailViewTest(TestCase):

    def setUp(self):
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


class TeamDetailViewTest(TestCase):

    def setUp(self):
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


class ArcDetailViewTest(TestCase):

    def setUp(self):
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
