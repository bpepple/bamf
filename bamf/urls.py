from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from comics.urls import (
    arc as arc_urls,
    character as character_urls,
    creator as creator_urls,
    importer as importer_urls,
    issue as issue_urls,
    publisher as publisher_urls,
    series as series_urls,
    server_settings as settings_urls,
    team as team_urls,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='series:list',
                                  permanent=False)),
    path('', include(arc_urls)),
    path('', include(character_urls)),
    path('', include(creator_urls)),
    path('', include(importer_urls)),
    path('', include(issue_urls)),
    path('', include(publisher_urls)),
    path('', include(series_urls)),
    path('', include(settings_urls)),
    path('', include(team_urls)),
]
