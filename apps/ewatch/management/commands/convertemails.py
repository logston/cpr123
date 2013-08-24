from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from apps.ewatch.models import Registration

class Command(BaseCommand):
    args = ''
    help = 'Save email domains from email addresses'

    option_list = BaseCommand.option_list + (
        make_option('--verbose',
            action='store_true',
            dest='verbose',
            default=False,
            help='Show conversion of email address to domain'),
        )


    def handle(self, *args, **options):
        for reg in Registration.objects.all():
            e = reg.email_address
            if e:
                es = reg.email_address.split('@')
            else:
                continue

            if es[1]:
                reg.email_domain = es[1]
                reg.save()

            if options['verbose']:
                self.stdout.write('%s to %s' % (e, es[1]))