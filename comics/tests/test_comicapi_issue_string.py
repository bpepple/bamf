from django.test import SimpleTestCase

from comics.utils.comicapi.issuestring import IssueString


class TestIssueString(SimpleTestCase):

    def test_issue_string_pad(self):
        val = IssueString(int(1)).asString(pad=3)
        self.assertEqual(val, '001')

    def test_issue_float(self):
        val = IssueString('1½').asFloat()
        self.assertEqual(val, 1.5)

    def test_issue_int(self):
        val = IssueString('1').asInt()
        self.assertEqual(val, 1)

    def test_issue_float_as_int(self):
        val = IssueString('1.5').asInt()
        self.assertEqual(val, 1)

    def test_issue_string_monsters_unleashed(self):
        val = IssueString('1.MU').asString(3)
        self.assertEqual(val, '001.MU')
