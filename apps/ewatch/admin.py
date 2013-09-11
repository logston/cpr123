from django.contrib import admin
from apps.ewatch.models import *


class ZipGeocodeAdmin(admin.ModelAdmin):
    search_fields = ('zip_code',)
    ordering = ['zip_code']
    list_display = ('zip_code', 'latitude', 'longitude')
admin.site.register(ZipGeocode, ZipGeocodeAdmin)

class AddressAdmin(admin.ModelAdmin):
    pass
admin.site.register(Address)

class LocationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Location)

class InstructorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Instructor)

class ClassAdmin(admin.ModelAdmin):
    date_hierarchy = 'time'
    list_display = ('enrollware_id', 'course', 'time', 'location')
    search_fields = ('enrollware_id',)
admin.site.register(Class, ClassAdmin)

class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        'enrollware_id', 
        'class_eid', 
        'primary_phone_area_code', 
        'email_domain')
    search_fields = ('enrollware_id',)
    raw_id_fields = ('mailing_address', 'billing_address',)

    def class_eid(self, reg):
        return '%s' % (reg.class_pk.enrollware_id)
    class_eid.short_description = 'Class Enrollware ID'
admin.site.register(Registration, RegistrationAdmin)

class UpdateCheckClassAdmin(admin.ModelAdmin):
    date_hierarchy = 'time'
    list_display = ('class_pk', 'time', 'exception')
    search_fields = ('Class__enrollware_id',)
admin.site.register(UpdateCheckClass, UpdateCheckClassAdmin)

class UpdateCheckRegistrationAdmin(admin.ModelAdmin):
    date_hierarchy = 'time'
    list_display = ('registration_pk', 'time')
    search_fields = ('registration_pk',)
admin.site.register(UpdateCheckRegistration, UpdateCheckRegistrationAdmin)






