import os

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse

from comics.models import Settings
from comics.views.settings import ServerSettingsView


HTML_OK_CODE = 200


class TestCaseBase(TestCase):

    def _create_user(self):
        user = User.objects.create(username='brian')
        user.set_password('1234')
        user.save()

        return user

    def _client_login(self):
        self.client.login(username='brian', password='1234')


class TestSettingsView(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        cls.user = cls._create_user(cls)
        cls.factory = RequestFactory()

        test_data_dir = settings.BASE_DIR + os.sep + 'comics/fixtures'
        cls.settings = Settings.objects.create(comics_directory=test_data_dir,
                                               api_key='27431e6787042105bd3e47e169a624521f89f3a4')
        cls.test_key = '1234567890123456789012345678901234567890'

    def setUp(self):
        self._client_login()

    def test_settings_view(self):
        request = self.factory.get(reverse('comics:server-settings'))
        request.user = self.user
        resp = ServerSettingsView.as_view()(request)
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_settings_update(self):
        self.client.post(reverse('comics:server-settings'),
                         {'api_key': self.test_key})
        self.settings.refresh_from_db()
        self.assertEqual(self.settings.api_key, self.test_key)
