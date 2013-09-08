from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from apps.ewatch.models import ZipGeocode, Address
from libs.utils.validators import is_valid_zip as is_valid_zip

class Command(BaseCommand):
    args = ''
    help = 'Pull a new ZipGeocode form Google'

    option_list = BaseCommand.option_list + (
        make_option('--verbose',
            action='store_true',
            dest='verbose',
            default=False,
            help=help),
        )

    def handle(self, *args, **options):
        for zc in Address.objects.values('zip_code'):
            if not zc['zip_code']:
                continue
            zc = zc['zip_code'][:5]
            if is_valid_zip(zc):
                if options['verbose']:
                    print(zc)