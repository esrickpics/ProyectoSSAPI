from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from activos.models import Activo, Categoria, Ubicacion
from django.db.models import Count
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseServerError, HttpResponseNotFound
import logging

logger = logging.getLogger(__name__)


class HomeView(LoginRequiredMixin, TemplateView):
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


class LoginView(DjangoLoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('core:home')


@login_required
def signout(request):
    logout(request)
    return redirect('core:login')


# ============== VISTAS DE MANEJO DE ERRORES ==============

def custom_404_view(request, exception):
    """Vista personalizada para error 404"""
    logger.warning(f"Error 404: {request.path} - Usuario: {request.user if request.user.is_authenticated else 'Anónimo'}")
    return render(request, 'core/error_404.html', status=404)


def custom_500_view(request):
    """Vista personalizada para error 500"""
    logger.error(f"Error 500 en: {request.path} - Usuario: {request.user if request.user.is_authenticated else 'Anónimo'}")
    return render(request, 'core/error_500.html', status=500)


def custom_403_view(request, exception):
    """Vista personalizada para error 403 (Permisos denegados)"""
    logger.warning(f"Error 403: {request.path} - Usuario: {request.user if request.user.is_authenticated else 'Anónimo'}")
    return render(request, 'core/error_403.html', status=403)


def custom_400_view(request, exception):
    """Vista personalizada para error 400 (Solicitud incorrecta)"""
    logger.warning(f"Error 400: {request.path} - Usuario: {request.user if request.user.is_authenticated else 'Anónimo'}")
    return render(request, 'core/error_400.html', status=400)


# ============== VISTAS DE PRUEBA DE ERRORES ==============

def test_404_view(request):
    """Vista para probar el error 404"""
    return HttpResponseNotFound("Esta es una prueba de error 404")


def test_500_view(request):
    """Vista para probar el error 500"""
    # Forzar un error para probar el manejo de errores 500
    raise Exception("Esta es una prueba de error 500")


def test_403_view(request):
    """Vista para probar el error 403"""
    from django.core.exceptions import PermissionDenied
    raise PermissionDenied("Esta es una prueba de error 403")


def test_400_view(request):
    """Vista para probar el error 400"""
    from django.core.exceptions import BadRequest
    raise BadRequest("Esta es una prueba de error 400")
