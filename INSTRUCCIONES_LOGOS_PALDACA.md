# 📸 Instrucciones para Logos de PALDACA

## Ubicación de los Logos

Los logos deben colocarse en la carpeta:
```
core/static/core/img/
```

## ✅ Logos Necesarios

### 1. **logo blanco.png**
- **Uso**: Navbar (fondo azul marino) y Footer
- **Descripción**: Logo en blanco para fondos oscuros
- **Tamaño recomendado**: 150-200px de ancho, altura proporcional (máx 35px alto)
- **Formato**: PNG con fondo transparente
- **Color del logo**: Blanco (#FFFFFF)

### 2. **logo color.png**
- **Uso**: Header superior derecha
- **Descripción**: Logo a color con los colores corporativos de PALDACA
- **Tamaño recomendado**: 150-200px de ancho, altura proporcional (máx 45px alto)
- **Formato**: PNG con fondo transparente
- **Colores**: Colores corporativos PALDACA

## 📍 Dónde Aparecen

1. **Navbar (logo blanco)**: Esquina superior izquierda
   - Archivo: `core/templates/base.html` línea ~22
   - CSS: `.navbar-paldaca`

2. **Header (logo color)**: Esquina superior derecha
   - Archivo: `core/templates/base.html` línea ~61
   - CSS: `.logoheader`

3. **Footer (logo blanco)**: Centro del footer
   - Archivo: `core/templates/base.html` línea ~89
   - CSS: `footer`

## 🔧 Cómo Agregar los Logos

### Opción 1: Colocar archivos directamente
1. Obtén los logos de PALDACA en formato PNG
2. Renombra los archivos exactamente como:
   - `logo blanco.png`
   - `logo color.png`
3. Colócalos en: `core/static/core/img/`
4. Reinicia el servidor Django: `python manage.py runserver`

### Opción 2: Si los logos tienen otros nombres
Si tus archivos tienen nombres diferentes (ej: `paldaca_white.png`, `paldaca_color.png`):

1. Coloca los archivos en `core/static/core/img/`
2. Edita `core/templates/base.html` y reemplaza:

```html
<!-- Línea ~22 - Navbar -->
<img src="{% static 'core/img/TU_LOGO_BLANCO.png' %}" alt="Consorcio Paldaca" style="max-height: 35px;">

<!-- Línea ~61 - Header -->
<img src="{% static 'core/img/TU_LOGO_COLOR.png' %}" alt="Logo PALDACA" class="logoheader">

<!-- Línea ~89 - Footer -->
<img src="{% static 'core/img/TU_LOGO_BLANCO.png' %}" alt="Consorcio Paldaca" style="max-height: 35px;">
```

## 🎨 Especificaciones Técnicas

### Colores Corporativos PALDACA:
```css
--e-global-color-red: #ed2546;
--e-global-color-moradopaldaca: #32407b;
--e-global-color-azulmarino: #141644;
--e-global-color-azul: #282c89;
```

### Fondos donde se muestran:
- **Navbar**: Fondo `#141644` (azul marino) → Usar logo blanco
- **Header**: Fondo blanco → Usar logo a color
- **Footer**: Fondo `#141644` (azul marino) → Usar logo blanco

## ⚠️ Notas Importantes

1. **Formato requerido**: PNG con transparencia
2. **Nombres exactos**: Respeta mayúsculas/minúsculas y espacios
3. **Si los logos no existen**: El sistema seguirá funcionando pero mostrará un error 404 en consola
4. **Caché del navegador**: Si actualizas un logo, limpia la caché del navegador (Ctrl + F5)

## 📝 Verificación

Para verificar que los logos se cargaron correctamente:

1. Abre el navegador en http://localhost:8000/
2. Abre DevTools (F12)
3. Ve a la pestaña "Console"
4. No deberías ver errores 404 para las imágenes
5. En la pestaña "Network" filtra por "img" y verifica que los logos se carguen

## 🆘 Solución de Problemas

### Los logos no se ven:
1. Verifica que los archivos existan en `core/static/core/img/`
2. Verifica que los nombres coincidan exactamente
3. Ejecuta: `python manage.py collectstatic` (si usas producción)
4. Limpia caché del navegador
5. Reinicia el servidor Django

### Error 404 en logos:
- Verifica la ruta: `core/static/core/img/logo blanco.png`
- Verifica que el nombre tenga espacio entre "logo" y "blanco"
- En Windows, verifica que la extensión sea `.png` y no `.png.jpg`

## 📞 Contacto

Si tienes problemas con los logos o necesitas ayuda, contacta al equipo de desarrollo.

---

**Sistema de Gestión de Activos - PALDACA**  
Versión 1.0

