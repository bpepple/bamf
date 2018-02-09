from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

from comics.views.publisher import PublisherDetail, PublisherList, SearchPublisherList


app_name = 'publisher'
urlpatterns = [
    path('page<int:page>/', PublisherList.as_view(), name='list'),
    path('<slug:slug>/', PublisherDetail.as_view(), name='detail'),
    re_path(r'^search/(?:page(?P<page>\d+)/)?$',
            SearchPublisherList.as_view(), name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
