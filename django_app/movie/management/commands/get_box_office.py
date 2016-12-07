from django.core.management import BaseCommand
from apis.box_office_search import box_office_search


class Command(BaseCommand):
    def handle(self, *args, **options):
        box_office_search()