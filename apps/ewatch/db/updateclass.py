"""
This module defines a class that fetchs a classes info from 
enrollware and then inserts that data into the db
"""
from django.db.utils import IntegrityError

from apps.ewatch.models import Class, Registration, UpdateCheckClass

from apps.ewatch.condition.condition_class_fetch import ConditionClassFetch
from apps.ewatch.fetch.fetchclass import FetchClass

class UpdateClass():
    """A class for updating class objects in the db"""

    def __init__(self, class_id):
        """Instantiate with a enrollware class_id"""
        self.class_ = Class.objects.get(enrollware_id=int(class_id))
        self.fetch = FetchClass().fetch_class(class_id)
        self.conditioner = ConditionClassFetch()
    
    def insert_details(self, details):
        for det in details.items():
            if det[0] == 'course':
                self.class_.course = det[1]
            if det[0] == 'registration_link':
                self.class_.registration_link = det[1]
            if det[0] == 'bulk_registration_link':
                self.class_.bulk_registration_link = det[1]
            if det[0] == 'client':
                self.class_.client = det[1]
            if det[0] == 'location':
                self.class_.location = det[1]
            if det[0] == 'instructor':
                self.class_.instructor = det[1]
            if det[0] == 'time':
                self.class_.time = det[1]
            if det[0] == 'max_students':
                self.class_.max_students = det[1]
            if det[0] == 'max_students_link':
                self.class_.max_students_link = det[1]
            if det[0] == 'listing':
                self.class_.listing = det[1]
            if det[0] == 'price':
                self.class_.price = det[1]
            if det[0] == 'book_price':
                self.class_.book_price = det[1]
            if det[0] == 'student_manikin_ratio':
                self.class_.student_manikin_ratio = det[1]
            if det[0] == 'total_hours':
                self.class_.total_hours = det[1]
        self.class_.save()
    
    def insert_registrations(self, registrations):
        for reg in registrations:
            try:
                Registration.objects.create(
                    class_pk=self.class_,
                    enrollware_id=reg[0], 
                    registration_time=reg[1])
            except IntegrityError:
                pass

    def update(self):
        d = self.conditioner.class_details(self.fetch['details'])
        self.insert_details(d)
        r = self.conditioner.class_registrations(self.fetch['registrations'])
        self.insert_registrations(r)
        UpdateCheckClass.objects.create(class_pk=self.class_)
