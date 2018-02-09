from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

from comics.views.character import CharacterDetail, CharacterList, SearchCharacterList


app_name = 'character'
urlpatterns = [
    path('page<int:page>/', CharacterList.as_view(), name='list'),
    path('<slug:slug>/', CharacterDetail.as_view(), name='detail'),
    re_path(r'^search/(?:page(?P<page>\d+)/)?$', SearchCharacterList.as_view(), name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
