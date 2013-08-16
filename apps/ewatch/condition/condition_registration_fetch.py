"""
This modules defines a class that conditions a Registration
fetch from enrollware for insertion into the db
"""
from datetime import date
from decimal import *
import re

from apps.ewatch.models import Address, Class

class ConditionRegistrationFetch():
    """
    A class with a number of methods for conditioning fetched
    registration data from enrollware for the db
    """

    def __init__(self):
        pass

    def _get_class_from_enrollware_id(self, class_id):
        """Return a Class object based on id"""
        return Class.objects.get_or_create(enrollware_id=int(class_id))

    def _condition_phone_number(self, pn):
        """Return a phone number of the format 1234567890"""
        ret_pn = ''
        for c in pn:
            if c.isdigit() or (c == 'x' or c == 'x'):
                ret_pn += c
        return ret_pn

    def _condition_address(self, a_dict):
        """Return an Address object based on a_dict"""
        a1 = a_dict['address_1'] if 'address_1' in a_dict else ''
        a2 = a_dict['address_2'] if 'address_2' in a_dict else ''
        c = a_dict['city'] if 'city' in a_dict else ''
        s = a_dict['state'] if 'state' in a_dict else 'NY'
        z = a_dict['zip'] if 'zip' in a_dict else ''
        return Address.objects.get_or_create(
                address_1=a1,
                address_2=a2,
                city=c,
                state=s,
                zip_code=z)[0]

    def _parse_date(self, date_str):
        """Return a Date object parsed from date_str"""
        patt = re.compile('(\d+)/(\d+)/(\d{4})')
        r = re.match(patt, date_str)
        return date(int(r.group(3)), int(r.group(1)), int(r.group(2)))

    def registration_details(self, din):
        """Return a db ready dictionary of registration details"""
        dout = {}
        if 'reschedule_class' in din and din['reschedule_class'] and \
                int(din['reschedule_class']):
            dout['reschedule_class'] = \
                    self._get_class_from_enrollware_id(din['reschedule_class'])
        if 'cert_type' in din:
            dout['cert_type'] = din['cert_type']
        if 'first_name' in din:
            dout['first_name'] = din['first_name']
        if 'last_name' in din:
            dout['last_name'] = din['last_name']
        if 'email_address' in din:
            dout['email_address'] = din['email_address']
        if 'primary_phone' in din:
            dout['primary_phone'] = \
                    self._condition_phone_number(din['primary_phone'])
        if 'alternate_phone' in din:
            dout['alternate_phone'] = \
                    self._condition_phone_number(din['alternate_phone'])
        if 'mailing' in din and din['mailing']:
            dout['mailing'] = self._condition_address(din['mailing'])
        if 'billing' in din and din['billing']:
            dout['billing'] = self._condition_address(din['billing'])
        if 'promo_code' in din:
            dout['promo_code'] = din['promo_code']
        if 'book' in din:
            dout['book'] = din['book'][0]
        if 'book_pickup_date' in din:
            dout['book_pickup_date'] = \
                    self._parse_date(din['book_pickup_date'])
        if 'total_charge' in din:
            dout['total_charge'] = Decimal(din['total_charge'].strip('$'))
        if 'hear' in din:
            dout['hear'] = din['hear']
        if 'return_client' in din and 'Yes' in din['return_client']:
            dout['return_client'] = True
        else:
            dout['return_client'] = False
        if 'comments' in din:
            dout['comments'] = din['comments']
        if 'codes' in din:
            dout['codes'] = din['codes']
        if 'status' in din:
            dout['status'] = din['status'][0]
        if 'checked_in' in din:
            dout['checked_in'] = din['checked_in']
        if 'test_score' in din:
            dout['test_score'] = din['test_score']
        if 'certificate_number' in din:
            dout['certificate_number'] = din['certificate_number']
        if 'remediation_scheduled' in din and din['remediation_scheduled'] and\
                int(din['remediation_scheduled']):
            dout['remediation_scheduled'] = \
                    self._get_class_from_enrollware_id(
                            din['remediation_scheduled'])
        return dout
