from django.contrib import admin
from apps.ewatch.models import *

class AddressAdmin(admin.ModelAdmin):
    pass

class LocationAdmin(admin.ModelAdmin):
    pass

class InstructorAdmin(admin.ModelAdmin):
    pass

class ClassAdmin(admin.ModelAdmin):
    date_hierarchy = 'time'
    list_display = ('enrollware_id', 'course', 'time', 'location')
    search_fields = ('enrollware_id',)

class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        'enrollware_id', 
        'class_pk', 
        'primary_phone_area_code', 
        'email_domain')
    search_fields = ('enrollware_id',)

class UpdateCheckClassAdmin(admin.ModelAdmin):
    date_hierarchy = 'time'
    list_display = ('class_pk', 'time', 'exception')
    search_fields = ('class_pk',)

class UpdateCheckRegistrationAdmin(admin.ModelAdmin):
    date_hierarchy = 'time'
    list_display = ('registration_pk', 'time')
    search_fields = ('registration_pk',)

admin.site.register(Address)
admin.site.register(Location)
admin.site.register(Instructor)
admin.site.register(Class, ClassAdmin)
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(UpdateCheckClass, UpdateCheckClassAdmin)
admin.site.register(UpdateCheckRegistration, UpdateCheckRegistrationAdmin)
