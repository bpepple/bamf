from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

from comics.views.team import TeamDetail, TeamList, SearchTeamList


app_name = 'team'
urlpatterns = [
    path('team/', TeamList.as_view(), name='list'),
    path('team/<slug:slug>/', TeamDetail.as_view(), name='detail'),
    re_path(r'^team/search/?$', SearchTeamList.as_view(), name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
