from django.contrib import admin
from django import forms
from .models import Uitspraak, Trefwoord, Letter
from django.urls import reverse
from django.utils.html import format_html


class UitspraakAdminForm(forms.ModelForm):
    trefwoorden = forms.ModelMultipleChoiceField(
        queryset=Trefwoord.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Trefwoorden",
    )

    class Meta:

        model = Uitspraak
        fields = "__all__"


@admin.register(Uitspraak)
class UitsprakenAdmin(admin.ModelAdmin):
    list_display = ("uitspraak_link",)
    # fields = '__ALL__'
    # form = UitspraakAdminForm
    # change_form_template = 'admin/uitspraak_change_form.html'

    def uitspraak_link(self, obj):
        change_url = reverse('admin:uitspraken_uitspraak_change', args=[obj.id])
        return format_html('<a href="{}" target="_blank">{}</a>', change_url, obj.titel)

    uitspraak_link.short_description = 'Uitspraak'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['next_prev_links'] = self.get_next_prev_links(object_id)
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def get_next_prev_links(self, object_id):
        queryset = self.get_queryset(request=None)
        object_ids = list(queryset.values_list('id', flat=True))
        try:
            current_index = object_ids.index(int(object_id))
        except ValueError:
            return None
        else:
            next_object_id = object_ids[current_index + 1] if current_index < len(object_ids) - 1 else None
            prev_object_id = object_ids[current_index - 1] if current_index > 0 else None
            next_url = reverse('admin:uitspraken_uitspraak_change', args=[next_object_id]) if next_object_id else None
            prev_url = reverse('admin:uitspraken_uitspraak_change', args=[prev_object_id]) if prev_object_id else None
            return {
                'next_url': next_url,
                'prev_url': prev_url
            }



@admin.register(Trefwoord)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ["naam", "type"]


@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ["letter", "description"]
