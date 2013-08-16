import re

from django.db import models

from libs.ref.us_states import us_states

# phone number regex
pnum_pattern = re.compile(r'[0-9]{10}')

def validate_pnum(pnum):
    """Raise validation error if not a 10 digit phone number"""
    if not re.match(pnum_pattern, pnum):
        raise ValidationError(u'%s is not a valid phone number'%pnum)


class Address(models.Model):
    address_1 = models.CharField(max_length=64, blank=True)
    address_2 = models.CharField(max_length=64, blank=True)
    city = models.CharField(max_length=32, blank=True)
    state_choices = us_states
    state = models.CharField(
            max_length=2, choices=state_choices, default='NY')
    zip_code = models.CharField(max_length=16, blank=True)

    def __str__(self):
        address_2 = self.address_2 if self.address_2 else ''
        return ', '.join([
                self.address_1,
                address_2,
                self.city,
                self.state,
                self.zip_code])

class Location(models.Model):
    """Model a Training Center Location"""
    name = models.CharField(max_length=32, blank=True)
    address = models.ForeignKey(Address, null=True, blank=True)

    def __str__(self):
        return self.name

class Instructor(models.Model):
    first_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=32, blank=True)
    certs = models.CharField(max_length=32, blank=True)
    address = models.ForeignKey(Address, null=True, blank=True)
    aha_instructor_id = models.CharField(max_length=16, blank=True)

    def __str__(self):
        certs = ', '+self.certs if self.certs else ''
        return self.first_name+' '+self.last_name+certs

class Class(models.Model):
    enrollware_id = models.PositiveIntegerField(
            unique=True, null=True, blank=True)
    course = models.CharField(max_length=128, blank=True)
    registration_link = models.URLField(blank=True)
    bulk_registration_link = models.URLField(blank=True)
    client = models.CharField(max_length=128, blank=True)
    location = models.ForeignKey(Location, null=True, blank=True)
    instructor = models.ForeignKey(Instructor, null=True, blank=True)
    time = models.DateTimeField(null=True, blank=True)
    max_students = models.PositiveSmallIntegerField(null=True, blank=True)
    max_students_link = models.OneToOneField('self', null=True, blank=True)
    listing = models.NullBooleanField(
            help_text='Included in the online class catalog')
    #assistants = models.  multiForeignKey(Instructor)
    #public_notes = models.TextField(null=True)
    #internal_notes = models.TextField(null=True)
    #documents = models.    multiFileField()
    price = models.DecimalField(
            max_digits=6, 
            decimal_places=2,
            null=True, 
            blank=True)
    book_price = models.DecimalField(
            max_digits=5,
            decimal_places=2,
            null=True, 
            blank=True)
    STUDENT_MANIKIN_RATIOS = tuple((x+1, str(x+1)+':1') for x in range(8))
    student_manikin_ratio = models.PositiveSmallIntegerField(
            choices=STUDENT_MANIKIN_RATIOS,
            default=1)
    total_hours = models.PositiveSmallIntegerField(null=True)
    time_added = models.DateTimeField(auto_now_add=True)
    removed = models.NullBooleanField()

    def __str__(self):
        return str(self.enrollware_id)

class Registration(models.Model):
    class_pk = models.ForeignKey(
            Class, 
            related_name='pk', 
            null=True, 
            blank=True)
    enrollware_id = models.PositiveIntegerField(
            unique=True, null=True, blank=True)
    reschedule_class = models.ForeignKey(Class, null=True, blank=True)
    types = (('', ''), ('C', 'Certification'), ('R', 'Recertification'))
    cert_type = models.CharField(
            max_length=1, 
            choices=types, 
            default='', 
            blank=True)
    first_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=32, blank=True)
    email_address = models.EmailField(blank=True)
    primary_phone = models.CharField(
            max_length=16, 
            blank=True,
            validators=[validate_pnum])
    alternate_phone = models.CharField(
            max_length=16, 
            blank=True,
            validators=[validate_pnum])
    mailing_address = models.ForeignKey(
            Address, related_name='mailing', null=True, blank=True)
    billing_address = models.ForeignKey(
            Address, related_name='billing', null=True, blank=True)
    promo_code = models.CharField(max_length=16, blank=True)
    book_choices = (
            ('', ''),
            ('N','Not needed'), 
            ('P', 'Pickup'),
            ('S', 'Ship'))
    book = models.CharField(
            max_length=1, 
            choices=book_choices, 
            default='',
            blank=True)
    book_pickup_date = models.DateField(null=True, blank=True)
    total_charge = models.DecimalField(
            max_digits=6, decimal_places=2, null=True, blank=True)
    hear = models.CharField(max_length=128, blank=True)
    return_client = models.NullBooleanField(default=False)
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
            max_length=1, 
            choices=status_choices, 
            default='',
            blank=True)
    checked_in = models.NullBooleanField()
    test_score = models.CharField(max_length=8, blank=True)
    certficate_number = models.CharField(max_length=16, blank=True)
    remediation_scheduled = models.ForeignKey(
            Class, 
            related_name='remediation_scheduled', 
            null=True,
            blank=True)
    registration_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return ' '.join([str(self.enrollware_id)])

class UpdateCheckClass(models.Model):
    class_pk = models.ForeignKey(Class, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.class_pk) + ' @ ' + str(self.time)

class UpdateCheckRegistration(models.Model):
    registration_pk = models.ForeignKey(Registration, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.registration_pk) + ' @ ' + str(self.time)
