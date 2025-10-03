from django.contrib import admin
from .models import Categoria, SubCategoria, Ubicacion, Activo


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']


@admin.register(SubCategoria)
class SubCategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria']
    list_filter = ['categoria']
    search_fields = ['nombre', 'categoria__nombre']
    autocomplete_fields = ['categoria']


@admin.register(Ubicacion)
class UbicacionAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']


@admin.register(Activo)
class ActivoAdmin(admin.ModelAdmin):
    list_display = [
        'codigo_inventario', 'marca', 'modelo', 
        'subcategoria', 'ubicacion', 'estado', 
        'usuario_asignado', 'fecha_creacion'
    ]
    list_filter = ['estado', 'subcategoria__categoria', 'subcategoria', 'ubicacion']
    search_fields = [
        'codigo_inventario', 'marca', 'modelo', 
        'numero_serial', 'observaciones'
    ]
    autocomplete_fields = ['subcategoria', 'ubicacion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('codigo_inventario', 'subcategoria', 'marca', 'modelo', 'numero_serial')
        }),
        ('Asignación', {
            'fields': ('usuario_asignado', 'ubicacion', 'estado')
        }),
        ('Detalles Adicionales', {
            'fields': ('observaciones',)
        }),
        ('Información de Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
