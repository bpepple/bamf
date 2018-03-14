from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView

from comics.models import Issue, Roles
from comics.utils.comicapi.comicarchive import ComicArchive
from comics.utils.reader import ImageAPIHandler


PAGINATE = 30

LIMIT_RESULTS = PAGINATE * 3


class IssueList(LoginRequiredMixin, ListView):
    model = Issue
    paginate_by = PAGINATE
    queryset = (
        Issue.objects
        .select_related('series')
        .only('series', 'number', 'slug', 'cover', 'status')
        .order_by('-import_date')[:LIMIT_RESULTS]
    )


class IssueDetail(LoginRequiredMixin, DetailView):
    model = Issue
    queryset = (
        Issue.objects
        .select_related('series', 'series__publisher')
    )

    def get_context_data(self, **kwargs):
        context = super(IssueDetail, self).get_context_data(**kwargs)
        issue = self.get_object()
        try:
            next_issue = Issue.get_next_by_date(issue, series=issue.series)
        except ObjectDoesNotExist:
            next_issue = None

        try:
            previous_issue = Issue.get_previous_by_date(
                issue, series=issue.series)
        except ObjectDoesNotExist:
            previous_issue = None

        context['roles_list'] = (
            Roles.objects.filter(issue=issue)
            .prefetch_related('role')
            .select_related('creator')
        )
        context['navigation'] = {
            'next_issue': next_issue,
            'previous_issue': previous_issue,
        }
        return context


@login_required
def reader(request, slug):
    issue = get_object_or_404(Issue, slug=slug)

    # Let's get the total number pages from the comic archive
    # instead of from the db in case the file has been modified.
    # If I ever implement a file monitor function this can be removed.
    ca = ComicArchive(issue.file)
    page_count = ca.getNumberOfPages()

    uri_list = []
    for page in range(page_count):
        i = ImageAPIHandler()
        data_uri = i.get_uri(issue.file, page)
        uri_list.append(data_uri)

    return render(request, 'comics/reader.html', {'issue': issue, 'data_uri': uri_list})


@login_required
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
