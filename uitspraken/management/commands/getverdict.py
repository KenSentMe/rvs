from uitspraken.utils import get_final_verdict
from uitspraken.models import Uitspraak
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Get final verdict in Uitspraken"

    def handle(self, *args, **options):
        counter = 0
        uitspraken = (Uitspraak.objects
                      .filter(beslissing__isnull=False)
                      .filter(oordeel__isnull=True) | Uitspraak.objects.filter(beslissing__isnull=False).filter(oordeel=0))
        print("Get final verdict in Uitspraken")
        print(f"Found {uitspraken.count()} uitspraken")
        for uitspraak in uitspraken:
            counter += get_final_verdict(uitspraak)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully got verdicts for {counter} out of {len(uitspraken)} uitspraken")
        )
