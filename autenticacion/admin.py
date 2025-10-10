from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Rol, PasswordResetToken, Sesion


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion', 'created_at')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('created_at',)
    ordering = ('nombre',)
    list_per_page = 25


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = (
        'id', 'username', 'email', 'nombres', 'apellidos', 
        'rol', 'estado', 'is_active', 'last_login'
    )
    search_fields = ('username', 'email', 'nombres', 'apellidos', 'rol__nombre')
    list_filter = ('estado', 'rol', 'is_active', 'created_at')
    ordering = ('username',)
    list_select_related = ('rol',)
    list_per_page = 25
    autocomplete_fields = ('rol',)

    fieldsets = UserAdmin.fieldsets + (
        ('Información Personal', {
            'fields': ('nombres', 'apellidos', 'telefono', 'area_unidad'),
        }),
        ('Configuración del Sistema', {
            'fields': ('rol', 'estado', 'ultimo_acceso', 'observaciones'),
        }),
    )


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'token', 'expira_en', 'usado', 'created_at')
    search_fields = ('usuario__username', 'usuario__email', 'token')
    list_filter = ('usado', 'created_at')
    ordering = ('-created_at',)
    list_select_related = ('usuario',)
    readonly_fields = ('token', 'created_at')
    list_per_page = 25


@admin.register(Sesion)
class SesionAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'ip_address', 'ultimo_actividad', 'expira_en', 'created_at')
    search_fields = ('usuario__username', 'usuario__email', 'ip_address')
    list_filter = ('created_at', 'ultimo_actividad')
    ordering = ('-ultimo_actividad',)
    list_select_related = ('usuario',)
    readonly_fields = ('token_sesion', 'created_at')
    list_per_page = 25
