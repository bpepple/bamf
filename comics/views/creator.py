from functools import reduce
import operator

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView, DetailView

from comics.models import Creator, Roles, Issue


PAGINATE = 30


class CreatorList(LoginRequiredMixin, ListView):
    model = Creator
    paginate_by = PAGINATE


class CreatorDetail(LoginRequiredMixin, DetailView):
    model = Creator

    def get_context_data(self, **kwargs):
        context = super(CreatorDetail, self).get_context_data(**kwargs)
        creator = self.get_object()
        roles = Roles.objects.filter(creator=creator)
        context['issue_list'] = (
            Issue.objects.filter(id__in=roles.values('issue_id'))
            .select_related('series')
            .only('slug', 'cover', 'number', 'status', 'series__name')
        )
        return context


class SearchCreatorList(CreatorList):

    def get_queryset(self):
        result = super(SearchCreatorList, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list)))

        return result
