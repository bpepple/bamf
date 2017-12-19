from django.test import TestCase

from comics.utils.utils import create_series_sortname

class UtilTest(TestCase):
    def test_create_series_sortname(self):
        sort_name = create_series_sortname('The Avengers')
        self.assertEqual('Avengers, The', sort_name)
        