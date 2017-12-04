from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

from ..views import SeriesList, SearchSeriesList


app_name = 'series'
urlpatterns = [
    path('series/', SeriesList.as_view(), name='list'),
    re_path(r'^series/search/?$', SearchSeriesList.as_view(), name='search')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)