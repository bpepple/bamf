from functools import reduce
import operator

from django.db.models import Q
from django.views.generic import ListView, DetailView

from comics.models import (Series, Issue, Character,
                           Arc, Team, Publisher,
                           Creator, Roles)


class SeriesList(ListView):
    model = Series
    paginate_by = 32


class SearchSeriesList(SeriesList):

    def get_queryset(self):
        result = super(SearchSeriesList, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list)))

        return result


class SeriesDetail(DetailView):
    model = Series


class IssueDetail(DetailView):
    model = Issue

    def get_context_data(self, **kwargs):
        context = super(IssueDetail, self).get_context_data(**kwargs)
        issue = self.get_object()
        context['roles_list'] = Roles.objects.filter(issue=issue)
        return context


class CharacterDetail(DetailView):
    model = Character

    def get_context_data(self, **kwargs):
        context = super(CharacterDetail, self).get_context_data(**kwargs)
        character = self.get_object()
        context['issue_list'] = character.issue_set.all(
        ).order_by('series__name', 'number')
        return context


class ArcDetail(DetailView):
    model = Arc

    def get_context_data(self, **kwargs):
        context = super(ArcDetail, self).get_context_data(**kwargs)
        arc = self.get_object()
        context['issue_list'] = arc.issue_set.all(
        ).order_by('series__name', 'number')
        return context


class TeamDetail(DetailView):
    model = Team

    def get_context_data(self, **kwargs):
        context = super(TeamDetail, self).get_context_data(**kwargs)
        team = self.get_object()
        context['issue_list'] = team.issue_set.all(
        ).order_by('series__name', 'number')
        return context


class PublisherDetail(DetailView):
    model = Publisher


class CreatorDetail(DetailView):
    model = Creator

    def get_context_data(self, **kwargs):
        context = super(CreatorDetail, self).get_context_data(**kwargs)
        creator = self.get_object()
        roles = Roles.objects.filter(creator=creator)
        context['issue_list'] = Issue.objects.filter(
            id__in=roles.values('issue_id'))
        return context
