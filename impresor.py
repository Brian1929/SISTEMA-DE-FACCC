"""
Módulo para impresión de facturas con soporte para diferentes formatos de papel.
Versión con diseño moderno y minimalista.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import datetime
from factura import Factura


class FormatoPapel(ABC):
    """Clase abstracta base para diferentes formatos de papel."""
    
    @property
    @abstractmethod
    def nombre(self) -> str:
        """Nombre del formato de papel."""
        pass
    
    @property
    @abstractmethod
    def ancho(self) -> float:
        """Ancho del papel en milímetros."""
        pass
    
    @property
    @abstractmethod
    def alto(self) -> float:
        """Alto del papel en milímetros."""
        pass
    
    @abstractmethod
    def obtener_configuracion(self) -> Dict[str, Any]:
        """Retorna la configuración específica del formato."""
        pass


class PapelNormal(FormatoPapel):
    """Formato de papel estándar (A4)."""
    
    @property
    def nombre(self) -> str:
        return "Papel Normal (A4)"
    
    @property
    def ancho(self) -> float:
        return 210.0  # mm
    
    @property
    def alto(self) -> float:
        return 297.0  # mm
    
    def obtener_configuracion(self) -> Dict[str, Any]:
        return {
            "margen_superior": 15,
            "margen_inferior": 15,
            "margen_izquierdo": 15,
            "margen_derecho": 15,
            "tamano_titulo": 16,
            "tamano_texto": 10,
            "espaciado_linea": 12,
        }


class PapelTermico(FormatoPapel):
    """Formato de papel térmico (80mm de ancho)."""
    
    @property
    def nombre(self) -> str:
        return "Papel Térmico (80mm)"
    
    @property
    def ancho(self) -> float:
        return 80.0  # mm
    
    @property
    def alto(self) -> float:
        return 297.0  # mm (rollo continuo)
    
    def obtener_configuracion(self) -> Dict[str, Any]:
        return {
            "margen_superior": 10,
            "margen_inferior": 10,
            "margen_izquierdo": 5,
            "margen_derecho": 5,
            "tamano_titulo": 12,
            "tamano_texto": 8,
            "espaciado_linea": 10,
        }


class PapelCarta(FormatoPapel):
    """Formato de papel carta (8.5 x 11 pulgadas)."""
    
    @property
    def nombre(self) -> str:
        return "Papel Carta (8.5x11)"
    
    @property
    def ancho(self) -> float:
        return 216.0  # mm
    
    @property
    def alto(self) -> float:
        return 279.0  # mm
    
    def obtener_configuracion(self) -> Dict[str, Any]:
        return {
            "margen_superior": 25,
            "margen_inferior": 25,
            "margen_izquierdo": 25,
            "margen_derecho": 25,
            "tamano_titulo": 18,
            "tamano_texto": 11,
            "espaciado_linea": 14,
        }


class ImpresorFactura(ABC):
    """Clase abstracta base para impresores de facturas."""
    
    @abstractmethod
    def imprimir(self, factura: Factura, formato: FormatoPapel) -> str:
        """
        Genera la representación de la factura para impresión.
        
        Args:
            factura: La factura a imprimir
            formato: El formato de papel a usar
            
        Returns:
            String con la representación de la factura
        """
        pass


class ImpresorTexto(ImpresorFactura):
    """Impresor que genera facturas en formato de texto plano."""
    
    def imprimir(self, factura: Factura, formato: FormatoPapel) -> str:
        """Genera una factura en formato de texto."""
        config = formato.obtener_configuracion()
        ancho_total = formato.ancho - config["margen_izquierdo"] - config["margen_derecho"]
        
        # Encabezado
        resultado = []
        resultado.append("=" * int(ancho_total / 2))
        resultado.append("FACTURA".center(int(ancho_total / 2)))
        resultado.append("=" * int(ancho_total / 2))
        resultado.append("")
        
        # Información de la factura
        resultado.append(f"Número: {factura.numero}")
        resultado.append(f"Fecha: {factura.fecha.strftime('%d/%m/%Y %H:%M:%S')}")
        resultado.append(f"Cliente: {factura.cliente}")
        resultado.append("")
        resultado.append("-" * int(ancho_total / 2))
        resultado.append("")
        
        # Items
        resultado.append(f"{'Código':<10} {'Descripción':<30} {'Cant.':>8} {'Precio':>12} {'Total':>12}")
        resultado.append("-" * int(ancho_total / 2))
        
        for item in factura.items:
            producto = item.producto
            subtotal = item.calcular_subtotal()
            
            # Primera línea: código y nombre
            nombre_completo = producto.nombre
            if len(nombre_completo) > 30:
                nombre_completo = nombre_completo[:27] + "..."
            
            resultado.append(
                f"{producto.codigo:<10} {nombre_completo:<30} "
                f"{item.cantidad:>8.2f} ${producto.precio:>11.2f} ${subtotal:>11.2f}"
            )
        
        resultado.append("-" * int(ancho_total / 2))
        resultado.append("")
        
        # Totales
        subtotal = factura.calcular_subtotal()
        impuesto = factura.calcular_impuesto()
        total = factura.calcular_total()
        
        resultado.append(f"{'Subtotal:':<50} ${subtotal:>11.2f}")
        if factura.impuesto > 0:
            resultado.append(f"{'Impuesto (' + str(factura.impuesto) + '%):':<50} ${impuesto:>11.2f}")
        resultado.append("=" * int(ancho_total / 2))
        resultado.append(f"{'TOTAL:':<50} ${total:>11.2f}")
        resultado.append("=" * int(ancho_total / 2))
        
        # Notas
        if factura.notas:
            resultado.append("")
            resultado.append("Notas:")
            resultado.append(factura.notas)
        
        resultado.append("")
        resultado.append("Gracias por su compra!")
        
        return "\n".join(resultado)


class ImpresorPDF(ImpresorFactura):
    """Impresor que genera facturas en formato PDF con diseño moderno y minimalista."""
    
    def imprimir(self, factura: Factura, formato: FormatoPapel) -> bytes:
        """Genera una factura en formato PDF con diseño Ejecutivo Premium y bordes redondeados."""
        try:
            from reportlab.lib.pagesizes import A4, letter
            from reportlab.lib.units import mm
            from reportlab.lib import colors
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable, Flowable
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
            import io
            
            # Clase auxiliar para bordes redondeados
            class RoundedBackground(Flowable):
                def __init__(self, table, radius=5, color=colors.white):
                    Flowable.__init__(self)
                    self.table = table
                    self.radius = radius
                    self.color = color
                    self.hAlign = 'LEFT'
                    self.width, self.height = table.wrap(0, 0)
                def draw(self):
                    self.canv.setFillColor(self.color)
                    self.canv.roundRect(0, 0, self.width, self.height, self.radius, stroke=0, fill=1)
                    self.table.drawOn(self.canv, 0, 0)
            
            # Cargar configuración
            try:
                from configuracion import Configuracion
                config_sistema = Configuracion()
                nombre_empresa = config_sistema.obtener("nombre_empresa", "BrianTech")
                direccion_empresa = config_sistema.obtener("direccion_empresa", "Santiago, Rep. Dom.")
                telefono_empresa = config_sistema.obtener("telefono_empresa", "(849)-711-2919")
                email_empresa = config_sistema.obtener("email_empresa", "Brianpolanco95@gmail.com")
                rfc_empresa = config_sistema.obtener("rfc_empresa", "")
                hex_color = config_sistema.obtener("color_factura", "#27AE60")
            except:
                nombre_empresa = "EMPRESA"
                direccion_empresa = "Dirección"
                telefono_empresa = "Teléfono"
                email_empresa = "Email"
                rfc_empresa = ""
                hex_color = "#27AE60"
            
            buffer = io.BytesIO()
            COLOR_PRIMARY = colors.HexColor(hex_color)
            COLOR_SECONDARY = colors.HexColor('#2C3E50')
            COLOR_ACCENT = colors.HexColor('#F2F4F4')
            COLOR_WHITE = colors.white
            
            pagesize = letter if isinstance(formato, PapelCarta) else A4
            doc = SimpleDocTemplate(buffer, pagesize=pagesize, rightMargin=15*mm, leftMargin=15*mm, topMargin=15*mm, bottomMargin=15*mm)
            
            styles = getSampleStyleSheet()
            story = []
            width = pagesize[0] - 30 * mm
            
            # Cargar logo de empresa para PDF
            try:
                logo_base64 = config_sistema.obtener("logo_empresa", "")
            except:
                logo_base64 = ""
            
            # --- ENCABEZADO ---
            title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=22, textColor=COLOR_PRIMARY, alignment=TA_RIGHT)
            empresa_style = ParagraphStyle('EmpresaStyle', parent=styles['Normal'], fontSize=18, textColor=COLOR_SECONDARY, leading=22, fontName='Helvetica-Bold')
            sub_style = ParagraphStyle('SubStyle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#566573'), leading=14)
            
            # Limpiar prefijo Tel si ya existe en el string
            tel_display = telefono_empresa if "Tel" in telefono_empresa else f"Tel: {telefono_empresa}"
            
            # Procesar logo si existe
            logo_img = None
            if logo_base64:
                try:
                    import base64
                    from reportlab.platypus import Image
                    if "," in logo_base64:
                        logo_base64 = logo_base64.split(",")[1]
                    img_data = base64.b64decode(logo_base64)
                    img_buffer = io.BytesIO(img_data)
                    logo_img = Image(img_buffer)
                    
                    # Redimensionar logo manteniendo proporción (max 28mm alto, 55mm ancho)
                    aspect = logo_img.imageWidth / logo_img.imageHeight
                    logo_img.drawHeight = 28 * mm
                    logo_img.drawWidth = 28 * mm * aspect
                    if logo_img.drawWidth > 55 * mm:
                        logo_img.drawWidth = 55 * mm
                        logo_img.drawHeight = 55 * mm / aspect
                except Exception as e:
                    print(f"⚠ Error al procesar logo: {str(e)}")
            
            # Determinar título del documento
            tipo_doc = "COTIZACIÓN" if "Cotizacion" in str(type(factura)) else "FACTURA"
            
            if logo_img:
                header_data = [[
                    logo_img,
                    [Paragraph(nombre_empresa, empresa_style), 
                     Paragraph(f"{direccion_empresa}<br/>{tel_display} | {email_empresa}<br/>{rfc_empresa}", sub_style)],
                    Paragraph(tipo_doc, title_style)
                ]]
                # Ajuste de anchos: Logo (30%), Info (35%), Título (35%) para dar más aire
                header_table = Table(header_data, colWidths=[width * 0.30, width * 0.35, width * 0.35])
            else:
                header_data = [[
                    [Paragraph(nombre_empresa, empresa_style), 
                     Paragraph(f"{direccion_empresa}<br/>{tel_display} | {email_empresa}<br/>{rfc_empresa}", sub_style)],
                    Paragraph(tipo_doc, title_style)
                ]]
                header_table = Table(header_data, colWidths=[width * 0.65, width * 0.35])
            
            header_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (0, 0), 'LEFT')
            ]))
            header_table.hAlign = 'LEFT'
            story.append(header_table)
            story.append(Spacer(1, 5))
            story.append(HRFlowable(width="100%", thickness=4, color=COLOR_PRIMARY, spaceAfter=25))
            
            # --- INFO CLIENTE ---
            label_style = ParagraphStyle('Label', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#7F8C8D'), leading=12)
            value_style = ParagraphStyle('Value', parent=styles['Normal'], fontSize=11, textColor=COLOR_SECONDARY, leading=14)
            
            info_data = [
                [Paragraph("FACTURAR A", label_style), "", Paragraph("DETALLES DE FACTURA", label_style), ""],
                [Paragraph(f"<b>{factura.cliente}</b>", value_style), "", Paragraph(f"<b>No:</b> {factura.numero}", value_style), ""],
                ["", "", Paragraph(f"<b>Fecha:</b> {factura.fecha.strftime('%d/%m/%Y')}", value_style), ""]
            ]
            
            info_table = Table(info_data, colWidths=[width*0.15, width*0.35, width*0.25, width*0.25])
            info_table.setStyle(TableStyle([('SPAN', (0, 1), (1, 1)), ('VALIGN', (0, 0), (-1, -1), 'TOP')]))
            info_table.hAlign = 'LEFT'
            story.append(info_table)
            story.append(Spacer(1, 20))
            
            # --- TABLA ITEMS CON HEADER REDONDEADO ---
            header_left_style = ParagraphStyle('HLeft', parent=styles['Normal'], fontSize=10, textColor=COLOR_WHITE, fontName='Helvetica-Bold', alignment=TA_LEFT)
            header_right_style = ParagraphStyle('HRight', parent=styles['Normal'], fontSize=10, textColor=COLOR_WHITE, fontName='Helvetica-Bold', alignment=TA_RIGHT)
            
            items_header_data = [[
                Paragraph("DESCRIPCIÓN", header_left_style),
                Paragraph("CANT.", header_right_style),
                Paragraph("PRECIO", header_right_style),
                Paragraph("TOTAL", header_right_style)
            ]]
            items_header_table = Table(items_header_data, colWidths=[width*0.54, width*0.12, width*0.16, width*0.18])
            items_header_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (1, 0), (-1, 0), 'RIGHT'),
                ('TOPPADDING', (0, 0), (-1, 0), 7),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 7),
                ('LEFTPADDING', (0, 0), (-1, 0), 5),
                ('RIGHTPADDING', (0, 0), (-1, 0), 5),
            ]))
            items_header_table.hAlign = 'LEFT'
            
            story.append(RoundedBackground(items_header_table, radius=6, color=COLOR_PRIMARY))
            
            # Contenido de items
            items_body_data = []
            for i, item in enumerate(factura.items):
                p = item.producto
                desc = f"<b>{p.nombre}</b><br/><font size='7' color='#626567'>SKU: {p.codigo}</font>"
                items_body_data.append([
                    Paragraph(desc, styles['Normal']),
                    f"{item.cantidad:.2f}",
                    f"${p.precio:,.2f}",
                    f"${item.calcular_subtotal():,.2f}"
                ])
            
            if items_body_data:
                items_body_table = Table(items_body_data, colWidths=[width*0.54, width*0.12, width*0.16, width*0.18])
                items_body_table.hAlign = 'LEFT'
                body_style = [
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('LEFTPADDING', (0, 0), (-1, -1), 5),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                    ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor('#D5DBDB')),
                ]
                for i in range(len(items_body_data)):
                    bg = COLOR_WHITE if i % 2 != 0 else COLOR_ACCENT
                    body_style.append(('BACKGROUND', (0, i), (-1, i), bg))
                items_body_table.setStyle(TableStyle(body_style))
                story.append(items_body_table)
            
            story.append(Spacer(1, 15))
            
            # --- TOTALES ---
            totals_label_style = ParagraphStyle('TotalLabel', parent=styles['Normal'], fontSize=11, textColor=colors.HexColor('#566573'), alignment=TA_RIGHT)
            totals_value_style = ParagraphStyle('TotalValue', parent=styles['Normal'], fontSize=11, textColor=COLOR_SECONDARY, alignment=TA_RIGHT)
            
            totals_top_data = [
                [Paragraph("SUBTOTAL", totals_label_style), Paragraph(f"${factura.calcular_subtotal():,.2f}", totals_value_style)],
            ]
            totals_top_table = Table(totals_top_data, colWidths=[width*0.3, width*0.2])
            totals_top_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'), 
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('LEFTPADDING', (0, 0), (-1, -1), 5),
                ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ]))
            totals_top_table.hAlign = 'RIGHT'
            
            story.append(Table([[totals_top_table]], colWidths=[width], style=[('ALIGN', (0, 0), (-1, -1), 'RIGHT')]))
            
            # Caja total redondeada compacta
            grand_total_style = ParagraphStyle('GrandTotal', parent=styles['Normal'], fontSize=14, textColor=COLOR_WHITE, alignment=TA_RIGHT, fontName='Helvetica-Bold')
            total_box_data = [[Paragraph("TOTAL", grand_total_style), Paragraph(f"${factura.calcular_total():,.2f}", grand_total_style)]]
            total_box_table = Table(total_box_data, colWidths=[width*0.15, width*0.20])
            total_box_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            total_box_table.hAlign = 'RIGHT'
            
            story.append(Table([[RoundedBackground(total_box_table, radius=8, color=COLOR_PRIMARY)]], colWidths=[width], style=[('ALIGN', (0, 0), (-1, -1), 'RIGHT')]))
            
            if factura.notas:
                story.append(Spacer(1, 30))
                story.append(Paragraph("<b>NOTAS ADICIONALES</b>", label_style))
                story.append(HRFlowable(width="20%", thickness=1, color=COLOR_PRIMARY, hAlign='LEFT', spaceAfter=5))
                story.append(Paragraph(factura.notas, styles['Normal']))
            
            # Cargar nombre para firma
            try:
                firma_autorizado = config_sistema.obtener("firma_autorizado", "")
            except:
                firma_autorizado = ""
            
            story.append(Spacer(1, 60))
            
            # Estilo para el nombre firmado (normal)
            signature_style = ParagraphStyle('SignatureStyle', parent=styles['Normal'], fontSize=12, textColor=COLOR_SECONDARY, fontName='Helvetica-Bold', alignment=TA_CENTER)
            
            firma_data = [
                [Paragraph(firma_autorizado, signature_style), "", ""],
                ["__________________________", "", "__________________________"], 
                ["Autorizado por", "", "Recibido por"]
            ]
            
            firma_table = Table(firma_data, colWidths=[width*0.35, width*0.3, width*0.35])
            firma_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
                ('FONTSIZE', (0, 2), (-1, 2), 8),
                ('TEXTCOLOR', (0, 2), (-1, 2), colors.HexColor('#7F8C8D')),
                ('BOTTOMPADDING', (0, 0), (0, 0), -2), # Bajar nombre a la línea
                ('TOPPADDING', (0, 1), (0, 1), 0),   # Quitar espacio sobre la línea
                ('TOPPADDING', (2, 1), (2, 1), 0),   # Quitar espacio sobre la línea de recibo
            ]))
            story.append(firma_table)
            
            story.append(Spacer(1, 40))
            footer_text = f"Generado electrónicamente por {nombre_empresa} el {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
            story.append(Paragraph(footer_text, ParagraphStyle('F', parent=styles['Normal'], fontSize=7, textColor=colors.HexColor('#BDC3C7'), alignment=TA_CENTER)))
            
            doc.build(story)
            buffer.seek(0)
            pdf_bytes = buffer.read()
            buffer.close()
            return pdf_bytes
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise Exception(f"Error en PDF Redondeado: {str(e)}")


class GestorImpresion:
    """Gestor centralizado para la impresión de facturas."""
    
    def __init__(self):
        self._impresores: Dict[str, ImpresorFactura] = {
            "texto": ImpresorTexto(),
            "pdf": ImpresorPDF(),
        }
        self._formatos: Dict[str, FormatoPapel] = {
            "normal": PapelNormal(),
            "termico": PapelTermico(),
            "carta": PapelCarta(),
        }
    
    def registrar_impresor(self, nombre: str, impresor: ImpresorFactura) -> None:
        """Registra un nuevo tipo de impresor."""
        self._impresores[nombre] = impresor
    
    def registrar_formato(self, nombre: str, formato: FormatoPapel) -> None:
        """Registra un nuevo formato de papel."""
        self._formatos[nombre] = formato
    
    def imprimir(self, factura: Factura, tipo_impresor: str = "texto", formato_papel: str = "normal") -> str:
        """
        Imprime una factura usando el impresor y formato especificados.
        
        Args:
            factura: La factura a imprimir
            tipo_impresor: Tipo de impresor ("texto" o "pdf")
            formato_papel: Formato de papel ("normal", "termico", "carta")
            
        Returns:
            Resultado de la impresión
        """
        if tipo_impresor not in self._impresores:
            raise ValueError(f"Impresor '{tipo_impresor}' no encontrado")
        
        if formato_papel not in self._formatos:
            raise ValueError(f"Formato '{formato_papel}' no encontrado")
        
        impresor = self._impresores[tipo_impresor]
        formato = self._formatos[formato_papel]
        
        return impresor.imprimir(factura, formato)
    
    def listar_impresores(self) -> list[str]:
        """Lista los impresores disponibles."""
        return list(self._impresores.keys())
    
    def listar_formatos(self) -> list[str]:
        """Lista los formatos de papel disponibles."""
        return list(self._formatos.keys())
