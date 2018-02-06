from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

from comics.views.creator import CreatorDetail, CreatorList, SearchCreatorList


app_name = 'creator'
urlpatterns = [
    path('', CreatorList.as_view(), name='list'),
    path('<slug:slug>/', CreatorDetail.as_view(), name='detail'),
    re_path(r'^search/?$', SearchCreatorList.as_view(), name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
