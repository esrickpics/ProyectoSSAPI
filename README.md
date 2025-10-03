# Sistema de Gestión de Activos (SSAPI)

Sistema web desarrollado en Django para la gestión integral de activos.

## Características Principales

### App Activos
- ✅ CRUD completo de **Categorías** y **Subcategorías**
- ✅ CRUD completo de **Ubicaciones**
- ✅ CRUD completo de **Activos** con:
  - Información detallada (marca, modelo, serial, código de inventario)
  - Estado (Activo, Inactivo, En Mantenimiento)
  - Asignación a usuarios
  - Ubicación física
- ✅ **Filtros dinámicos** por categoría, subcategoría, ubicación, estado y búsqueda
- ✅ Acciones especiales:
  - Reasignar activo a otro usuario
  - Reubicar activo a otra ubicación
- ✅ Interfaz moderna con Bootstrap 5

## Instalación

### Requisitos
- Python 3.8+
- PostgreSQL (opcional, se puede usar SQLite para desarrollo)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd ProyectoSSAPI
```

2. **Crear y activar entorno virtual**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar base de datos**

**Opción A: SQLite (desarrollo)**
- Ya está configurado por defecto en `SSAPI/settings.py`

**Opción B: PostgreSQL (producción)**
1. Crear base de datos en PostgreSQL:
```sql
CREATE DATABASE PALDACADB;
```

2. En `SSAPI/settings.py`, descomentar la configuración de PostgreSQL y comentar SQLite:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'PALDACADB',
        'USER': 'postgres',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

5. **Aplicar migraciones**
```bash
python manage.py migrate
```

6. **Crear superusuario**
```bash
python manage.py createsuperuser
```

7. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

8. **Acceder a la aplicación**
- Aplicación principal: http://localhost:8000/
- Panel de administración: http://localhost:8000/admin/

## Estructura del Proyecto

```
ProyectoSSAPI/
├── SSAPI/              # Configuración principal del proyecto
├── core/               # App núcleo (dashboard, navegación)
├── activos/            # App de gestión de activos ✅
│   ├── models.py       # Modelos: Categoria, SubCategoria, Ubicacion, Activo
│   ├── views.py        # Vistas basadas en clases (CBV)
│   ├── forms.py        # Formularios
│   ├── urls.py         # Rutas
│   └── templates/      # Plantillas HTML
├── usuarios/           # App de usuarios asignados
│   └── models.py       # Modelo: UsuarioAsignado
├── mantenimientos/     # App de mantenimientos (pendiente)
├── reportes/           # App de reportes (pendiente)
└── requirements.txt    # Dependencias
```

## Modelos de Datos

### Activos App

**Categoria**
- nombre (único)

**SubCategoria**
- nombre
- categoria (FK)

**Ubicacion**
- nombre (único)

**Activo**
- codigo_inventario (único)
- subcategoria (FK)
- marca
- modelo
- numero_serial (opcional)
- usuario_asignado (FK a UsuarioAsignado, opcional)
- ubicacion (FK)
- observaciones (opcional)
- estado (Activo, Inactivo, En Mantenimiento)
- fecha_creacion
- fecha_actualizacion

### Usuarios App

**UsuarioAsignado**
- nombres
- apellidos
- identificacion (único)
- email (opcional)
- telefono (opcional)
- cargo (opcional)
- departamento (opcional)
- activo

## Uso del Sistema

### Panel de Administración
1. Acceder a http://localhost:8000/admin/
2. Iniciar sesión con el superusuario
3. Gestionar todos los modelos desde el panel

### Interfaz Principal
1. Acceder a http://localhost:8000/
2. Navegar por:
   - **Activos** → Ver listado con filtros
   - **Categorías** → Gestionar categorías
   - **Subcategorías** → Gestionar subcategorías
   - **Ubicaciones** → Gestionar ubicaciones

### Operaciones Comunes

**Crear un activo:**
1. Ir a "Activos" > "Crear Activo"
2. Completar el formulario
3. Guardar

**Filtrar activos:**
1. En la lista de activos, usar los filtros superiores
2. Seleccionar categoría, subcategoría, ubicación, estado
3. Usar la búsqueda para código, marca o modelo

**Reasignar activo:**
1. Abrir detalle del activo
2. Click en "Reasignar Activo"
3. Seleccionar nuevo usuario

**Reubicar activo:**
1. Abrir detalle del activo
2. Click en "Reubicar Activo"
3. Seleccionar nueva ubicación

## Próximos Pasos

- [ ] Desarrollar app de mantenimientos
- [ ] Desarrollar app de reportes PDF
- [ ] Implementar dashboard en app core
- [ ] Añadir gráficos y estadísticas
- [ ] Implementar historial de cambios

## Tecnologías Utilizadas

- **Backend:** Django 5.2.7
- **Frontend:** Bootstrap 5, Bootstrap Icons
- **Base de datos:** PostgreSQL / SQLite
- **Python:** 3.8+

## Licencia

Ver archivo LICENSE

---

Desarrollado para el Sistema de Gestión de Activos SSAPI
