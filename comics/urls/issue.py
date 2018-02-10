from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from comics.views.issue import (IssueList, IssueDetail, reader,
                                update_issue_status)


app_name = 'issue'
urlpatterns = [
    path('issue/page<int:page>/', IssueList.as_view(), name='list'),
    path('issue/<slug:slug>/', IssueDetail.as_view(), name='detail'),
    path('issue/<slug:slug>/reader/', reader, name='reader'),
    path('issue/<slug:slug>/update-status/',
         update_issue_status, name='update_issue_status'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
