from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from comics.views import CharacterDetail


app_name = 'character'
urlpatterns = [
    path('character/<slug:slug>/', CharacterDetail.as_view(), name='detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
