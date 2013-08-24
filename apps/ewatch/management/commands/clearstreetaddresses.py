from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from apps.ewatch.models import Address

class Command(BaseCommand):
    args = ''
    help = 'Clear street addresses from all Address objects'

    option_list = BaseCommand.option_list + (
        make_option('--verbose',
            action='store_true',
            dest='verbose',
            default=False,
            help='Show conversion of email address to domain'),
        )


    def handle(self, *args, **options):
        for address in Address.objects.all():
            if address.address_1:
                address.address_1 = ''
            if address.address_2:
                address.address_2 = ''

            address.save()

            if options['verbose']:
                self.stdout.write('%s cleared' % address)