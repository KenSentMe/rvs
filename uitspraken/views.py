from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.db.models import Count


from django.shortcuts import render, get_object_or_404

from .models import Uitspraak
from .forms import LabelForm
from .scraper import scrape_and_populate_database


@method_decorator(login_required, name='dispatch')
class IndexView(generic.ListView):
    template_name = "uitspraken/index.html"
    context_object_name = "uitspraken"
    paginate_by = 25

    def get_queryset(self):
        queryset = Uitspraak.objects.all()
        labels = self.request.GET.getlist('label')
        if labels:
            queryset = queryset.filter(label__in=labels)
        oordelen = self.request.GET.getlist('oordeel')
        if oordelen:
            queryset = queryset.filter(oordeel__in=oordelen)
        trefwoorden = self.request.GET.getlist('proceduresoort') + self.request.GET.getlist('rechtsgebied')
        if trefwoorden:
            queryset = queryset.filter(trefwoorden__id__in=trefwoorden).distinct().annotate(
                num_trefwoorden=Count('trefwoorden')).filter(num_trefwoorden=len(trefwoorden))
            return queryset
        letters = self.request.GET.getlist('letter')
        if letters:
            queryset = queryset.filter(letters__letter__in=letters)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        trefwoorden = Uitspraak.objects.get_trefwoorden()
        oordelen = Uitspraak.objects.get_oordelen()
        labels = Uitspraak.objects.get_labels()
        letters = Uitspraak.objects.get_letters()
        context['page_obj'] = page_obj
        context['all_trefwoorden'] = trefwoorden
        context['proceduresoort_trefwoorden'] = trefwoorden.filter(type="proceduresoort")
        context['rechtsgebied_trefwoorden'] = trefwoorden.filter(type="rechtsgebied")
        context['selected_proceduresoort'] = self.request.GET.getlist('proceduresoort')
        context['selected_rechtsgebied'] = self.request.GET.getlist('rechtsgebied')
        context['all_oordelen'] = oordelen
        context['selected_oordelen'] = self.request.GET.getlist('oordeel')
        context['all_labels'] = labels
        context['selected_labels'] = self.request.GET.getlist('label')
        context['all_letters'] = letters
        context['selected_letters'] = self.request.GET.getlist('letter')

        return context


@method_decorator(login_required, name='dispatch')
class UitspraakView(generic.DetailView):
    model = Uitspraak
    template_name = "uitspraken/uitspraak.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        labels = self.request.GET.getlist('label')
        if labels and labels != ['']:
            queryset = queryset.filter(label__in=labels)
        oordelen = self.request.GET.getlist('oordeel')
        if oordelen and oordelen != ['']:
            queryset = queryset.filter(oordeel__in=oordelen)

        trefwoorden = self.request.GET.getlist('trefwoord')

        if trefwoorden:
            queryset = queryset.filter(trefwoorden__in=trefwoorden)
        letters = self.request.GET.getlist('letter')
        if letters:
            queryset = queryset.filter(letters__letter__in=letters)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uitspraak = context['uitspraak']
        queryset = self.get_queryset()
        previous_uitspraak = queryset.filter(id__lt=uitspraak.id).last()
        next_uitspraak = queryset.filter(id__gt=uitspraak.id).first()
        context['previous_uitspraak'] = previous_uitspraak
        context['next_uitspraak'] = next_uitspraak
        context['query_string'] = self.request.META['QUERY_STRING']
        return context


@login_required()
def scraper_view(request):
    if request.method == "POST":
        rows = int(request.POST.get('rows'))
        start_year = int(request.POST.get('start_year'))
        end_year = int(request.POST.get('end_year'))
        facet = int(request.POST.get('facet'))
        output = scrape_and_populate_database(rows, list(range(start_year, end_year + 1)), facet)
        context = {'output': output}
        return render(request, 'uitspraken/scraper.html', context)
    else:
        return render(request, 'uitspraken/scraper.html')


def update_label(request, pk):
    instance = get_object_or_404(Uitspraak, pk=pk)

    if request.method == 'POST':
        form = LabelForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
    else:
        form = LabelForm(instance=instance)

    context = {'form': form}
    return render(request, 'uitspraken/uitspraak.html', context)

