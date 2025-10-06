# 📋 Instrucciones para Agregar el Logo de PALDACA

## 🎯 Objetivo
Reemplazar el placeholder "LOGO PALDACA" con tu logo oficial en los reportes PDF.

## 📁 Ubicación del Archivo
Coloca tu logo en la siguiente ruta:
```
core/static/core/img/logo_paldaca.png
```

## 🔧 Modificación Necesaria

Una vez que hayas colocado el archivo `logo_paldaca.png`, descomenta las siguientes líneas en el archivo `reportes/utils.py`:

### En la función `crear_encabezado_institucional()` (líneas 133-135):

**Cambiar esto:**
```python
# TODO: Reemplazar con el logo oficial de PALDACA
# logo_path = os.path.join(settings.STATIC_ROOT, 'core/img/logo_paldaca.png')
# logo = Image(logo_path, width=2*inch, height=0.8*inch)

# Por ahora, crear un placeholder para el logo
logo_placeholder = Paragraph(
    '<font color="#32407b" size="16"><b>LOGO PALDACA</b></font>',
    ParagraphStyle('LogoPlaceholder', alignment=TA_LEFT, fontSize=16)
)
```

**Por esto:**
```python
# Logo oficial de PALDACA
logo_path = os.path.join(settings.STATIC_ROOT, 'core/img/logo_paldaca.png')
logo = Image(logo_path, width=2*inch, height=0.8*inch)

# Usar el logo real en lugar del placeholder
logo_placeholder = logo
```

### En la tabla del encabezado (línea 157):

**Cambiar esto:**
```python
header_data = [[logo_placeholder, empresa_paragraph]]
```

**Por esto:**
```python
header_data = [[logo, empresa_paragraph]]
```

## 📏 Especificaciones del Logo

- **Formato:** PNG (recomendado) o JPG
- **Tamaño:** El sistema lo redimensionará automáticamente a 2 pulgadas de ancho x 0.8 pulgadas de alto
- **Calidad:** Mínimo 300 DPI para impresión profesional
- **Fondo:** Preferiblemente transparente (PNG) o blanco

## ✅ Verificación

Después de hacer los cambios:

1. **Reinicia el servidor Django**
2. **Genera un reporte PDF** desde la lista de activos
3. **Verifica** que el logo aparezca correctamente en el encabezado

## 🎨 Características del Diseño

El logo se mostrará:
- **Posición:** Esquina superior izquierda del encabezado
- **Tamaño:** 2" x 0.8" (ajustable)
- **Alineación:** A la izquierda, con texto de la empresa a la derecha
- **Separación:** Línea divisoria azul (#32407b) debajo del encabezado

## 🔄 Alternativas

Si prefieres un tamaño diferente, puedes modificar los valores en la línea:
```python
logo = Image(logo_path, width=2*inch, height=0.8*inch)
```

**Ejemplos:**
- Logo más grande: `width=2.5*inch, height=1*inch`
- Logo más pequeño: `width=1.5*inch, height=0.6*inch`

---

**¡Listo!** Una vez que agregues el logo, tus reportes PDF tendrán un aspecto completamente profesional e institucional. 🎉
