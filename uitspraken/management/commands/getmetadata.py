from uitspraken.utils import get_metadata
from uitspraken.models import Uitspraak
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Get metadata in Uitspraken"

    def handle(self, *args, **options):
        uitspraken = Uitspraak.objects.all()
        for uitspraak in uitspraken:
            get_metadata(uitspraak)

        self.stdout.write(
            self.style.SUCCESS("Finished collecting metadata")
        )