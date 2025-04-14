from uitspraken.utils import get_plaats
from uitspraken.models import Uitspraak
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Get plaats in Uitspraken"

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.NOTICE("Getting plaats for uitspraken")
        )
        counter = 0
        # Use iterator() to fetch records in batches
        for uitspraak in Uitspraak.objects.filter(
            beslissing__gt='',  # checks for non-empty string
            plaats=''
        ).iterator(chunk_size=2000):
            counter += get_plaats(uitspraak)
            if counter % 100 == 0:  # Show progress every 100 records
                self.stdout.write(
                    self.style.SUCCESS(f"Processed {counter} uitspraken, current ID: {uitspraak.id}")
                )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully got plaats for {counter} uitspraken")
        )
