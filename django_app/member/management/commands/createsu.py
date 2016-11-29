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
        username = config['defaultSuperuser']['username']
        password = config['defaultSuperuser']['password']
        email = config['defaultSuperuser']['email']
        gender = config['defaultSuperuser']['gender']
        date_of_birth = config['defaultSuperuser']['date_of_birth']
        phone_number = config['defaultSuperuser']['phone_number']
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                password=password,
                email=email,
                gender=gender,
                date_of_birth=date_of_birth,
                phone_number=phone_number,
            )
        else:
            print('default superuser exist')
