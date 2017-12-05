from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from comics.views import ArcDetail


app_name = 'arc'
urlpatterns = [
    path('arc/<slug:slug>/', ArcDetail.as_view(), name='detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
