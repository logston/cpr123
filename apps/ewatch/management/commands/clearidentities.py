from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from apps.ewatch.models import Registration

class Command(BaseCommand):
    args = ''
    help = 'Clear First and Last name plus email and phone numbers'

    option_list = BaseCommand.option_list + (
        make_option('--verbose',
            action='store_true',
            dest='verbose',
            default=False,
            help='Show conversion of email address to domain'),
        )


    def handle(self, *args, **options):
        for reg in Registration.objects.all():
            reg.first_name = ''
            reg.last_name = ''
            reg.email_address = ''
            reg.primary_phone = ''
            reg.alternate_phone = ''
            reg.save()

            if options['verbose']:
                self.stdout.write('cleared %s' % reg)