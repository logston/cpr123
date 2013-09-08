import json
import logging
import urllib.request

from apps.ewatch.models import ZipGeocode

logger = logging.getLogger(__name__)

def fetch_json_from_google_api(zc):
    url = "http://maps.googleapis.com/maps/api/geocode/json?address="+\
        str(zc)+"&sensor=false"
    urlp = urllib.request.urlopen(url)
    return urlp.read()

def get_dict_from_json(j):
	"""Turn JSON bytecode into a python dict"""
	return json.loads(j.decode('latin-1'))

def get_lat_long_from_dict(d):
	"""Return location dict from JSON dict"""
	if not d['status'] == 'OK':
		raise ValueError
	return d['results'][0]['geometry']['location']

def fetch_new_zc(zc):
	"""Return ZipGeocode object form db after pulling data from google"""
	j = fetch_json_from_google_api(zc)
	d = get_dict_from_json(j)
	ll = get_lat_long_from_dict(d)
	return ZipGeocode.objects.create(zip_code=zc,
									 latitude=ll['lat'],
									 longitude=ll['lng'])

def get_lat_long(zc):
    # see if lat/long is in db 
    return zc
    zc_obj = ZipGeocode.objects.get_or_none(zip_code=zc)
    if not zc_obj:
        # if not, go get lat long from google
        zc_obj = fetch_new_zc(zc)

    return (zc_obj.latitude, zc_obj.longitude)
