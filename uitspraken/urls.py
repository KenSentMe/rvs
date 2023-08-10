from django.urls import path

from . import views

app_name = "uitspraken"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.UitspraakView.as_view(), name="uitspraak"),
    path("scraper/", views.scraper_view, name="scraper"),
    path('update-label/<int:pk>/', views.update_label, name='update-label'),
]