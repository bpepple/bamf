from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

from comics.views import CreatorDetail, CreatorList, SearchCreatorList


app_name = 'creator'
urlpatterns = [
    path('creator/', CreatorList.as_view(), name='list'),
    path('creator/<slug:slug>/', CreatorDetail.as_view(), name='detail'),
    re_path(r'^creator/search/?$', SearchCreatorList.as_view(), name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
