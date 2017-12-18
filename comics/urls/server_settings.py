from django.urls import path

from comics.views import ServerSettingsView


app_name = 'comics'
urlpatterns = [
    path('server-settings/', ServerSettingsView.as_view(), name='server-settings'),
]
