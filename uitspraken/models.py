from django.db import models


class Trefwoord(models.Model):
    naam = models.CharField(max_length=100)
    type = models.CharField(max_length=24)

    class Meta:
        verbose_name_plural = "Trefwoorden"

    def __str__(self):
        return self.naam


class Uitspraak(models.Model):

    label_choices = [
        ("NEW", "Nieuw"),
        ("TRU", "Goed"),
        ("FAL", "Fout")
    ]

    titel = models.CharField(max_length=100)
    ecli = models.CharField(max_length=24)
    samenvatting = models.TextField()
    datum = models.DateField()
    link = models.URLField()
    inhoud = models.TextField()
    trefwoorden = models.ManyToManyField(Trefwoord)
    oordeel = models.IntegerField(default=0)
    uitleg = models.CharField(max_length=250, default="")
    plaats = models.CharField(max_length=100, default="")
    provincie = models.CharField(max_length=100, default="")
    label = models.CharField(max_length=3, choices=label_choices, default="NEW")

    class Meta:
        verbose_name_plural = "Uitspraken"

