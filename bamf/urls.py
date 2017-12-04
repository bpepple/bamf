from django.contrib import admin
from django.urls import path, include

from comics.urls import series as series_urls

from .views import redirect_root


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_root),
    path('', include(series_urls)),
]
