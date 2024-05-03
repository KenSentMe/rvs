from uitspraken.models import Uitspraak
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Reset values for Uitspraken"

    def handle(self, *args, **options):
        uitspraken = Uitspraak.objects.all()
        for uitspraak in uitspraken:
            uitspraak.beslissing = ""
            uitspraak.appellant = ""
            uitspraak.counterpart = ""
            uitspraak.oordeel = 0
            uitspraak.plaats = ""
            uitspraak.provincie = ""
            uitspraak.label = "NEW"
            uitspraak.save()

        self.stdout.write(
            self.style.SUCCESS(f"Successfully reset values for {len(uitspraken)} uitspraken")
        )
