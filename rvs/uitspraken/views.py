from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.db.models import Count

from .models import Uitspraak, Trefwoord


@method_decorator(login_required, name='dispatch')
class IndexView(generic.ListView):
    template_name = "uitspraken/index.html"
    context_object_name = "uitspraken"
    paginate_by = 10

    def get_queryset(self):
        queryset = Uitspraak.objects.all().order_by("id")
        trefwoorden = self.request.GET.getlist('trefwoord')
        if trefwoorden:
            queryset = queryset.filter(trefwoorden__id__in=trefwoorden).distinct().annotate(
                num_trefwoorden=Count('trefwoorden')).filter(num_trefwoorden=len(trefwoorden))
            return queryset
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['all_trefwoorden'] = Trefwoord.objects.all()
        context['selected_trefwoorden'] = self.request.GET.getlist('trefwoord')
        return context


@method_decorator(login_required, name='dispatch')
class UitspraakView(generic.DetailView):
    model = Uitspraak
    template_name = "uitspraken/uitspraak.html"
