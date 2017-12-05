from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from comics.views import CreatorDetail


app_name = 'creator'
urlpatterns = [
    path('creator/<slug:slug>/', CreatorDetail.as_view(), name='detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
