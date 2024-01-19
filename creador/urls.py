from django.urls import path

from . import views

app_name = "creador"

#------- Custom templates -------
urlpatterns = [
    path("", views.index, name="index"),
    path("cartaporte/", views.CartaporteView.as_view(), name="cartaporte"),
    path('opciones-empresa/', views.EmpresaOptionsView.as_view(), name='opciones-empresa'),
]

