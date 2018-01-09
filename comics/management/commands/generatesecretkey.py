import os
import re
from shutil import copyfile

from django.core import management
from django.utils.crypto import get_random_string

import bamf


BASE_DIR = os.path.dirname(bamf.__file__)


class Command(management.BaseCommand):
    help = 'Generates a random secret key.'

    @staticmethod
    def _generate_secret_key():
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+'
        return get_random_string(50, chars)

    def handle(self, *args, **options):
        orig = os.path.join(BASE_DIR, 'settings.py')
        temp = os.path.join(BASE_DIR, 'temp.py')
        copyfile(orig, temp)

        with open(temp, 'w') as new_file:
            with open(orig) as old_file:
                for line in old_file:
                    secret_key = re.match(r'^SECRET_KEY ?=', line)
                    if secret_key:
                        line = "SECRET_KEY = '{0}'".format(
                            Command._generate_secret_key()) + '\n'
                    new_file.write(line)

        new_file.close()
        os.remove(orig)
        os.rename(temp, orig)
