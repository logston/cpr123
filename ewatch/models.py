from django.db import models

class Address(models.Model):
    address_1 = models.CharField(max_length=64, blank=True)
    address_2 = models.CharField(max_length=64, blank=True)
    city = models.CharField(max_length=32, blank=True)
    states = ''
    state = models.CharField(max_length=2, choices=states, default='NY')
    zip_code = models.CharField(max_length=16, blank=True)

class Location(models.Model):
    pass

class Instructor(models.Model):
    pass

class Class(models.Model):
    enrollware_id = models.PositiveIntegerField(
            unique=True, null=True, blank=True)
    course = models.CharField(max_length=128, blank=True)
    registration_link = models.URLField(blank=True)
    bulk_registration_link = models.URLField(blank=True)
    client = models.CharField(max_length=128, blank=True)
    location = models.ForeignKey(Location, null=True)
    instructor = models.ForeignKey(Instructor, null=True)
    time = models.DateTimeField(null=True, blank=True)
    max_students = models.PositiveSmallIntegerField(null=True, blank=True)
    listing = models.NullBooleanField(
            help_text='Included in the online class catalog')
    #assistants = models.  multiForeignKey(Instructor)
    #public_notes = models.TextField(null=True)
    #internal_notes = models.TextField(null=True)
    #documents = models.    multiFileField()
    price = models.PositiveSmallIntegerField(null=True, blank=True)
    book_price = models.PositiveSmallIntegerField(null=True, blank=True)
    STUDENT_MANIKIN_RATIOS = tuple((x+1, str(x+1)+':1') for x in range(8))
    student_manikin_ratio = models.PositiveSmallIntegerField(
            choices=STUDENT_MANIKIN_RATIOS,
            default=1)
    total_hours = models.PositiveSmallIntegerField(null=True)

class Registration(models.Model):
    class_pk = models.ForeignKey(Class, related_name='pk', null=True)
    reschedule_class = models.ForeignKey(Class, null=True)
    types = (('', ''), ('C', 'Certification'), ('R', 'Recertification'))
    cert_type = models.CharField(max_length=1, choices=types, default='')
    first_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=32, blank=True)
    email_address = models.EmailField(blank=True)
    primary_phone = models.CharField(max_length=16, blank=True)
    alternate_phone = models.CharField(max_length=16, blank=True)
    mailing_address = models.ForeignKey(
            Address, related_name='mailing', null=True)
    billing_address = models.ForeignKey(
            Address, related_name='billing', null=True)
    promo_code = models.CharField(max_length=16, blank=True)
    book_choices = (
            ('', ''),
            ('N','Not needed'), 
            ('P', 'Pickup'),
            ('S', 'Ship'))
    book = models.CharField(max_length=1, choices=book_choices, default='')
    book_pickup_date = models.DateField(null=True)
    total_charge = models.DecimalField(max_digits=6, decimal_places=2)
    comments = models.TextField(blank=True)
    codes = models.CharField(max_length=128, blank=True)
    status_choices = (
            ('',''),
            ('P','Pending'),
            ('C','Complete'),
            ('I','Incomplete'),
            ('R','Remediate'),
            ('N','No Show'))
    status = models.CharField(
            max_length=1, choices=status_choices, default='')
    checked_in = models.NullBooleanField()
    test_score = models.CharField(max_length=8, blank=True)
    remediation_scheduled = models.ForeignKey(
            Class, related_name='remediation_scheduled', null=True)
