from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import UpdateView

from comics.models import Settings


class ServerSettingsView(LoginRequiredMixin, UpdateView):
    model = Settings
    fields = '__all__'
    template_name = 'comics/server_settings.html'

    def get_object(self, *args, **kwargs):
        return Settings.get_solo()

    def form_valid(self, form):
        self.object = form.save()
        return render(self.request, 'comics/server-settings-success.html', {'server-settings': self.object})
