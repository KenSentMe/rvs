from uitspraken.utils import get_final_verdict
from uitspraken.models import Uitspraak
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Get final verdict in Uitspraken"

    def handle(self, *args, **options):
        counter = 0
        uitspraken = Uitspraak.objects.all()
        for uitspraak in uitspraken:
            if not uitspraak.oordeel:
                print(f"Getting final verdict for {uitspraak.id}")
                counter += get_final_verdict(uitspraak)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully got verdicts for {counter} out of {len(uitspraken)} uitspraken")
        )
