from django.urls import path, include
from rest_framework import routers

from comics.views import IssueListViewSet


router = routers.DefaultRouter()
router.register('', IssueListViewSet)

app_name = 'router'
urlpatterns = [
    path('comiclist/', include(router.urls)),
]
