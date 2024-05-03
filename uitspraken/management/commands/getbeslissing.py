from uitspraken.utils import get_beslissing
from uitspraken.models import Uitspraak
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Get beslissing in Uitspraken"

    def handle(self, *args, **options):
        counter = 0
        uitspraken = Uitspraak.objects.all()
        for uitspraak in uitspraken:
            if not uitspraak.beslissing:
                counter += get_beslissing(uitspraak)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully got beslissingen for {counter} out of {len(uitspraken)} uitspraken")
        )
