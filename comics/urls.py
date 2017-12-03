from django.urls import path
from . import views


app_name = 'comics'
urlpatterns = [
    path('series/', views.SeriesList.as_view(), name='comics_series_list')
]