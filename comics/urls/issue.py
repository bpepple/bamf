from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from comics.views import IssueDetail


app_name = 'issue'
urlpatterns = [
    path('issue/<slug:slug>/', IssueDetail.as_view(), name='detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
