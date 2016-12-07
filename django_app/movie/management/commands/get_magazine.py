from django.core.management import BaseCommand
from apis.magazine_search import magazine_search


class Command(BaseCommand):
    def handle(self, *args, **options):
        magazine_search()