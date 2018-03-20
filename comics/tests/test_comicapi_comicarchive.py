import os

from django.conf import settings
from django.test import SimpleTestCase

from comics.utils.comicapi.comicarchive import ComicArchive

TEST_DATA = settings.BASE_DIR + os.sep + \
    'comics/fixtures/Captain Atom #078 (1965).cbz'


class TestComicArchive(SimpleTestCase):

    def test_if_zipfile(self):
        ca = ComicArchive(TEST_DATA)
        z = ca.isZip()
        self.assertTrue(z)

    def test_if_folder(self):
        ca = ComicArchive(TEST_DATA)
        z = ca.isFolder()
        self.assertFalse(z)

    def test_if_writable(self):
        ca = ComicArchive(TEST_DATA)
        z = ca.isWritable()
        self.assertTrue(z)

    def test_seems_to_be_comic_archive_zip(self):
        ca = ComicArchive(TEST_DATA)
        z = ca.seemsToBeAComicArchive()
        self.assertTrue(z)

    def test_get_number_of_pages_zip(self):
        ca = ComicArchive(TEST_DATA)
        z = ca.getNumberOfPages()
        self.assertEqual(z, 24)

    def test_cix_has_cbi(self):
        ca = ComicArchive(TEST_DATA)
        z = ca.hasCBI()
        self.assertFalse(z)

    def test_cix_has_cix(self):
        ca = ComicArchive(TEST_DATA)
        z = ca.hasCIX()
        self.assertTrue(z)

    def test_cix_has_CoMeT(self):
        ca = ComicArchive(TEST_DATA)
        z = ca.hasCoMet()
        self.assertFalse(z)

    def test_read_cix(self):
        ca = ComicArchive(TEST_DATA)
        md = ca.readCIX()
        self.assertIsNotNone(md)
