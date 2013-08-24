from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from apps.ewatch.models import Registration, Address

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
        for reg in Registration.objects.all():
            ma = reg.mailing_address.__str__()
            ba = reg.billing_address.__str__()

            for address in Address.objects.all():
                if address.__str__() == ma:
                    reg.mailing_address = address
                    if options['verbose']:
                        self.stdout.write('Registration %s mailing_address assigned to Address %s' % (reg, address))
                    break

            for address in Address.objects.all():
                if address.__str__() == ba:
                    reg.billing_address = address
                    if options['verbose']:
                        self.stdout.write('Registration %s billing_address assigned to Address %s' % (reg, address))
            reg.save()

        address_list = []
        for address in Address.objects.all():
            if address.__str__() in address_list:
                print('Deleteing ', address)
                address.delete()
            else:
                address_list.append(address.__str__())