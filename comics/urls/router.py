from django.urls import path, include
from rest_framework import routers

from comics.views import ComicViewSet, PublisherViewSet, SeriesViewSet,\
    CreatorViewSet


router = routers.DefaultRouter()
router.register('comic', ComicViewSet)
router.register('creator', CreatorViewSet)
router.register('publisher', PublisherViewSet)
router.register('series', SeriesViewSet)

app_name = 'api'
urlpatterns = [
    path('api/', include(router.urls)),
]
