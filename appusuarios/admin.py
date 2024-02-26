from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UsuarioEcuapass

class UsuarioEcuapassAdmin (UserAdmin):
    # Customize how the UsuarioEcuapass model is displayed in the admin interface
    list_display = ('username', 'email', 'perfil', 'is_staff', 'date_joined')
    list_filter = ('perfil', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'perfil')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'perfil'),
        }),
    )


admin.site.register (UsuarioEcuapass, UsuarioEcuapassAdmin)

