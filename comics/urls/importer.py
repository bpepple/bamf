from django.urls import path

from comics.views.importer import importer


app_name = 'importer'
urlpatterns = [
    path('importer/', importer, name='index'),
]
