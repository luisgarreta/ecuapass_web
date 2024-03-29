from django.contrib import admin

# Register your models here.
from .models_CartaporteDoc import Cartaporte, CartaporteDoc
from .models_ManifiestoDoc import Manifiesto, ManifiestoDoc
from .models_DeclaracionDoc import Declaracion, DeclaracionDoc
from .models_Entidades import Empresa, Conductor, Vehiculo

#admin.site.register(Empresa)
#admin.site.register(Conductor)
admin.site.register(Vehiculo)
#admin.site.register(Cartaporte)
#admin.site.register(Manifiesto)

# Define the admin class
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'id', 'direccion', 'ciudad', 'pais')

# Register the admin class with the associated model
admin.site.register(Empresa, EmpresaAdmin)

class ConductorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'documento', 'nacionalidad', 'licencia')

# Register the admin class with the associated model
admin.site.register(Conductor, ConductorAdmin)

class ManifiestosInline(admin.TabularInline):
    model = Manifiesto

class CartaporteAdmin(admin.ModelAdmin):
    list_display = ('numero', 'remitente', 'documento', 'fecha_emision')
    inlines = [ManifiestosInline]

admin.site.register(Cartaporte, CartaporteAdmin)

class ManifiestoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'vehiculo', 'cartaporte', 'fecha_emision')

admin.site.register(Manifiesto, ManifiestoAdmin)

class DeclaracionAdmin(admin.ModelAdmin):
    list_display = ('numero', 'cartaporte', 'fecha_emision')

admin.site.register(Declaracion, DeclaracionAdmin)

