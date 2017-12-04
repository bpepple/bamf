from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


app_name = 'comics'
urlpatterns = [
    path('series/', views.SeriesList.as_view(), name='comics_series_list')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)