from django.contrib import admin
from .models import UsuarioAsignado


@admin.register(UsuarioAsignado)
class UsuarioAsignadoAdmin(admin.ModelAdmin):
    list_display = [
        'identificacion', 'nombres', 'apellidos', 
        'cargo', 'departamento', 'activo', 'fecha_creacion'
    ]
    list_filter = ['activo', 'departamento']
    search_fields = [
        'nombres', 'apellidos', 'identificacion', 
        'email', 'cargo', 'departamento'
    ]
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombres', 'apellidos', 'identificacion')
        }),
        ('Información de Contacto', {
            'fields': ('email', 'telefono')
        }),
        ('Información Laboral', {
            'fields': ('cargo', 'departamento', 'activo')
        }),
        ('Información de Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
