from django.urls import path
from . import views

app_name = 'mantenimientos'

urlpatterns = [
    # Lista de mantenimientos
    path('', views.MantenimientoListView.as_view(), name='mantenimiento-list'),
    
    # Crear mantenimiento
    path('nuevo/', views.MantenimientoCreateView.as_view(), name='mantenimiento-create'),
    
    # Detalle de mantenimiento
    path('<int:pk>/', views.MantenimientoDetailView.as_view(), name='mantenimiento-detail'),
    
    # Actualizar mantenimiento
    path('<int:pk>/editar/', views.MantenimientoUpdateView.as_view(), name='mantenimiento-update'),
    
    # Finalizar mantenimiento
    path('<int:pk>/finalizar/', views.finalizar_mantenimiento, name='mantenimiento-finalizar'),
]
