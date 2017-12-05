from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from comics.views import TeamDetail


app_name = 'team'
urlpatterns = [
    path('team/<slug:slug>/', TeamDetail.as_view(), name='detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
