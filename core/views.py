from django.shortcuts import render
from django.views.generic import TemplateView
from activos.models import Activo


class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener estadísticas
        context['total_activos'] = Activo.objects.count()
        context['activos_mantenimiento'] = Activo.objects.filter(estado='EM').count()
        context['total_reportes'] = 0  # Por ahora en 0, se actualizará cuando se implemente reportes
        
        return context
