from django.db import models


class Trefwoord(models.Model):
    name = models.CharField(max_length=100)
    type = models.IntegerField()

    class Meta:
        verbose_name_plural = "Trefwoorden"


class Uitspraak(models.Model):
    titel = models.CharField(max_length=24)
    ecli = models.CharField(max_length=24)
    samenvatting = models.TextField()
    datum = models.DateField()
    link = models.URLField()
    inhoud = models.TextField()
    trefwoorden = models.ManyToManyField(Trefwoord)

    class Meta:
        verbose_name_plural = "Uitspraken"

