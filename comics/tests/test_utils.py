from django.test import SimpleTestCase

from comics.utils.utils import create_series_sortname


class UtilTest(SimpleTestCase):

    def test_create_series_sortname(self):
        sort_name = create_series_sortname('The Avengers')
        self.assertEqual('Avengers, The', sort_name)
