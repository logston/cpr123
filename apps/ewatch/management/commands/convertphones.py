from django.core.management.base import BaseCommand, CommandError
from apps.ewatch.models import Registration

class Command(BaseCommand):
    args = ''
    help = 'Save 10 digit phone numbers as 3 digit area codes'

    def handle(self, *args, **options):
        for reg in Registration.objects.all():
            pn = reg.primary_phone
            an = reg.alternate_phone

            if pn and not reg.primary_phone_area_code:
                reg.primary_phone_area_code = self.getac(pn)
            if an and not reg.alternate_phone_area_code:
                reg.alternate_phone_area_code = self.getac(an)

            reg.save()

    def getac(self, pn):
        if len(pn) == 10:
            return pn[:3]
        elif len(pn) == 11:
            return pn[1:4]
        else:
            return '000'