from uitspraken.utils import get_appellant_type
from uitspraken.models import Uitspraak
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Get appellant types in Uitspraken"

    def handle(self, *args, **options):
        counter = 0
        uitspraken = Uitspraak.objects.all()
        for uitspraak in uitspraken:
            counter += get_appellant_type(uitspraak)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully got appellant types for {counter} out of {len(uitspraken)} uitspraken")
        )
