from functools import reduce
import operator

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView


from comics.models import Issue, Roles
from comics.utils.reader import ImageAPIHandler


PAGINATE = 30

LIMIT_RESULTS = PAGINATE * 3


class IssueList(ListView):
    model = Issue
    paginate_by = PAGINATE
    queryset = Issue.objects.order_by('-import_date')[:LIMIT_RESULTS]


class IssueDetail(DetailView):
    model = Issue

    def get_context_data(self, **kwargs):
        context = super(IssueDetail, self).get_context_data(**kwargs)
        issue = self.get_object()
        context['roles_list'] = Roles.objects.filter(issue=issue)
        return context


class SearchIssueList(IssueList):

    def get_queryset(self):
        result = super(SearchIssueList, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list)))

        return result


def reader(request, slug):
    issue = get_object_or_404(Issue, slug=slug)

    uri_list = []
    for page in range(issue.page_count):
        i = ImageAPIHandler()
        data_uri = i.get_uri(slug, page)
        uri_list.append(data_uri)

    return render(request, 'comics/reader.html', {'issue': issue, 'data_uri': uri_list})


def update_issue_status(request, slug):
    issue = Issue.objects.get(slug=slug)

    if request.GET.get('complete', '') == '1':
        issue.leaf = 1
        issue.status = 2
        issue.save()
    else:
        issue.leaf = int(request.GET.get('leaf', ''))
        issue.status = 1
        issue.save()

    data = {'saved': 1}

    return JsonResponse(data)
