from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    # Reporte general de activos
    path('activos/', views.generar_reporte_activos, name='reporte-activos'),
    
    # Nota de entrega
    path('nota-entrega/', views.generar_nota_entrega, name='nota-entrega'),
    
]
