# servidor_mcp.py
import datetime
import os
from mcp.server.fastmcp import FastMCP
from pptx import Presentation
from pptx.util import Inches, Pt

# Inicializamos el servidor MCP
mcp = FastMCP("MiAgenteLocal")

# --- Definición de Herramientas (Tools) ---


@mcp.tool()
def obtener_hora() -> str:
    """Devuelve la fecha y hora actual del sistema."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@mcp.tool()
def listar_archivos(directorio: str = ".") -> str:
    """
    Lista los archivos en un directorio local.
    Args:
        directorio: Ruta del directorio (por defecto es el actual).
    """
    try:
        files = os.listdir(directorio)
        return (
            f"Archivos en '{directorio} escribirlo en formato json': {', '.join(files)}"
        )
    except Exception as e:
        return f"Error al leer directorio: {str(e)}"


@mcp.tool()
def calcular_suma(a: int, b: int) -> int:
    """Suma dos números enteros."""
    return a + b


@mcp.tool()
def crear_presentacion_educativa(
    contenido: list, nombre_archivo: str = "presentacion_educativa.pptx"
) -> str:
    """
    Crea una presentación de PowerPoint basada en una estructura pedagógica.

    Args:
        contenido: Una lista de diccionarios, donde cada elemento representa una diapositiva.
                   Cada diccionario debe tener 'titulo' y 'cuerpo' (texto o lista de puntos).
                   Se recomienda seguir la secuencia de 13 diapositivas del Architecto Educativo.
        nombre_archivo: El nombre del archivo .pptx a generar.
    """
    try:
        prs = Presentation()

        for slide_data in contenido:
            # Usar layout de Título y Cuerpo (generalmente índice 1)
            slide_layout = prs.slide_layouts[1]
            slide = prs.slides.add_slide(slide_layout)

            # Título
            title = slide.shapes.title
            title.text = slide_data.get("titulo", "Sin Título")

            # Cuerpo
            body = slide.placeholders[1]
            text_content = slide_data.get("cuerpo", "")

            if isinstance(text_content, list):
                tf = body.text_frame
                tf.text = ""  # Limpiar default
                for point in text_content:
                    p = tf.add_paragraph()
                    p.text = point
            else:
                body.text = str(text_content)

        prs.save(nombre_archivo)
        return f"Presentación creada exitosamente: {nombre_archivo}"
    except Exception as e:
        return f"Error al crear la presentación: {str(e)}"


@mcp.tool()
def crear_presentacion_desde_plantilla(
    plantilla_path: str,
    reemplazos: dict,
    contenido_slides: list,
    nombre_archivo: str = "presentacion_plantilla.pptx",
) -> str:
    """
    Crea una presentación basándose en una plantilla, reemplazando marcadores de posición
    y añadiendo diapositivas adicionales.

    Args:
        plantilla_path: Ruta al archivo .pptx de la plantilla.
        reemplazos: Diccionario con los marcadores a reemplazar { '{{MARCADOR}}': 'Valor' }.
        contenido_slides: Lista de diccionarios para las diapositivas adicionales (estructura pedagógica).
        nombre_archivo: Nombre del archivo de salida.
    """
    try:
        prs = Presentation(plantilla_path)

        # 1. Reemplazar texto en todas las diapositivas de la plantilla
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    for placeholder, value in reemplazos.items():
                        if placeholder in shape.text:
                            shape.text = shape.text.replace(placeholder, str(value))

        # Buscar el mejor layout para "Título y Cuerpo" (TITLE_AND_BODY)
        # Intentamos encontrar un layout que tenga al menos un título y un placeholder de cuerpo
        best_layout = None
        # for layout in prs.slide_layouts:
        #     if len(layout.placeholders) >= 2:
        #         print(
        #             f"Layout {layout.name} tiene {len(layout.placeholders)} placeholders."
        #         )
        #         # Verificamos si el primer placeholder es un título
        #         # if layout.name == 'TITLE_AND_BODY':  # 1 es TITLE
        #         #     best_layout = layout
        #         # break

        if best_layout is None:
            best_layout = prs.slide_layouts[2] if len(prs.slide_layouts) > 1 else prs.slide_layouts[2]

        # 2. Añadir las diapositivas pedagógicas
        for slide_data in contenido_slides:
            slide = prs.slides.add_slide(best_layout)

            # Título
            if slide.shapes.title:
                slide.shapes.title.text = slide_data.get("titulo", "Sin Título")
            elif len(slide.placeholders) > 0:
                slide.placeholders[0].text = slide_data.get("titulo", "Sin Título")

            # Cuerpo
            if len(slide.placeholders) > 1:
                body = slide.placeholders[1]
                text_content = slide_data.get("cuerpo", "")
                if isinstance(text_content, list):
                    tf = body.text_frame
                    tf.text = ""
                    for point in text_content:
                        p = tf.add_paragraph()
                        p.text = point
                else:
                    body.text = str(text_content)

        prs.save(nombre_archivo)
        return f"Presentación desde plantilla creada exitosamente: {nombre_archivo}"
    except Exception as e:
        return f"Error al crear la presentación desde plantilla: {str(e)}"


# Si ejecutamos este script directamente, arranca el servidor MCP
if __name__ == "__main__":
    mcp.run()
