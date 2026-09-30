"""Compila docs/informe.md y las figuras intermedias en un PDF."""

import argparse
import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


RAIZ = Path(__file__).resolve().parent
INFORME = RAIZ / "docs" / "informe.md"
SALIDA = RAIZ / "docs" / "informe.pdf"

# Las marcas del informe señalan las capturas generadas por cada apartado.
CAPTURAS = {
    "b_histogramas": ("b", "comparacion_histogramas.png", "Comparación global y local con sus histogramas."),
    "b_zonas": ("b", "zonas.png", "Los cinco recortes originales y sus resultados locales."),
    "c_ventanas": ("c", "comparacion_ventanas.png", "Imagen original, referencia global y diez ventanas."),
    "c_zonas": ("c", "comparacion_zonas.png", "Cinco zonas procesadas con cinco ventanas cuadradas."),
    "c_rectangulares": ("c", "comparacion_rectangulares.png", "Ventanas cuadrada y rectangulares de comparación."),
}


def formato_en_linea(texto):
    """Convierte negrita, cursiva, código y enlaces Markdown a texto PDF."""
    texto = html.escape(texto, quote=False)
    texto = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", texto)
    texto = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', texto)
    texto = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", texto)
    return re.sub(r"\*(.+?)\*", r"<i>\1</i>", texto)


def separar_celdas(fila):
    """Lee las celdas de una fila sencilla de tabla Markdown."""
    return [celda.strip() for celda in fila.strip().strip("|").split("|")]


def compilar(informe, salida, capturas_b, capturas_c):
    """Construye el PDF a partir del Markdown y las cinco figuras de los scripts."""
    informe = Path(informe)
    salida = Path(salida)
    capturas = {"b": Path(capturas_b), "c": Path(capturas_c)}
    texto = informe.read_text(encoding="utf-8")
    for seccion, archivo, _ in CAPTURAS.values():
        ruta = capturas[seccion] / archivo
        if not ruta.is_file():
            raise FileNotFoundError(f"Falta una captura. Ejecute primero los apartados b y c: {ruta}")

    estilos = getSampleStyleSheet()
    estilos.add(ParagraphStyle(
        name="TituloInforme", parent=estilos["Title"], fontName="Helvetica-Bold",
        fontSize=23, leading=28, textColor=colors.HexColor("#17365D"),
        alignment=TA_LEFT, spaceAfter=16,
    ))
    estilos.add(ParagraphStyle(
        name="SubtituloInforme", parent=estilos["Heading2"], fontSize=15,
        leading=19, textColor=colors.HexColor("#245B80"), spaceBefore=16,
        spaceAfter=7, keepWithNext=True,
    ))
    estilos.add(ParagraphStyle(
        name="TextoInforme", parent=estilos["BodyText"], fontName="Helvetica",
        fontSize=9.5, leading=14, textColor=colors.HexColor("#253244"),
        alignment=TA_LEFT, spaceAfter=8,
    ))
    estilos.add(ParagraphStyle(
        name="CeldaInforme", parent=estilos["BodyText"], fontSize=8,
        leading=10.5, spaceAfter=0,
    ))
    estilos.add(ParagraphStyle(
        name="CodigoInforme", parent=estilos["Code"], fontName="Courier",
        fontSize=8, leading=11, backColor=colors.HexColor("#F0F3F7"),
        borderPadding=8, spaceBefore=4, spaceAfter=10,
    ))
    estilos.add(ParagraphStyle(
        name="PieFigura", parent=estilos["BodyText"], fontName="Helvetica-Oblique",
        fontSize=8.5, leading=11, textColor=colors.HexColor("#526477"),
        alignment=TA_CENTER, spaceAfter=6,
    ))

    cuerpo = []
    lineas = texto.splitlines()
    indice = 0
    while indice < len(lineas):
        linea = lineas[indice].strip()
        if not linea:
            indice += 1
            continue

        # Inserta cada figura exactamente donde su marca aparece en el Markdown.
        marca = re.fullmatch(r"<!--\s*CAPTURA:\s*([a-z_]+)\s*-->", linea)
        if marca:
            nombre = marca.group(1)
            if nombre not in CAPTURAS:
                raise ValueError(f"Marca de captura desconocida en el informe: {nombre}")
            seccion, archivo, descripcion = CAPTURAS[nombre]
            imagen = Image(
                str(capturas[seccion] / archivo),
                width=17 * cm,
                height=11.4 * cm,
                kind="proportional",
                hAlign="CENTER",
            )
            cuerpo.append(KeepTogether([
                Paragraph("Captura intermedia: " + descripcion, estilos["PieFigura"]),
                imagen,
                Spacer(1, 10),
            ]))
            indice += 1
            continue

        # Reconoce tablas Markdown y repite su encabezado si ocupan más de una página.
        if linea.startswith("|") and indice + 1 < len(lineas) and "---" in lineas[indice + 1]:
            filas = [separar_celdas(linea)]
            indice += 2
            while indice < len(lineas) and lineas[indice].strip().startswith("|"):
                filas.append(separar_celdas(lineas[indice].strip()))
                indice += 1
            datos = [[Paragraph(formato_en_linea(celda), estilos["CeldaInforme"])
                      for celda in fila] for fila in filas]
            cantidad = len(filas[0])
            tabla = Table(
                datos,
                colWidths=[17 * cm / cantidad] * cantidad,
                repeatRows=1,
                hAlign="LEFT",
            )
            tabla.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17365D")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F2F5F8")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CAD4DF")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]))
            cuerpo.extend([Spacer(1, 4), tabla, Spacer(1, 10)])
            continue

        # Mantiene los títulos y subtítulos Markdown como secciones visibles del informe.
        titulo = re.match(r"^(#{1,3})\s+(.+)$", linea)
        if titulo:
            nivel = len(titulo.group(1))
            estilo = estilos["TituloInforme"] if nivel == 1 else estilos["SubtituloInforme"]
            cuerpo.append(Paragraph(formato_en_linea(titulo.group(2)), estilo))
            indice += 1
            continue

        # Conserva los listados del Markdown como viñetas de texto.
        if linea.startswith("- "):
            elementos = []
            while indice < len(lineas) and lineas[indice].strip().startswith("- "):
                item = lineas[indice].strip()[2:]
                elementos.append(ListItem(Paragraph(formato_en_linea(item), estilos["TextoInforme"])))
                indice += 1
            cuerpo.append(ListFlowable(
                elementos, bulletType="bullet", start="circle", leftIndent=18, bulletFontSize=7
            ))
            cuerpo.append(Spacer(1, 6))
            continue

        # Une líneas consecutivas de texto para preservar cada párrafo.
        if linea.startswith("``` ") or linea == "```":
            indice += 1
            codigo = []
            while indice < len(lineas) and lineas[indice].strip() != "```":
                codigo.append(lineas[indice].rstrip())
                indice += 1
            indice += 1
            cuerpo.append(Paragraph(html.escape("<br/>".join(codigo)), estilos["CodigoInforme"]))
            continue

        parrafo = [linea]
        indice += 1
        while indice < len(lineas):
            siguiente = lineas[indice].strip()
            if (not siguiente or siguiente.startswith(("#", "|", "- ", "<!--", "```"))):
                break
            parrafo.append(siguiente)
            indice += 1
        cuerpo.append(Paragraph(formato_en_linea(" ".join(parrafo)), estilos["TextoInforme"]))

    salida.parent.mkdir(parents=True, exist_ok=True)

    def encabezado_y_pie(canvas, documento):
        canvas.saveState()
        ancho, alto = A4
        canvas.setStrokeColor(colors.HexColor("#CAD4DF"))
        canvas.setLineWidth(0.6)
        canvas.line(documento.leftMargin, alto - 39, ancho - documento.rightMargin, alto - 39)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#526477"))
        canvas.drawString(documento.leftMargin, alto - 31, "Procesamiento de Imágenes I | TP1 | Problema 1")
        canvas.drawRightString(ancho - documento.rightMargin, 24, f"Página {documento.page}")
        canvas.restoreState()

    documento = SimpleDocTemplate(
        str(salida), pagesize=A4, title="Informe TP1 - Problema 1",
        author="Tomas Colombo, Manuel Ibarbia, Juan Manuel Ayala y Franco Cerana",
        subject="Ecualización local de histograma",
        leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm, bottomMargin=1.5 * cm,
    )
    documento.build(cuerpo, onFirstPage=encabezado_y_pie, onLaterPages=encabezado_y_pie)
    print(f"Informe PDF guardado en: {salida}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--markdown", type=Path, default=INFORME)
    parser.add_argument("--salida", type=Path, default=SALIDA)
    parser.add_argument("--capturas-b", type=Path, required=True)
    parser.add_argument("--capturas-c", type=Path, required=True)
    argumentos = parser.parse_args()
    compilar(argumentos.markdown, argumentos.salida, argumentos.capturas_b, argumentos.capturas_c)
