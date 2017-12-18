from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

from comics.views import ArcDetail, ArcList, SearchArcList


app_name = 'arc'
urlpatterns = [
    path('arc/', ArcList.as_view(), name='list'),
    path('arc/<slug:slug>/', ArcDetail.as_view(), name='detail'),
    re_path(r'^arc/search/?$', SearchArcList.as_view(), name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
