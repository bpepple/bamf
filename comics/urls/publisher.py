from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

from comics.views import PublisherDetail, PublisherList, SearchPublisherList


app_name = 'publisher'
urlpatterns = [
    path('publisher/', PublisherList.as_view(), name='list'),
    path('publisher/<slug:slug>/', PublisherDetail.as_view(), name='detail'),
    re_path(r'^publisher/search/?$',
            SearchPublisherList.as_view(), name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
