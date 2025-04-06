from uitspraken.utils import get_beslissing
from uitspraken.models import Uitspraak
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Get beslissing in Uitspraken"

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.NOTICE("Getting beslissingen for uitspraken")
        )
        counter = 0
        uitspraken = Uitspraak.objects.filter(beslissing='')
        total = uitspraken.count()
        for uitspraak in uitspraken:
            if not uitspraak.beslissing:
                counter += get_beslissing(uitspraak)
                self.stdout.write(
                    self.style.SUCCESS(f"{counter}/{total}: Successfully got beslissing for {uitspraak.id}")
                )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully got beslissingen for {counter} out of {total} uitspraken")
        )
