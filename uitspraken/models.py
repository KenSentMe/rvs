from django.db import models


class Trefwoord(models.Model):
    naam = models.CharField(max_length=100)
    type = models.CharField(max_length=24)

    class Meta:
        verbose_name_plural = "Trefwoorden"

    def __str__(self):
        return self.naam


class UitspraakManager(models.Manager):
    def get_queryset(self):
        exclude_trefwoorden_id = [9, 8, 6, 17, 31, 41, 42, 38, 45, 3, 16, 21, 26, 27, 28, 32, 39, 43, 47]
        return super().get_queryset().exclude(trefwoorden__id__in=exclude_trefwoorden_id).order_by("id")[0:250]

    def get_trefwoorden(self):
        return Trefwoord.objects.filter(uitspraak__in=self.get_queryset()).distinct()



class Uitspraak(models.Model):

    label_choices = [
        ("NEW", "Nieuw"),
        ("TRU", "Goed"),
        ("FAL", "Fout"),
        ("UNK", "Weet niet")
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
    appellant = models.CharField(max_length=250, default="")
    counterpart = models.CharField(max_length=250, default="")

    objects = UitspraakManager()

    class Meta:
        verbose_name_plural = "Uitspraken"

