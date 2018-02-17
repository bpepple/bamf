from functools import reduce
import operator

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView, DetailView

from comics.models import Character


PAGINATE = 30


class CharacterList(LoginRequiredMixin, ListView):
    model = Character
    paginate_by = PAGINATE


class CharacterDetail(LoginRequiredMixin, DetailView):
    model = Character

    def get_context_data(self, **kwargs):
        context = super(CharacterDetail, self).get_context_data(**kwargs)
        character = self.get_object()
        context['issue_list'] = (
            character.issue_set.all()
            .select_related('series')
            .only('slug', 'thumb', 'number', 'status', 'series__name')
        )
        return context


class SearchCharacterList(CharacterList):

    def get_queryset(self):
        result = super(SearchCharacterList, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list)))

        return result
