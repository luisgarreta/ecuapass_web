from django.contrib import admin

# Register your models here.
from .models import ManifiestoDoc, Manifiesto, Vehiculo, Conductor
from .models import CartaporteDoc, Cartaporte, Empresa

admin.site.register(ManifiestoDoc)
admin.site.register(Manifiesto)
admin.site.register(Vehiculo)
admin.site.register(Conductor)

admin.site.register(CartaporteDoc)
admin.site.register(Cartaporte)
admin.site.register(Empresa)
