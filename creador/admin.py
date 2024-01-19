from django.contrib import admin

# Register your models here.
from .models import CartaporteDoc
from .models import Cartaporte
from .models import Empresa

admin.site.register(CartaporteDoc)
admin.site.register(Cartaporte)
admin.site.register(Empresa)
