from django.contrib import admin

# Register your models here.
from .models import ManifiestoDoc
from .models import Manifiesto
from .models import Vehiculo

admin.site.register(ManifiestoDoc)
admin.site.register(Manifiesto)
admin.site.register(Vehiculo)
