from django.contrib import admin
from .models import Mantenimiento


@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):
    """Configuración del admin para Mantenimiento"""
    
    list_display = ['activo', 'tecnico', 'fecha', 'costo', 'estado', 'fecha_creacion']
    list_filter = ['estado', 'fecha', 'fecha_creacion']
    search_fields = ['activo__codigo_inventario', 'tecnico', 'descripcion']
    readonly_fields = ['fecha', 'fecha_creacion', 'fecha_actualizacion']
    date_hierarchy = 'fecha'
    
    fieldsets = (
        ('Información del Activo', {
            'fields': ('activo',)
        }),
        ('Datos del Técnico', {
            'fields': ('tecnico', 'telefono')
        }),
        ('Detalles del Mantenimiento', {
            'fields': ('descripcion', 'costo', 'estado')
        }),
        ('Información de Registro', {
            'fields': ('fecha', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Hacer el activo readonly si ya existe el mantenimiento"""
        if obj:  # Si estamos editando
            return self.readonly_fields + ['activo']
        return self.readonly_fields