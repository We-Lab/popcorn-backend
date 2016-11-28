import json
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

User = get_user_model()
CONF_DIR = settings.CONF_DIR
config = json.loads(open(os.path.join(CONF_DIR, 'settings_deploy.json')).read())


class Command(BaseCommand):
    def handle(self, *args, **options):
        email = config['defaultSuperuser']['email']
        password = config['defaultSuperuser']['password']
        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                email=email,
                password=password,
            )
        else:
            print('default superuser exist')
