# cliente_claude_console.py
import os
import json
import logging

import ollama
import logo
from logo import Color, console
from rich.markdown import Markdown

# Tools MCP reales
import servidor_mcp

  
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
    agentes = cargar_md("agentes")

    return f"""
Eres un agente MCP local. Usa herramientas cuando sea necesario.
Sigue las reglas definidas en los agentes y skills cargados.

## SKILLS:
{skills}

## AGENTES:
{agentes}
"""


TOOL_IMPL = {
    "crear_presentacion_desde_plantilla": servidor_mcp.crear_presentacion,
    "read_file": servidor_mcp.read_file,
}

OLLAMA_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "crear_presentacion_desde_plantilla",
            "description": "Crea una presentación de PowerPoint usando una plantilla .pptx y contenido adicional.",
            "parameters": {
                "type": "object",
                "properties": {
                    "plantilla_path": {
                        "type": "string",
                        "description": "Ruta al archivo de plantilla .pptx.",
                    },
                    "reemplazos": {
                        "type": "object",
                        "description": "Diccionario con los marcadores y sus valores.",
                    },
                    "contenido_slides": {
                        "type": "array",
                        "description": "Lista de diapositivas con título y contenido.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "titulo": {"type": "string"},
                                "cuerpo": {
                                    "oneOf": [
                                        {"type": "string"},
                                        {"type": "array", "items": {"type": "string"}}
                                    ]
                                }
                            },
                            "required": ["titulo", "cuerpo"],
                        },
                    },
                    "nombre_archivo": {
                        "type": "string",
                        "description": "Nombre del archivo de salida .pptx.",
                    },
                },
                "required": ["plantilla_path", "reemplazos", "contenido_slides"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Lee el contenido de un archivo local y lo devuelve como texto.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Ruta al archivo a leer.",
                    }
                },
                "required": ["path"],
            },
        },
    },
]


def claude_chat(modelo, mensaje_usuario):
    contexto = cargar_contexto()

    mensaje_procesado, archivos_leidos = servidor_mcp.procesar_referencias_archivo(
        mensaje_usuario,
        base_dir=os.getcwd(),
        workspace_root=os.getcwd(),
    )

    if archivos_leidos:
        console.print(f"[{Color.GRAY}][Archivos cargados: {', '.join(archivo['nombre'] for archivo in archivos_leidos)}][/{Color.GRAY}]")

    historial = [
        {"role": "system", "content": contexto},
        {"role": "user", "content": mensaje_procesado},
    ]

    # Primera llamada: permitimos al modelo generar tool calls
    respuesta = ollama.chat(
        model=modelo,
        messages=historial,
        tools=OLLAMA_TOOLS,
    )

    tool_calls = respuesta.get("message", {}).get("tool_calls", [])

    if tool_calls:
        for llamada in tool_calls:
            nombre = llamada["function"]["name"]
            args = llamada["function"].get("arguments", {})

            console.print(f"\n[{Color.TOOL}][Tool → {nombre}][/{Color.TOOL}]")

            if nombre not in TOOL_IMPL:
                console.print(f"[{Color.ASSISTANT}]Tool no registrada: {nombre}[/{Color.ASSISTANT}]")
                continue

            resultado = TOOL_IMPL[nombre](**args)
            console.print(json.dumps(resultado, ensure_ascii=False, indent=2))

            historial.append(
                {"role": "tool", "name": nombre, "content": json.dumps(resultado)}
            )

        # Segunda llamada: el modelo recibe el resultado de la tool y puede confirmar o explicar
        respuesta = ollama.chat(
           model=modelo,
           messages=historial,
         )

    contenido = respuesta.get("message", {}).get("content", "")
    if contenido:
        logo.console.print(f"[{Color.ASSISTANT}]Rolux:[/{Color.ASSISTANT}]")
        logo.console.print(Markdown(contenido))
    else:
        logo.console.print(f"[{Color.ASSISTANT}]\n[/{Color.ASSISTANT}]")

    logo.console.print()


# ============================================================
# 5) LOOP INTERACTIVO ESTILO CLAUDE
# ============================================================
# 1. Configuración del modelo (Asegúrate de tenerlo: `ollama pull llama3.2`)
MODELO = "gemma4:31b-cloud" # "qwen3:0.6b" 
def iniciar_consola():
    logo.mostrar_logo()
    
    while True:
        try:
            user = logo.console.input(f"[{Color.USER}]Tú:[/{Color.USER}] ")
        except KeyboardInterrupt:
            logo.console.print("\nSaliendo… \n Gracias por usar Rolux. ¡Hasta luego!")
            break

        if user.lower() in ["salir", "exit", "quit"]:
            logo.console.print(f"\nSaliendo… \n [{Color.GREEN}]Gracias por usar Rolux. ¡Hasta luego!")
            break

        claude_chat(MODELO, user)


if __name__ == "__main__":
    iniciar_consola()