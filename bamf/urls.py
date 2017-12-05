from django.contrib import admin
from django.urls import path, include

from comics.urls import (
    arc as arc_urls,
    character as character_urls,
    creator as creator_urls,
    issue as issue_urls,
    publisher as publisher_urls,
    series as series_urls,
    team as team_urls,
)

from .views import redirect_root


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_root),
    path('', include(arc_urls)),
    path('', include(character_urls)),
    path('', include(creator_urls)),
    path('', include(issue_urls)),
    path('', include(publisher_urls)),
    path('', include(series_urls)),
    path('', include(team_urls)),
]
