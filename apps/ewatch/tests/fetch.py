from http.cookiejar import LWPCookieJar
from urllib.request import OpenerDirector

from django.test import TestCase
from django.test.client import RequestFactory

from apps.ewatch.fetch.fetch import Fetch

class FetchTest(TestCase):
    def setUp(self):
        # every test needs a fetch object
        self.fetch = Fetch()
        self.factory = RequestFactory()

    def test_fetch_init(self):
        self.assertEqual(self.fetch.origin, 'https://www.enrollware.com/')
        self.assertEqual(self.fetch.login_path, '/admin/login.aspx')
        self.assertIsInstance(self.fetch.cj, LWPCookieJar)
        self.assertIsInstance(self.fetch.opener, OpenerDirector)

    def test_make_request(self):
        req = self.factory.post(self.fetch.login_path)

