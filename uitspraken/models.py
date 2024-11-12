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


ids_list = [131,
            89,
            277,
            201,
            139,
            168,
            329,
            261,
            143,
            157,
            6543,
            6256,
            6052,
            5749,
            6243,
            6020,
            5823,
            6233,
            5940,
            6395,
            2179,
            2056,
            2156,
            2122,
            2057,
            1769,
            2107,
            2247,
            1689,
            1922,
            2666,
            2452,
            2579,
            2551,
            2931,
            2476,
            2930,
            2694,
            2307,
            2299,
            5214,
            5251,
            4864,
            5569,
            5349,
            4935,
            4825,
            5137,
            5535,
            5157,
            15430,
            15193,
            15456,
            14743,
            15130,
            15074,
            14358,
            14629,
            14242,
            15112,
            366,
            834,
            788,
            696,
            603,
            445,
            671,
            583,
            441,
            484,
            20898,
            20783,
            21016,
            20977,
            20905,
            20770,
            21110,
            20994,
            21038,
            20776,
            15645,
            16535,
            15574,
            16161,
            16292,
            16487,
            15540,
            15828,
            15941,
            15590,
            13668,
            13437,
            13198,
            13113,
            14146,
            13921,
            14139,
            13670,
            12827,
            13193,
            18147,
            17971,
            18464,
            18694,
            17992,
            17899,
            18445,
            18607,
            18116,
            18611,
            20350,
            20177,
            20510,
            20568,
            19872,
            20571,
            19979,
            19810,
            19842,
            20607,
            1313,
            1346,
            1269,
            1305,
            1234,
            1349,
            1326,
            1047,
            1559,
            1279,
            4064,
            4099,
            4195,
            4713,
            4412,
            4396,
            4026,
            4267,
            4581,
            3969,
            16945,
            17748,
            17694,
            17265,
            17310,
            17372,
            17247,
            17332,
            17030,
            16988,
            11579,
            12094,
            11265,
            11187,
            11945,
            11291,
            12174,
            11482,
            11118,
            11614,
            3627,
            3421,
            3743,
            3295,
            3093,
            3251,
            3412,
            2986,
            3727,
            3109,
            7007,
            7449,
            7277,
            7602,
            6695,
            6917,
            7553,
            7138,
            6574,
            7550,
            9733,
            10450,
            10395,
            9709,
            9836,
            10156,
            11000,
            10761,
            10833,
            10890,
            19386,
            19459,
            19341,
            19036,
            19446,
            19345,
            18830,
            18838,
            19180,
            19319,
            8782,
            8498,
            8293,
            8755,
            8254,
            8560,
            9165,
            9099,
            7931,
            8080]


class UitspraakManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(id__in=ids_list)

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

