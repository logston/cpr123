import json
import os

from django.test import TestCase
from django.test.client import RequestFactory

from apps.ewatch.models import ZipGeocode
from libs.api.google_geocode import fetch_json_from_google_api
from libs.api.google_geocode import fetch_new_zc
from libs.api.google_geocode import get_dict_from_json
from libs.api.google_geocode import get_lat_long
from libs.api.google_geocode import get_lat_long_from_dict
from libs.utils.validators import is_valid_zip

class ValidZipCodeTest(TestCase):
    def test__zip_non_numeric(self):
        self.assertFalse(is_valid_zip('1fe12'))

    def test__zip_too_long(self):
        self.assertFalse(is_valid_zip('2332'))

    def test__valid_zip(self):
        self.assertTrue(is_valid_zip('11232'))

class GoogleGeocodeAPITest(TestCase):

    api_repsonse = fetch_json_from_google_api(11232)
    path = os.path.abspath(os.path.dirname(__file__))
    valid_json = os.path.join(
        path, 
        '../../../libs/api/test_google_geocode_zip_11232.json')
    with open(valid_json, 'rb') as fp:
        valid_bytecode = fp.read()

    def test__valid_JSON_from_request(self):
        self.assertEqual(self.valid_bytecode, self.api_repsonse)

    def test__get_dict_from_json(self):
        c = get_dict_from_json(self.valid_bytecode)
        t = get_dict_from_json(self.api_repsonse)
        self.assertEqual(c, t)

    def test__api_resonse_is_okay(self):
        d = get_dict_from_json(self.api_repsonse)
        self.assertEqual(d['status'], 'OK')
        self.assertEqual(d['results'][0]['formatted_address'], 
                         'Brooklyn, NY 11232, USA')

    def test__lat_response_is_correct(self):
        d = get_dict_from_json(self.api_repsonse)
        self.assertEqual(d['results'][0]['geometry']['location']['lat'], 
                         40.6560436)

    def test__lng_response_is_correct(self):
        d = get_dict_from_json(self.api_repsonse)
        self.assertEqual(d['results'][0]['geometry']['location']['lng'],
                         -74.0079781)

    def test__get_lat_long_from_dict(self):
        d = get_dict_from_json(self.api_repsonse)
        ll = get_lat_long_from_dict(d)
        self.assertEqual(ll['lat'], 40.6560436)
        self.assertEqual(ll['lng'], -74.0079781)

    def test__fetch_new_zc(self):
        zc = '11232'
        zgc = ZipGeocode.objects.get_or_none(zip_code=zc)
        self.assertIsNone(zgc)
        d = get_dict_from_json(self.api_repsonse)
        ll = get_lat_long_from_dict(d)
        ZipGeocode.objects.create(zip_code=zc,
                                  latitude=ll['lat'],
                                  longitude=ll['lng'])
        self.assertIsNone(ZipGeocode.objects.get_or_none(zip_code='94547'))
        self.assertIsNotNone(ZipGeocode.objects.get_or_none(zip_code=zc))












