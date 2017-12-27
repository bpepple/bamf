from functools import reduce
import operator

from django.db.models import Q
from django.views.generic import ListView, DetailView

from comics.models import Arc

PAGINATE = 30


class ArcList(ListView):
    model = Arc
    paginate_by = PAGINATE


class ArcDetail(DetailView):
    model = Arc

    def get_context_data(self, **kwargs):
        context = super(ArcDetail, self).get_context_data(**kwargs)
        arc = self.get_object()
        context['issue_list'] = arc.issue_set.all(
        ).order_by('series__sort_title', 'date')
        return context


class SearchArcList(ArcList):

    def get_queryset(self):
        result = super(SearchArcList, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list)))

        return result
