from django.urls import path

from comics.views.settings import ServerSettingsView


app_name = 'comics'
urlpatterns = [
    path('', ServerSettingsView.as_view(), name='server-settings'),
]
