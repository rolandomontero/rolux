# servidor_mcp.py

import os
from mcp.server.fastmcp import FastMCP
from pptx import Presentation
from pptx.util import Inches, Pt
from pathlib import Path
import re

# ============================================================
#  PROCESAMIENTO DE REFERENCIAS A ARCHIVOS
# ============================================================

def resolver_ruta_archivo(path_referencia, base_dir=None, workspace_root=None):
    base_dir = Path(base_dir or os.getcwd()).resolve()
    workspace_root = Path(workspace_root or base_dir).resolve()
    referencia = (path_referencia or "").strip().strip('"').strip("'")

    if not referencia:
        return None

    if referencia.startswith("~"):
        referencia = os.path.expanduser(referencia)

    candidatos = []
    if os.path.isabs(referencia):
        candidatos.append(Path(referencia))
    else:
        candidatos.extend([
            base_dir / referencia,
            workspace_root / referencia,
            Path(referencia),
        ])

    for candidato in candidatos:
        if candidato.exists():
            return candidato.resolve()

    return None

def procesar_referencias_archivo(mensaje, base_dir=None, workspace_root=None):
    if not mensaje:
        return mensaje, []

    base_dir = Path(base_dir or os.getcwd()).resolve()
    workspace_root = Path(workspace_root or base_dir).resolve()
    mensaje_procesado = mensaje
    archivos_leidos = []

    patron = re.compile(r"@file:(?P<ruta>.+?)(?=(?:\s@file:)|$)")

    for coincidencia in patron.finditer(mensaje_procesado):
        raw_path = coincidencia.group("ruta").strip()
        raw_path = raw_path.rstrip(".,;:!? ")

        if raw_path.startswith(("\"", "'")) and raw_path.endswith(("\"", "'")) and len(raw_path) >= 2:
            raw_path = raw_path[1:-1]

        ruta_archivo = resolver_ruta_archivo(raw_path, base_dir=base_dir, workspace_root=workspace_root)

        if ruta_archivo is None:
            reemplazo = f"\n\n[Referencia a archivo no encontrada: {raw_path}]\n"
        else:
            try:
                contenido = ruta_archivo.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                contenido = ruta_archivo.read_text(encoding="latin-1")

            reemplazo = (
                f"\n\n[Instrucción cargada desde archivo: {ruta_archivo.name}]\n"
                f"{contenido}\n"
            ) 
            archivos_leidos.append({
                "nombre": ruta_archivo.name,
                "ruta": str(ruta_archivo),
                "contenido": contenido,
            })

        mensaje_procesado = (
            mensaje_procesado[:coincidencia.start()]
            + reemplazo
            + mensaje_procesado[coincidencia.end():]
        )

    return mensaje_procesado, archivos_leidos

def aplicar_formato_markdown(paragraph, texto):
    """
    Procesa texto básico de markdown (negritas y cursivas) y lo aplica a un párrafo de PowerPoint.
    """
    if not texto:
        return

    paragraph.text = ""
    # Pattern to find **bold**, __bold__, *italic*, or _italic_
    pattern = r"(\*\*.*?\*\*|__.*?__|\*.*?\*|_.*?_)"
    parts = re.split(pattern, texto)

    for part in parts:
        if not part:
            continue

        if (part.startswith("**") and part.endswith("**")) or (part.startswith("__") and part.endswith("__")):
            run = paragraph.add_run()
            run.text = part[2:-2]
            run.font.bold = True
        elif (part.startswith("*") and part.endswith("*")) or (part.startswith("_") and part.endswith("_")):
            run = paragraph.add_run()
            run.text = part[1:-1]
            run.font.italic = True
        else:
            run = paragraph.add_run()
            run.text = part

 
# ============================================================
#  INICIALIZACIÓN DEL SERVIDOR MCP
# ============================================================

mcp = FastMCP("MiAgenteLocal")

# --- Definición de Herramientas (Tools) ---
@mcp.tool()
def crear_presentacion(
    plantilla_path: str,
    reemplazos: dict,
    contenido_slides: list,
    nombre_archivo: str = "presentacion_plantilla.pptx",
    
) -> str:
    """
    Se crea una presentación basándose en una plantilla, reemplazando marcadores de posición y añadiendo diapositivas adicionales.

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
        normalize_newlines = lambda text: text.replace("\\n", "\n") if isinstance(text, str) else text

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
                        aplicar_formato_markdown(p, normalize_newlines(point))
                else:
                    tf = body.text_frame
                    tf.text = ""
                    p = tf.paragraphs[0] if tf.paragraphs else tf.add_paragraph()
                    aplicar_formato_markdown(p, normalize_newlines(str(text_content)))

        prs.save('PPTX/' + nombre_archivo)
        return f"Presentación desde plantilla creada exitosamente: {nombre_archivo}"
    except Exception as e:
        return f"Error al crear la presentación desde plantilla: {str(e)}"

@mcp.tool()
def read_file(path: str):
    """
    Lee el contenido de un archivo dentro del workspace o por ruta absoluta.
    """
   
    ruta_archivo = resolver_ruta_archivo(path, base_dir=os.getcwd(), workspace_root=os.getcwd())
    if ruta_archivo is None:
        return {"path": path, "error": "Archivo no encontrado"}

    try:
        contenido = ruta_archivo.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        contenido = ruta_archivo.read_text(encoding="latin-1")
        
    return {"path": str(ruta_archivo), "content": contenido}

@mcp.tool()
def generar_correos_ausentes(
    fecha: str = "2026-08-26",
    excel: str = "AUSENTE.xlsx",
    plantilla: str = "carta_ausentes.txt",
    plantilla_talento: str = "carta_talento.txt",
    remitente: str = "rolando.montero@colsanjavier.cl",
    enviar: bool = False,
    borradores: bool = True,
) -> str:
    """
    Genera borradores o envía correos de ausentes desde Excel y una plantilla.
    """
    from ausentes import generar_correos_ausentes
    return generar_correos_ausentes(
        fecha=fecha,
        excel=excel,
        plantilla=plantilla,
        plantilla_talento=plantilla_talento,
        remitente=remitente,
        enviar=enviar,
        borradores=borradores,
    )

# Si ejecutamos este script directamente, arranca el servidor MCP
if __name__ == "__main__":
    mcp.run()
