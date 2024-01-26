from django.urls import path

from . import views
app_name = "manifiesto"

urlpatterns = [
    path("", views.ManifiestoView.as_view(), name="manifiesto"),
    path('opciones-vehiculo/', views.VehiculoOptionsView.as_view(), name='opciones-vehiculo'),
]
