from django.db import models


class Trefwoord(models.Model):
    naam = models.CharField(max_length=100)
    type = models.CharField(max_length=24)

    class Meta:
        verbose_name_plural = "Trefwoorden"

    def __str__(self):
        return self.naam


class Letter(models.Model):
    letter = models.CharField(max_length=1)
    description = models.CharField(max_length=100)

    def __str__(self):
        output = f"{self.letter} - {self.description}"
        return output


class AppellantType(models.Model):
    type = models.CharField(max_length=32)

    def __str__(self):
        return self.type


sample_ids = [287,
 302,
 33,
 223,
 310,
 6386,
 6270,
 5776,
 5825,
 5981,
 2253,
 1876,
 1944,
 1804,
 1835,
 2940,
 2880,
 2434,
 2650,
 2349,
 5477,
 4916,
 5044,
 5647,
 5589,
 14827,
 14265,
 14746,
 15492,
 14347,
 413,
 687,
 511,
 800,
 705,
 20768,
 20810,
 20859,
 20888,
 21017,
 16562,
 16183,
 15737,
 15601,
 15933,
 13528,
 14019,
 14026,
 13750,
 13449,
 17829,
 18625,
 18134,
 18811,
 18788,
 20477,
 19833,
 20162,
 20397,
 20681,
 1196,
 1004,
 988,
 1324,
 1231,
 4269,
 4596,
 4142,
 4092,
 4156,
 17625,
 17501,
 17742,
 16844,
 16762,
 12570,
 11245,
 11770,
 11123,
 12588,
 3783,
 3048,
 3319,
 3037,
 3780,
 7208,
 6996,
 7104,
 6753,
 6763,
 10158,
 9631,
 9889,
 10372,
 10741,
 19062,
 19413,
 19209,
 18953,
 18849,
 9179,
 9027,
 8844,
 8041,
 8665]



class UitspraakManager(models.Manager):
    def get_queryset(self):
        # return super().get_queryset()
        # return super().get_queryset().exclude(id__in=ids_list + new_ids)
        return super().get_queryset().filter(id__in=sample_ids)

    def get_trefwoorden(self):
        return Trefwoord.objects.filter(uitspraak__in=self.get_queryset()).distinct()

    def get_oordelen(self):
        return self.get_queryset().values_list("oordeel", flat=True).order_by().distinct()

    def get_labels(self):
        label_choices = dict(Uitspraak.label_choices)
        label_values = self.get_queryset().values_list("label", flat=True).order_by().distinct()
        label_dict = {label: label_choices.get(label) for label in label_values if label in label_choices}
        return label_dict

    def get_letters(self):
        return Letter.objects.filter(uitspraak__in=self.get_queryset()).distinct()

    def get_appellant_types(self):
        return AppellantType.objects.filter(uitspraak__in=self.get_queryset()).distinct()


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
    beslissing = models.TextField(default="")
    trefwoorden = models.ManyToManyField(Trefwoord)
    oordeel = models.IntegerField(default=0)
    uitleg = models.CharField(max_length=250, default="")
    plaats = models.CharField(max_length=100, default="")
    provincie = models.CharField(max_length=100, default="")
    label = models.CharField(max_length=3, choices=label_choices, default="NEW")
    appellant = models.CharField(max_length=250, default="")
    appellant_types = models.ManyToManyField(AppellantType)
    counterpart = models.CharField(max_length=250, default="")
    letters = models.ManyToManyField(Letter)

    objects = UitspraakManager()

    class Meta:
        verbose_name_plural = "Uitspraken"

