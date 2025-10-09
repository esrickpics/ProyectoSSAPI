import logging
import traceback
from django.http import HttpResponseServerError
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class ErrorHandlingMiddleware(MiddlewareMixin):
    """
    Middleware personalizado para capturar y manejar errores de manera elegante
    """
    
    def process_exception(self, request, exception):
        """
        Captura todas las excepciones no manejadas y las registra
        """
        # Obtener información del usuario
        user_info = "Anónimo"
        if hasattr(request, 'user') and request.user.is_authenticated:
            user_info = f"{request.user.username} (ID: {request.user.id})"
        
        # Registrar el error completo
        logger.error(
            f"Error no manejado en {request.path} - "
            f"Usuario: {user_info} - "
            f"IP: {self.get_client_ip(request)} - "
            f"Error: {str(exception)}",
            exc_info=True,
            extra={
                'user': user_info,
                'path': request.path,
                'method': request.method,
                'ip': self.get_client_ip(request),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            }
        )
        
        # En modo DEBUG, dejar que Django maneje el error normalmente
        if settings.DEBUG:
            return None
        
        # En producción, mostrar una página de error personalizada
        try:
            error_html = render_to_string('core/error_500.html', {
                'error_id': id(exception),  # ID único para el error
                'path': request.path,
            })
            return HttpResponseServerError(error_html)
        except Exception as render_error:
            # Si incluso el renderizado falla, devolver un error básico
            logger.critical(f"Error crítico al renderizar página de error: {render_error}")
            return HttpResponseServerError(
                "<h1>Error del Servidor</h1>"
                "<p>Ha ocurrido un error interno. Por favor, contacte al administrador.</p>"
            )
    
    def get_client_ip(self, request):
        """
        Obtiene la IP real del cliente
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Middleware para agregar headers de seguridad
    """
    
    def process_response(self, request, response):
        # Prevenir clickjacking
        response['X-Frame-Options'] = 'DENY'
        
        # Prevenir MIME type sniffing
        response['X-Content-Type-Options'] = 'nosniff'
        
        # Habilitar XSS protection
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Referrer policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response
