"""
This module defines a class that fetchs Registration info from
enrollware and inserts that data into the db
"""

from django.db.utils import IntegrityError

from apps.ewatch.models import Class, Registration, UpdateCheckRegistration

from apps.ewatch.condition.condition_registration_fetch \
        import ConditionRegistrationFetch
from apps.ewatch.fetch.fetchregistration import FetchRegistration

class UpdateRegistration():
    """A class for updating registration objects in db"""

    def __init__(self, class_id, reg_id):
        """Instantiate with enrollware registration id"""
        self.class_ = Class.objects.get_or_create(
                enrollware_id=int(class_id))[0]
    
        self.reg = Registration.objects.get_or_create(
                enrollware_id = int(reg_id))[0]
        if not self.reg.class_pk:
            self.reg.class_pk = self.class_
            self.reg.save()
        self.fetch = FetchRegistration().fetch_registration(class_id, reg_id)
        self.conditioner = ConditionRegistrationFetch()
        
    def insert_details(self, details):
        """Take a dictionary of details and save them to Registration"""
        for det in details.items():
            if det[0] == 'cert_type':
                self.reg.cert_type = det[1]
            if det[0] == 'first_name':
                self.reg.first_name = det[1]
            if det[0] == 'last_name':
                self.reg.last_name = det[1]
            if det[0] == 'email_address':
                self.reg.email_address = det[1]
            if det[0] == 'primary_phone':
                self.reg.primary_phone = det[1]
            if det[0] == 'alternate_phone':
                self.reg.alternate_phone = det[1]
            if det[0] == 'mailing':
                self.reg.mailing_address = det[1]
            if det[0] == 'billing':
                self.reg.billing_address = det[1]
            if det[0] == 'promo_code':
                self.reg.promo_code = det[1]
            if det[0] == 'book':
                self.reg.book = det[1]
            if det[0] == 'book_pickup_date':
                self.reg.book_pickup_date = det[1]
            if det[0] == 'total_charge':
                self.reg.total_charge = det[1]
            if det[0] == 'hear':
                self.reg.hear = det[1]
            if det[0] == 'return_client':
                self.reg.return_client = det[1]
            if det[0] == 'comments':
                self.reg.comments = det[1]
            if det[0] == 'codes':
                self.reg.codes = det[1]
            if det[0] == 'status':
                self.reg.status = det[1]
            if det[0] == 'checked_in':
                self.reg.checked_in = det[1]
            if det[0] == 'test_score':
                self.reg.test_score = det[1]
            if det[0] == 'certficate_number':
                self.reg.certficate_number = det[1]
            if det[0] == 'remediation_scheduled':
                self.reg.remediation_scheduled = det[1]
        self.reg.save()

    def update(self):
        """Retrun updated Registration object"""
        d = self.conditioner.registration_details(self.fetch)
        self.insert_details(d)
        UpdateCheckRegistration.objects.create(registration_pk=self.reg)
        return self.reg
