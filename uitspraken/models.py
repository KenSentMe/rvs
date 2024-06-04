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


class UitspraakManager(models.Manager):
    def get_queryset(self):
        exclude_trefwoorden_id = [9, 8, 6, 17, 31, 41, 42, 38, 45, 3, 16, 21, 26, 27, 28, 32, 39, 43, 47]
        return super().get_queryset().exclude(trefwoorden__id__in=exclude_trefwoorden_id).filter(datum__year=2022).order_by("id")

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

