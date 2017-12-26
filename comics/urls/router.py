from django.urls import path, include
from rest_framework import routers

from comics.views import IssueListViewSet


router = routers.DefaultRouter()
router.register('comiclist', IssueListViewSet)

app_name = 'api'
urlpatterns = [
    path('api/', include(router.urls)),
]
