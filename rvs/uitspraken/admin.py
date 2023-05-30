from django.contrib import admin
from .models import Uitspraak, Trefwoord


@admin.register(Uitspraak)
class UitsprakenAdmin(admin.ModelAdmin):
    pass


@admin.register(Trefwoord)
class KeywordAdmin(admin.ModelAdmin):
    pass
