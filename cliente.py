import datetime
import logging
import os
import ollama
import logo
from httpx import Timeout, HTTPError
from servidor_mcp import crear_presentacion, read_file, procesar_referencias_archivo
from logo import Color, console

# ---------------------------------------------------------
# 1) DESACTIVAR LOGS DE OLLAMA Y HTTPX
# ---------------------------------------------------------
logging.getLogger("ollama").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("httpcore").setLevel(logging.ERROR)

# Opcional: silenciar todos los logs del sistema
# logging.basicConfig(level=logging.CRITICAL)

# ============================================================
# 2) CARGA DE SKILLS Y AGENTES
# ============================================================

def cargar_md(path):
    contenido = ""
    if not os.path.exists(path):
        return contenido

    for archivo in os.listdir(path):
        if archivo.endswith(".md"):
            with open(os.path.join(path, archivo), "r", encoding="utf-8") as f:
                contenido += f"\n\n# Archivo: {archivo}\n" + f.read()
    return contenido


def cargar_contexto():
    skills = cargar_md("skills")
    agentes = cargar_md("edu-presentation-architect.md") #("agentes")

    return f"""
Eres un agente MCP local. Usa herramientas cuando sea necesario.
Sigue las reglas definidas en los agentes y skills cargados.

## SKILLS:
{skills}

## AGENTES:
{agentes}
"""


# ---------------------------------------------------------
# 1) SKILL: generar_clase_ppt (envoltorio pedagógico)
# ---------------------------------------------------------

def skill_generar_clase_ppt(
    asignatura: str,
    tema: str,
    curso: str,
    unidad: str = "",
    plantilla_path: str = "PLANTILLA_QCA.pptx",
    contenido_slides: list | None = None,
    nombre_archivo: str | None = None,
    fecha: str | None = None,
):
    """
    Skill pedagógico que:
    - construye placeholders para la plantilla
    - arma la estructura de diapositivas
    - llama a crear_presentacion_desde_plantilla
    """

    if fecha is None:
        fecha = datetime.date.today().strftime("%d-%m-%Y")

    if not nombre_archivo:
        nombre_archivo = f"Clase_{asignatura}_{tema.replace(' ', '_')}.pptx"

    # 1) Placeholders de la plantilla
    reemplazos = {
        "{{NC}}": "10",
        "{{CURSO}}": curso,
        "{{FECHA}}": fecha,
        "{{ASIGNATURA}}": asignatura,
        "{{UNIDAD}}": unidad if unidad else f"Unidad: {tema}",
        "{{CONTENIDOS}}": tema,
        "{{HABILIDADES}}": "Análisis, reflexión, comunicación científica",
        "{{VIRTUD}}": "RESPONSABILIDAD",
        "{{OA}}": f"Comprender y aplicar conceptos clave sobre {tema.lower()}.",
        "{{OC}}": f"Al finalizar la clase, el estudiante será capaz de explicar y ejemplificar {tema.lower()}.",
    }

    # 2) Estructura pedagógica básica (puedes ajustarla a tu estilo)
    if contenido_slides is None:
        contenido_slides = [
            {
                "titulo": f"{asignatura}: {tema}",
                "cuerpo": f"Curso: {curso}\nFecha: {fecha}",
            },
            {
            "titulo": "Objetivo de la clase",
            "cuerpo": reemplazos["{{OC}}"],
        },
        {
            "titulo": "Activación de conocimientos previos",
            "cuerpo": [
                "¿Qué recuerdas de clases anteriores relacionadas con este tema?",
                "Comenta un ejemplo de la vida cotidiana donde aparezca este contenido.",
            ],
        },
        {
            "titulo": f"Conceptos clave sobre {tema}",
            "cuerpo": [
                "Definición principal.",
                "Características fundamentales.",
                "Importancia en el contexto de la asignatura.",
            ],
        },
        {
            "titulo": "Ejemplos guiados",
            "cuerpo": [
                "Ejemplo 1 explicado paso a paso.",
                "Ejemplo 2 con participación de los estudiantes.",
            ],
        },
        {
            "titulo": "Actividad individual o en parejas",
            "cuerpo": [
                "Resolver una situación problema relacionada con el tema.",
                "Registrar el procedimiento y la conclusión.",
            ],
        },
        {
            "titulo": "Puesta en común",
            "cuerpo": [
                "Socializar respuestas.",
                "Comparar estrategias de resolución.",
            ],
        },
        {
            "titulo": "Cierre de la clase",
            "cuerpo": [
                "Síntesis de las ideas principales.",
                "Preguntas finales de verificación.",
            ],
        },
        {
            "titulo": "Reflexión",
            "cuerpo": [
                "¿Qué fue lo más importante que aprendiste hoy?",
                "¿En qué situaciones podrías aplicar este conocimiento?",
            ],
        },
    ]

    # 3) Llamada a la tool real del MCP
    crear_presentacion(
        plantilla_path=plantilla_path,
        reemplazos=reemplazos,
        contenido_slides=contenido_slides,
        nombre_archivo=nombre_archivo,
    )

    return {
        "status": "ok",
        "archivo": nombre_archivo,
        "plantilla": plantilla_path,
        "tema": tema,
        "curso": curso,
    }


# ---------------------------------------------------------
# 2) DEFINICIÓN DE TOOLS PARA OLLAMA
# ---------------------------------------------------------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "generar_clase_ppt",
            "description": (
                "Genera una clase en PowerPoint usando una plantilla y la tool "
                "`crear_presentacion` del servidor MCP."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "asignatura": {
                        "type": "string",
                        "description": "Asignatura, por ejemplo 'Química', 'Física', 'Matemáticas'.",
                    },
                    "tema": {
                        "type": "string",
                        "description": "Tema central de la clase, por ejemplo 'Enlaces iónicos'.",
                    },
                    "curso": {
                        "type": "string",
                        "description": "Nivel o curso, por ejemplo '2° Medio'.",
                    },
                    "unidad": {
                        "type": "string",
                        "description": "Unidad curricular, opcional.",
                    },
                    "contenido_slides": {
                        "type": "array",
                        "description": "Lista de diapositivas con título y contenido.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "titulo": {"type": "string"},
                                "cuerpo": {"type": "string"},
                            },
                            "required": ["titulo", "cuerpo"],
                        },
                    },
                    "plantilla_path": {
                        "type": "string",
                        "description": "Ruta al archivo de plantilla .pptx.",
                        "default": "PLANTILLA_QCA.pptx",
                    },
                    "nombre_archivo": {
                        "type": "string",
                        "description": "Nombre del archivo de salida [<número de clase>_<fecha>_<tema>].pptx.",
                    },
                },
                "required": ["asignatura", "tema", "curso"],
            },
        },
    }
]


# ---------------------------------------------------------
# 3) BUCLE DEL AGENTE
# ---------------------------------------------------------

def despachar_tool(name: str, arguments: dict):
    if name == "generar_clase_ppt":
        return skill_generar_clase_ppt(**arguments)
    else:
        raise ValueError(f"Tool desconocida: {name}")




# 1. Configuración del modelo (Asegúrate de tenerlo: `ollama pull llama3.2`)
MODELO = "gemma4:31b-cloud" # "qwen3:0.6b" # "qwen3:0.6b" 

def ciclo_agente(model: str = MODELO):
    logo.mostrar_logo()
    contexto = cargar_contexto()
    print(f"Agente de clases PPT listo con {model}.\nEscribe 'salir' para terminar.\n")

    historial = [{"role": "system", "content": contexto}]

    while True:
        user_input = input("Tú: ")
        if user_input.lower().strip() in {"salir", "exit", "quit"}:
            break


        mensaje_procesado, archivos_leidos = procesar_referencias_archivo(
        user_input,
        base_dir=os.getcwd(),
        workspace_root=os.getcwd(), )

        if archivos_leidos:
            console.print(f"[{Color.GRAY}][Archivos cargados: {', '.join(archivo['nombre'] for archivo in archivos_leidos)}][/{Color.GRAY}]")

        historial.append({"role": "user", "content": mensaje_procesado})
        print("[Agente] Procesando tu solicitud...")
        
        respuesta = ollama.chat(
            model=model,
            messages=historial,
            tools=TOOLS,
        )

        # ¿El modelo pidió usar una tool?
        tool_calls = respuesta.get("message", {}).get("tool_calls", [])

        if tool_calls:
            for call in tool_calls:
                tool_name = call["function"]["name"]
                args = call["function"].get("arguments", {}) or {}
                print(f"[Agente] Ejecutando tool: {tool_name} con args: {args}")

                resultado_tool = despachar_tool(tool_name, args)

                historial.append(
                    {
                        "role": "tool",
                        "name": tool_name,
                        "content": str(resultado_tool),
                    }
                )

            # Segunda llamada al modelo, ahora con el resultado de la tool
            respuesta = ollama.chat(
                model=model,
                messages=historial,
            )

        contenido = respuesta.get("message", {}).get("content", "")
        historial.append({"role": "assistant", "content": contenido})
        print(f"Agente: {contenido}\n")


if __name__ == "__main__":
    ciclo_agente()
