from uitspraken.utils import get_appellant_type
from uitspraken.models import Uitspraak
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Get appellant type in Uitspraken"

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.NOTICE("Getting appellant type for uitspraken")
        )
        counter = 0
        # Use iterator() to fetch records in batches
        for uitspraak in Uitspraak.objects.filter(
            beslissing__gt='',  # checks for non-empty string
            appellant_type=None
        ).iterator(chunk_size=2000):
            counter += get_appellant_type(uitspraak)
            if counter % 100 == 0:  # Show progress every 100 records
                self.stdout.write(
                    self.style.SUCCESS(f"Processed {counter} uitspraken, current ID: {uitspraak.id}")
                )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully got appellant type for {counter} uitspraken")
        )
