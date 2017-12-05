from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from comics.views import PublisherDetail


app_name = 'publisher'
urlpatterns = [
    path('publisher/<slug:slug>/', PublisherDetail.as_view(), name='detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
