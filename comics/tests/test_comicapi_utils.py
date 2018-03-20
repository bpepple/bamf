from django.test import SimpleTestCase

from comics.utils.comicapi.utils import removearticles


class TestUtils(SimpleTestCase):

    def test_remove_articles(self):
        txt = 'The Champions & Inhumans'
        new_txt = removearticles(txt)
        self.assertEqual(new_txt, 'champions inhumans')
