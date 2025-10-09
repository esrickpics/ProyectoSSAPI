# Sistema de Manejo de Errores - SSAPI

## 📋 Descripción General

El sistema implementa un manejo completo de errores que incluye:
- **Vistas personalizadas** para errores 400, 403, 404 y 500
- **Middleware de captura de errores** para prevenir caídas del sistema
- **Logging detallado** de todos los errores
- **Headers de seguridad** para proteger la aplicación
- **Páginas de error responsivas** con diseño profesional

## 🔧 Componentes Implementados

### 1. Vistas de Manejo de Errores
- **`custom_404_view`**: Página no encontrada
- **`custom_500_view`**: Error interno del servidor
- **`custom_403_view`**: Acceso denegado
- **`custom_400_view`**: Solicitud incorrecta

### 2. Middleware Personalizado
- **`ErrorHandlingMiddleware`**: Captura errores no manejados
- **`SecurityHeadersMiddleware`**: Agrega headers de seguridad

### 3. Templates de Error
- **`error_404.html`**: Diseño profesional para página no encontrada
- **`error_500.html`**: Página de error del servidor con ID único
- **`error_403.html`**: Página de acceso denegado
- **`error_400.html`**: Página de solicitud incorrecta

## 🚀 Cómo Activar el Sistema

### 1. Configuración Automática
El sistema ya está configurado automáticamente en:
- **`SSAPI/settings.py`**: Handlers de error configurados
- **`core/middleware.py`**: Middleware implementado
- **`core/views.py`**: Vistas de error creadas

### 2. Verificar Configuración
```python
# En SSAPI/settings.py
handler404 = 'core.views.custom_404_view'
handler500 = 'core.views.custom_500_view'
handler403 = 'core.views.custom_403_view'
handler400 = 'core.views.custom_400_view'

# Middleware activado
MIDDLEWARE = [
    # ... otros middleware
    'core.middleware.ErrorHandlingMiddleware',
    'core.middleware.SecurityHeadersMiddleware',
]
```

## 🧪 Cómo Probar las Vistas de Error

### URLs de Prueba Disponibles

#### 1. Error 404 - Página No Encontrada
```
http://127.0.0.1:8000/test/404/
```
- **Qué hace**: Simula una página no encontrada
- **Resultado**: Muestra la página de error 404 personalizada

#### 2. Error 500 - Error del Servidor
```
http://127.0.0.1:8000/test/500/
```
- **Qué hace**: Fuerza un error interno del servidor
- **Resultado**: Muestra la página de error 500 con ID único

#### 3. Error 403 - Acceso Denegado
```
http://127.0.0.1:8000/test/403/
```
- **Qué hace**: Simula un error de permisos
- **Resultado**: Muestra la página de error 403

#### 4. Error 400 - Solicitud Incorrecta
```
http://127.0.0.1:8000/test/400/
```
- **Qué hace**: Simula una solicitud mal formada
- **Resultado**: Muestra la página de error 400

### Pruebas Adicionales

#### Probar Error 404 Natural
```
http://127.0.0.1:8000/pagina-que-no-existe/
```
- Accede a cualquier URL que no exista
- Debería mostrar la página 404 personalizada

#### Probar en Modo Producción
1. **Cambiar DEBUG a False** en `settings.py`:
   ```python
   DEBUG = False
   ```

2. **Reiniciar el servidor**:
   ```bash
   python manage.py runserver
   ```

3. **Probar las URLs de error** - ahora mostrarán las páginas personalizadas

## 📊 Logging de Errores

### Información Registrada
- **Usuario**: Nombre e ID del usuario (si está autenticado)
- **Ruta**: URL donde ocurrió el error
- **Método HTTP**: GET, POST, etc.
- **IP del cliente**: Dirección IP del usuario
- **User Agent**: Información del navegador
- **Stack trace**: Detalles técnicos del error

### Ubicación de Logs
Los logs se guardan en el sistema de logging de Django. Para verlos:
```python
# En settings.py, agregar configuración de logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'error.log',
        },
    },
    'loggers': {
        'core.middleware': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

## 🔒 Características de Seguridad

### Headers de Seguridad Agregados
- **X-Frame-Options**: Previene clickjacking
- **X-Content-Type-Options**: Previene MIME type sniffing
- **X-XSS-Protection**: Habilita protección XSS
- **Referrer-Policy**: Controla información de referrer

### Información Sensible Protegida
- Los errores en producción no muestran detalles técnicos
- Los logs no incluyen información sensible del usuario
- Las páginas de error no revelan estructura interna

## 🎨 Personalización de Páginas de Error

### Modificar Diseño
1. **Editar templates** en `core/templates/core/`
2. **Cambiar colores** en los archivos CSS de cada template
3. **Agregar logos** o información específica de la empresa

### Agregar Información Adicional
```html
<!-- En error_500.html -->
<div class="error-details">
    <h6>Información del Error</h6>
    <small>
        ID del Error: <strong>{{ error_id }}</strong><br>
        Ruta: <strong>{{ path }}</strong><br>
        Hora: <strong>{% now "d/m/Y H:i:s" %}</strong>
    </small>
</div>
```

## 🚨 Solución de Problemas

### Si las páginas de error no aparecen:
1. **Verificar DEBUG**: Debe estar en `False` para ver páginas personalizadas
2. **Revisar URLs**: Asegurarse de que las URLs de prueba estén configuradas
3. **Verificar middleware**: Confirmar que el middleware esté en `MIDDLEWARE`

### Si los logs no aparecen:
1. **Configurar logging** en `settings.py`
2. **Verificar permisos** de escritura en archivos de log
3. **Revisar nivel de logging** configurado

## 📝 Notas Importantes

- **Solo en desarrollo**: Las URLs de prueba (`/test/404/`, etc.) solo deben estar activas en desarrollo
- **Producción**: En producción, remover las URLs de prueba por seguridad
- **Logs**: Monitorear regularmente los logs de error para identificar problemas
- **Backup**: Mantener backups de las páginas de error personalizadas

## 🔄 Mantenimiento

### Limpieza de Logs
```bash
# Limpiar logs antiguos (ejemplo)
find . -name "*.log" -mtime +30 -delete
```

### Monitoreo
- Revisar logs de error semanalmente
- Configurar alertas para errores críticos
- Actualizar páginas de error según necesidades del negocio
