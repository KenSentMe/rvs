from uitspraken.utils import get_letter
from uitspraken.models import Uitspraak
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Get letter in Uitspraken"

    def handle(self, *args, **options):
        counter = 0
        uitspraken = Uitspraak.objects.all()
        for uitspraak in uitspraken:
            counter += get_letter(uitspraak)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully got letters for {counter} out of {len(uitspraken)} uitspraken")
        )
