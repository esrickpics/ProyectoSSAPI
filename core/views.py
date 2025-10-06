from django.shortcuts import render
from django.views.generic import TemplateView
from activos.models import Activo, Categoria, Ubicacion
from django.db.models import Count


class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estadísticas generales
        context['total_activos'] = Activo.objects.count()
        context['activos_mantenimiento'] = Activo.objects.filter(estado='EM').count()
        
        # Activos por categoría
        context['activos_por_categoria'] = Categoria.objects.annotate(
            total=Count('subcategorias__activos')
        ).order_by('-total')[:5]
        
        # Activos por ubicación
        context['activos_por_ubicacion'] = Ubicacion.objects.annotate(
            total=Count('activos')
        ).order_by('-total')[:5]
        
        return context
