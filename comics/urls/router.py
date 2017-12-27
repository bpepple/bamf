from django.urls import path, include
from rest_framework import routers

from comics.views import ComicViewSet, PublisherViewSet


router = routers.DefaultRouter()
router.register('comic', ComicViewSet)
router.register('publisher', PublisherViewSet)

app_name = 'api'
urlpatterns = [
    path('api/', include(router.urls)),
]
