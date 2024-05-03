from uitspraken.utils import get_first_verdict
from uitspraken.models import Uitspraak
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Get first verdict in Uitspraken"

    def handle(self, *args, **options):
        counter = 0
        uitspraken = Uitspraak.objects.all()
        for uitspraak in uitspraken:
            if not uitspraak.oordeel:
                print(f"Getting first verdict for {uitspraak.id}")
                counter += get_first_verdict(uitspraak)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully got first verdicts for {counter} out of {len(uitspraken)} uitspraken")
        )
