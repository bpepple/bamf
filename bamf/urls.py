from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.documentation import include_docs_urls

from comics.urls import (
    arc as arc_urls,
    character as character_urls,
    creator as creator_urls,
    importer as importer_urls,
    issue as issue_urls,
    publisher as publisher_urls,
    router as router_urls,
    series as series_urls,
    server_settings as settings_urls,
    team as team_urls,
)


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='Bamf API')),
    path('', RedirectView.as_view(url='/series/page1',
                                  permanent=False)),
    path('arc/', include(arc_urls)),
    path('character/', include(character_urls)),
    path('creator/', include(creator_urls)),
    path('importer/', include(importer_urls)),
    path('', include(issue_urls)),
    path('publisher/', include(publisher_urls)),
    path('api/', include(router_urls)),
    path('series/', include(series_urls)),
    path('server-settings/', include(settings_urls)),
    path('team/', include(team_urls)),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
