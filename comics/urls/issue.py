from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

from comics.views.issue import (IssueList, IssueDetail, reader,
                                update_issue_status, SearchIssueList)


app_name = 'issue'
urlpatterns = [
    path('issue/', IssueList.as_view(), name='list'),
    path('issue/<slug:slug>/', IssueDetail.as_view(), name='detail'),
    path('issue/<slug:slug>/reader/', reader, name='reader'),
    path('issue/<slug:slug>/update-status/',
         update_issue_status, name='update_issue_status'),
    re_path(r'^issue/search/?$', SearchIssueList.as_view(), name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
