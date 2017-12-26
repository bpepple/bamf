from django.urls import path, include
from rest_framework import routers

from comics.views import ComicViewSet


router = routers.DefaultRouter()
router.register('comic', ComicViewSet)

app_name = 'api'
urlpatterns = [
    path('api/', include(router.urls)),
]
