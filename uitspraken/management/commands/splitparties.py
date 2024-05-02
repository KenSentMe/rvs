from uitspraken.utils import split_parties
from uitspraken.models import Uitspraak
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Split parties in Uitspraken"

    def handle(self, *args, **options):
        counter = 0
        uitspraken = Uitspraak.objects.all()
        for uitspraak in uitspraken:
            if not uitspraak.appellant or not uitspraak.counterpart:
                counter += split_parties(uitspraak)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully split parties for {counter} out of {len(uitspraken)} uitspraken")
        )
