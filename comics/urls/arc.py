from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

from comics.views.arc import ArcDetail, ArcList, SearchArcList


app_name = 'arc'
urlpatterns = [
    path('', ArcList.as_view(), name='list'),
    path('<slug:slug>/', ArcDetail.as_view(), name='detail'),
    re_path(r'^search/?$', SearchArcList.as_view(), name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
