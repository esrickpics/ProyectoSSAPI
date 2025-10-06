import os
import io
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, HRFlowable
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.graphics.shapes import Drawing, Line
from reportlab.graphics import renderPDF


def generar_pdf(template_name, context, filename):
    """
    Genera un PDF institucional moderno usando reportlab
    
    Args:
        template_name: Nombre del template HTML (no se usa en esta implementación)
        context: Contexto con los datos
        filename: Nombre del archivo PDF
    
    Returns:
        HttpResponse con el PDF
    """
    # Crear un buffer para el PDF
    buffer = io.BytesIO()
    
    # Crear el documento PDF con márgenes equilibrados
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=3*cm,
        bottomMargin=2*cm
    )
    
    # Estilos personalizados
    styles = getSampleStyleSheet()
    
    # Estilo para el título principal
    title_style = ParagraphStyle(
        'InstitutionalTitle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#32407b'),
        fontName='Helvetica-Bold'
    )
    
    # Estilo para subtítulos
    subtitle_style = ParagraphStyle(
        'InstitutionalSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=15,
        textColor=colors.HexColor('#32407b'),
        fontName='Helvetica-Bold'
    )
    
    # Estilo para texto normal
    normal_style = ParagraphStyle(
        'InstitutionalNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        fontName='Helvetica'
    )
    
    # Estilo para información del reporte
    info_style = ParagraphStyle(
        'ReportInfo',
        parent=styles['Normal'],
        fontSize=9,
        spaceAfter=4,
        fontName='Helvetica'
    )
    
    # Construir el contenido del PDF
    story = []
    
    # 1. ENCABEZADO INSTITUCIONAL
    header_elements = crear_encabezado_institucional()
    story.extend(header_elements)
    story.append(Spacer(1, 20))
    
    # 2. TÍTULO DEL REPORTE
    if context.get('responsable_entrega'):
        story.append(Paragraph("NOTA DE ENTREGA DE ACTIVOS", title_style))
    else:
        story.append(Paragraph("REPORTE DE ACTIVOS", title_style))
    
    story.append(Spacer(1, 15))
    
    # 3. INFORMACIÓN GENERAL DEL REPORTE
    story.append(crear_informacion_reporte(context, info_style))
    story.append(Spacer(1, 20))
    
    # 4. TABLA DE ACTIVOS
    if context.get('activos'):
        story.append(crear_tabla_activos(context['activos']))
        story.append(Spacer(1, 20))
    
    # 5. SECCIÓN DE FIRMAS (solo para nota de entrega)
    if context.get('responsable_entrega'):
        firmas_elements = crear_seccion_firmas(context, subtitle_style)
        story.extend(firmas_elements)
    
    # 6. PIE DE PÁGINA
    story.append(crear_pie_pagina(context, normal_style))
    
    # Construir el PDF
    doc.build(story)
    
    # Obtener el contenido del buffer
    pdf_content = buffer.getvalue()
    buffer.close()
    
    # Crear respuesta HTTP
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


def crear_encabezado_institucional():
    """Crea el encabezado institucional con logo y datos de la empresa"""
    
    # TODO: Reemplazar con el logo oficial de PALDACA
    logo_path = os.path.join(settings.BASE_DIR, 'core', 'static', 'core', 'img', 'logo_paldaca.png')
    logo = Image(logo_path, width=2*inch, height=0.8*inch)
    print(logo_path)
    # Datos de la empresa
    empresa_data = [
        ['CONSORCIO PALDACA'],
        ['Sistema de Gestión de Activos'],
        ['Reporte Institucional']
    ]
    
    empresa_text = ''
    for linea in empresa_data:
        empresa_text += f'<font color="#32407b" size="12"><b>{linea[0]}</b></font><br/>'
    
    empresa_paragraph = Paragraph(empresa_text, ParagraphStyle('EmpresaInfo', alignment=TA_RIGHT))
    
    # Crear tabla del encabezado
    header_data = [[logo, empresa_paragraph]]
    header_table = Table(header_data, colWidths=[3*inch, 3*inch])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    
    # Línea divisoria
    line = HRFlowable(width="100%", thickness=2, color=colors.HexColor('#32407b'))
    
    return [header_table, line]


def crear_informacion_reporte(context, info_style):
    """Crea la sección de información del reporte"""
    
    info_data = [
        ['Fecha de generación:', context.get('fecha_generacion', '')],
        ['Total de activos:', str(len(context.get('activos', [])))],
    ]
    
    if context.get('responsable_entrega'):
        info_data.append(['Responsable de entrega:', context['responsable_entrega']])
    
    if context.get('observaciones'):
        info_data.append(['Observaciones:', context['observaciones']])
    
    # Crear tabla de información
    info_table = Table(info_data, colWidths=[2.5*inch, 3.5*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (1, 0), (1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    return info_table


def crear_tabla_activos(activos):
    """Crea la tabla profesional de activos"""
    
    # Encabezados optimizados
    headers = ['Código', 'Categoría', 'Marca', 'Modelo', 'Serial', 'Ubicación', 'Estado', 'Usuario']
    
    # Datos de la tabla
    table_data = [headers]
    
    for activo in activos:
        row = [
            activo.codigo_inventario,
            f"{activo.subcategoria.categoria.nombre} - {activo.subcategoria.nombre}",
            activo.marca,
            activo.modelo,
            activo.numero_serial or 'N/A',
            activo.ubicacion.nombre,
            activo.get_estado_display(),
            str(activo.usuario_asignado) if activo.usuario_asignado else 'Sin asignar'
        ]
        table_data.append(row)
    
    # Crear la tabla con anchos optimizados
    activos_table = Table(table_data, colWidths=[0.9*inch, 1.3*inch, 0.8*inch, 0.9*inch, 0.8*inch, 0.8*inch, 0.7*inch, 0.8*inch])
    activos_table.setStyle(TableStyle([
        # Estilo del encabezado
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#32407b')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        
        # Estilo del contenido
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    ]))
    
    return activos_table


def crear_seccion_firmas(context, subtitle_style):
    """Crea la sección de firmas para nota de entrega"""
    
    story = []
    story.append(Paragraph("FIRMAS DE ENTREGA Y RECEPCIÓN", subtitle_style))
    story.append(Spacer(1, 20))
    
    # Tabla de firmas profesional
    signature_data = [
        ['ENTREGA', 'RECEPCIÓN'],
        ['', ''],
        ['Responsable:', 'Recibe:'],
        [context['responsable_entrega'], '_____________________'],
        ['', ''],
        ['Firma y sello:', 'Firma y sello:'],
        ['', ''],
        ['', ''],
        ['', ''],
        ['Fecha: _______________', 'Fecha: _______________']
    ]
    
    signature_table = Table(signature_data, colWidths=[3*inch, 3*inch])
    signature_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#32407b')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('MINROWHEIGHT', (0, 0), (-1, -1), 25),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#32407b')),
    ]))
    
    story.append(signature_table)
    return story


def crear_pie_pagina(context, normal_style):
    """Crea el pie de página institucional"""
    
    footer_text = f"""
    <para align="center">
    <font size="8" color="#666666">
    Este documento fue generado automáticamente por el Sistema de Gestión de Activos de Consorcio PALDACA<br/>
    Fecha: {context.get('fecha_generacion', '')} | Total de registros: {len(context.get('activos', []))}
    </font>
    </para>
    """
    
    return Paragraph(footer_text, normal_style)


def formatear_fecha(fecha):
    """Formatea una fecha para mostrar en español"""
    if fecha:
        meses = [
            'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
            'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
        ]
        return f"{fecha.day} de {meses[fecha.month - 1]} de {fecha.year}"
    return ""


def obtener_filtros_aplicados(request):
    """Extrae los filtros aplicados de la request"""
    filtros = {}
    
    # Filtros de activos
    if request.GET.get('categoria'):
        filtros['categoria'] = request.GET.get('categoria')
    if request.GET.get('subcategoria'):
        filtros['subcategoria'] = request.GET.get('subcategoria')
    if request.GET.get('ubicacion'):
        filtros['ubicacion'] = request.GET.get('ubicacion')
    if request.GET.get('estado'):
        filtros['estado'] = request.GET.get('estado')
    if request.GET.get('usuario_asignado'):
        filtros['usuario_asignado'] = request.GET.get('usuario_asignado')
    if request.GET.get('buscar'):
        filtros['buscar'] = request.GET.get('buscar')
    
    return filtros
