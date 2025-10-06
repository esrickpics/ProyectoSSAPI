from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Vista principal con buscador
    path('', views.UsuarioSearchView.as_view(), name='usuario-search'),
    
    # Perfil de usuario
    path('<int:pk>/perfil/', views.UsuarioProfileView.as_view(), name='usuario-profile'),
    
    # CRUD de usuarios
    path('crear/', views.UsuarioCreateView.as_view(), name='usuario-create'),
    path('<int:pk>/editar/', views.UsuarioUpdateView.as_view(), name='usuario-update'),
    path('<int:pk>/eliminar/', views.UsuarioDeleteView.as_view(), name='usuario-delete'),
]
