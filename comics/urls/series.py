from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from ..views import SeriesList


app_name = 'comics'
urlpatterns = [
    path('series/', SeriesList.as_view(), name='serieslist')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)