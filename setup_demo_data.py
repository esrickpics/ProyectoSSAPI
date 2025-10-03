"""
Script para crear datos de demostración en el sistema
Ejecutar con: python manage.py shell < setup_demo_data.py
"""

from activos.models import Categoria, SubCategoria, Ubicacion, Activo
from usuarios.models import UsuarioAsignado

print("=== Iniciando configuración de datos de demostración ===\n")

# Limpiar datos existentes (opcional, comentar si no desea borrar)
# print("Limpiando datos existentes...")
# Activo.objects.all().delete()
# SubCategoria.objects.all().delete()
# Categoria.objects.all().delete()
# Ubicacion.objects.all().delete()
# UsuarioAsignado.objects.all().delete()

# Crear Categorías
print("Creando categorías...")
cat_informatica = Categoria.objects.get_or_create(nombre="Informática")[0]
cat_mobiliario = Categoria.objects.get_or_create(nombre="Mobiliario")[0]
cat_vehiculos = Categoria.objects.get_or_create(nombre="Vehículos")[0]
cat_herramientas = Categoria.objects.get_or_create(nombre="Herramientas")[0]
print(f"✓ {Categoria.objects.count()} categorías creadas")

# Crear SubCategorías
print("\nCreando subcategorías...")
# Informática
subcat_computadores = SubCategoria.objects.get_or_create(
    nombre="Computadores",
    categoria=cat_informatica
)[0]
subcat_impresoras = SubCategoria.objects.get_or_create(
    nombre="Impresoras",
    categoria=cat_informatica
)[0]
subcat_monitores = SubCategoria.objects.get_or_create(
    nombre="Monitores",
    categoria=cat_informatica
)[0]

# Mobiliario
subcat_escritorios = SubCategoria.objects.get_or_create(
    nombre="Escritorios",
    categoria=cat_mobiliario
)[0]
subcat_sillas = SubCategoria.objects.get_or_create(
    nombre="Sillas",
    categoria=cat_mobiliario
)[0]

# Vehículos
subcat_automoviles = SubCategoria.objects.get_or_create(
    nombre="Automóviles",
    categoria=cat_vehiculos
)[0]

print(f"✓ {SubCategoria.objects.count()} subcategorías creadas")

# Crear Ubicaciones
print("\nCreando ubicaciones...")
ubi_oficina1 = Ubicacion.objects.get_or_create(nombre="Oficina Principal")[0]
ubi_oficina2 = Ubicacion.objects.get_or_create(nombre="Oficina Administrativa")[0]
ubi_almacen = Ubicacion.objects.get_or_create(nombre="Almacén")[0]
ubi_sala_juntas = Ubicacion.objects.get_or_create(nombre="Sala de Juntas")[0]
ubi_recepcion = Ubicacion.objects.get_or_create(nombre="Recepción")[0]
print(f"✓ {Ubicacion.objects.count()} ubicaciones creadas")

# Crear Usuarios Asignados
print("\nCreando usuarios asignados...")
user1 = UsuarioAsignado.objects.get_or_create(
    identificacion="1234567890",
    defaults={
        'nombres': 'Juan Carlos',
        'apellidos': 'García López',
        'email': 'juan.garcia@empresa.com',
        'telefono': '555-0101',
        'cargo': 'Gerente General',
        'departamento': 'Gerencia',
        'activo': True
    }
)[0]

user2 = UsuarioAsignado.objects.get_or_create(
    identificacion="0987654321",
    defaults={
        'nombres': 'María Elena',
        'apellidos': 'Rodríguez Pérez',
        'email': 'maria.rodriguez@empresa.com',
        'telefono': '555-0102',
        'cargo': 'Asistente Administrativa',
        'departamento': 'Administración',
        'activo': True
    }
)[0]

user3 = UsuarioAsignado.objects.get_or_create(
    identificacion="1122334455",
    defaults={
        'nombres': 'Pedro Antonio',
        'apellidos': 'Martínez Silva',
        'email': 'pedro.martinez@empresa.com',
        'telefono': '555-0103',
        'cargo': 'Jefe de IT',
        'departamento': 'Tecnología',
        'activo': True
    }
)[0]

print(f"✓ {UsuarioAsignado.objects.count()} usuarios asignados creados")

# Crear Activos
print("\nCreando activos...")

# Computadores
Activo.objects.get_or_create(
    codigo_inventario="IT-PC-001",
    defaults={
        'subcategoria': subcat_computadores,
        'marca': 'Dell',
        'modelo': 'OptiPlex 7090',
        'numero_serial': 'SN123456789',
        'usuario_asignado': user1,
        'ubicacion': ubi_oficina1,
        'estado': 'AC',
        'observaciones': 'Computador de escritorio Intel i7, 16GB RAM, SSD 512GB'
    }
)

Activo.objects.get_or_create(
    codigo_inventario="IT-PC-002",
    defaults={
        'subcategoria': subcat_computadores,
        'marca': 'HP',
        'modelo': 'EliteDesk 800',
        'numero_serial': 'SN987654321',
        'usuario_asignado': user3,
        'ubicacion': ubi_oficina1,
        'estado': 'AC',
        'observaciones': 'Computador de escritorio Intel i5, 8GB RAM'
    }
)

# Monitores
Activo.objects.get_or_create(
    codigo_inventario="IT-MON-001",
    defaults={
        'subcategoria': subcat_monitores,
        'marca': 'Samsung',
        'modelo': 'S24F350',
        'numero_serial': 'MON123456',
        'usuario_asignado': user1,
        'ubicacion': ubi_oficina1,
        'estado': 'AC',
        'observaciones': 'Monitor LED 24 pulgadas Full HD'
    }
)

# Impresoras
Activo.objects.get_or_create(
    codigo_inventario="IT-IMP-001",
    defaults={
        'subcategoria': subcat_impresoras,
        'marca': 'HP',
        'modelo': 'LaserJet Pro M404dn',
        'numero_serial': 'IMP789012',
        'ubicacion': ubi_oficina2,
        'estado': 'EM',
        'observaciones': 'Impresora láser monocromática - En mantenimiento preventivo'
    }
)

# Mobiliario
Activo.objects.get_or_create(
    codigo_inventario="MOB-ESC-001",
    defaults={
        'subcategoria': subcat_escritorios,
        'marca': 'OfficeMax',
        'modelo': 'Executive Desk',
        'usuario_asignado': user1,
        'ubicacion': ubi_oficina1,
        'estado': 'AC',
        'observaciones': 'Escritorio ejecutivo de madera'
    }
)

Activo.objects.get_or_create(
    codigo_inventario="MOB-SIL-001",
    defaults={
        'subcategoria': subcat_sillas,
        'marca': 'Herman Miller',
        'modelo': 'Aeron',
        'numero_serial': 'SIL456789',
        'usuario_asignado': user2,
        'ubicacion': ubi_oficina2,
        'estado': 'AC',
        'observaciones': 'Silla ergonómica con soporte lumbar'
    }
)

Activo.objects.get_or_create(
    codigo_inventario="MOB-SIL-002",
    defaults={
        'subcategoria': subcat_sillas,
        'marca': 'IKEA',
        'modelo': 'Markus',
        'ubicacion': ubi_almacen,
        'estado': 'IN',
        'observaciones': 'Silla de oficina en almacén - Sin asignar'
    }
)

# Vehículo
Activo.objects.get_or_create(
    codigo_inventario="VEH-CAR-001",
    defaults={
        'subcategoria': subcat_automoviles,
        'marca': 'Toyota',
        'modelo': 'Corolla 2022',
        'numero_serial': 'VIN1234567890ABCD',
        'ubicacion': ubi_recepcion,
        'estado': 'AC',
        'observaciones': 'Vehículo de la empresa - Placa ABC-123'
    }
)

print(f"✓ {Activo.objects.count()} activos creados")

print("\n=== Configuración completada exitosamente ===")
print(f"""
Resumen:
- Categorías: {Categoria.objects.count()}
- Subcategorías: {SubCategoria.objects.count()}
- Ubicaciones: {Ubicacion.objects.count()}
- Usuarios Asignados: {UsuarioAsignado.objects.count()}
- Activos: {Activo.objects.count()}

Ahora puedes iniciar el servidor con: python manage.py runserver
Y acceder a http://localhost:8000/
""")


