from django.urls import path

from .DocManifiesto_Views import DocManifiestoView, VehiculoOptionsView, ConductorOptionsView
from .DocCartaporte_Views import DocCartaporteView, EmpresaOptionsView

from . import views

app_name = "docs"

urlpatterns = [
    path("", views.index, name="index"),
    path("manifiesto/", DocManifiestoView.as_view(), name="manifiesto"),
    path("cartaporte/", DocCartaporteView.as_view(), name="cartaporte"),
    path('manifiesto/opciones-vehiculo/', VehiculoOptionsView.as_view(), name='opciones-vehiculo'),
    path('manifiesto/opciones-conductor/', ConductorOptionsView.as_view(), name='opciones-conductor'),
    path('cartaporte/opciones-empresa/', EmpresaOptionsView.as_view(), name='opciones-empresa'),
]
