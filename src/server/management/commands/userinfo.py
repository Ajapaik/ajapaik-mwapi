from django.core.management.base import BaseCommand, CommandError
import json
from webservice.models import User
from webservice.mediawiki import get_mediawiki_whoami, get_mediawiki_client

class Command(BaseCommand):
    help = 'Print wikimedia userinfo of first user'

    def handle(self, *args, **options):

        users = User.objects.all()
        for user in users:
            print(str(user))
            client= get_mediawiki_client(user.id);
            r=get_mediawiki_whoami(client)
            print(r.json())

