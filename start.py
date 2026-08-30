# cliente_claude_console.py
import os
import sys
import json
import logging

import ollama
import logo
from logo import Color, console
from rich.markdown import Markdown

# Tools MCP reales
import servidor_mcp
from tools import TOOL_IMPL, OLLAMA_TOOLS

# ---------------------------------------------------------
# 1) DESACTIVAR LOGS DE OLLAMA Y HTTPX
# ---------------------------------------------------------
logging.getLogger("ollama").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("httpcore").setLevel(logging.ERROR)

# Opcional: silenciar todos los logs del sistema
# logging.basicConfig(level=logging.CRITICAL)


def duracion(nanosegundos: int) -> str:
    """Convierte nanosegundos a mm:ss o hh:mm:ss"""
    segundos = nanosegundos / 1_000_000_000
    segundos = int(segundos)
    h, resto = divmod(segundos, 3600)
    m, s = divmod(resto, 60)
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def tokens(n: int) -> str:
    """Convierte tokens a formato '120k', '1.5M', etc."""
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M".replace(".0M", "M")
    if n >= 1_000:
        return f"{n/1_000:.0f}k"
    return str(n)


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


def _extract_message(respuesta):
    """Normaliza la extracción del campo 'message' desde distintos tipos de respuesta.
    Algunas versiones de la librería `ollama` devuelven objetos con atributos, otras dicts.
    """
    if respuesta is None:
        return {}
    # Si es un dict-like
    try:
        if isinstance(respuesta, dict):
            return respuesta.get("message", {}) or {}
    except Exception:
        pass
    # Si tiene atributo 'message'
    if hasattr(respuesta, "message"):
        try:
            return getattr(respuesta, "message") or {}
        except Exception:
            return {}
    # Si tiene método to_dict
    if hasattr(respuesta, "to_dict"):
        try:
            return respuesta.to_dict().get("message", {}) or {}
        except Exception:
            return {}
    return {}


def chat(modelo, mensaje_usuario):
    contexto = cargar_contexto()

    mensaje_procesado, archivos_leidos = servidor_mcp.procesar_referencias_archivo(
        mensaje_usuario,
        base_dir=os.getcwd(),
        workspace_root=os.getcwd(),
    )

    if archivos_leidos:
        console.print(
            f"[{Color.GRAY}] Archivos cargados: {', '.join(archivo['nombre'] for archivo in archivos_leidos)}[/{Color.GRAY}]"
        )

    historial = [
        {"role": "system", "content": contexto},
        {"role": "user", "content": mensaje_procesado},
    ]

    with console.status(
        "[bold green]Esperando respuesta del modelo...",
        spinner="dots",
        spinner_style="green",
    ):
        # Primera llamada: permitimos al modelo generar tool calls
        try:
            respuesta = ollama.chat(
                model=modelo,
                messages=historial,
                tools=OLLAMA_TOOLS,
            )
        except Exception as e:
            # Mostrar información amigable y registrar detalle para depuración
            console.print(
                f"[{Color.ASSISTANT}]❌ Error al comunicarse con el servidor de Ollama: {e}[/{Color.ASSISTANT}]"
            )
            # Si la excepción tiene atributos adicionales (ej. ResponseError), mostrar texto si existe
            try:
                err_text = getattr(e, "args", [str(e)])[0]
                console.print(f"[{Color.GRAY}]Detalles: {err_text}[/{Color.GRAY}]")
            except Exception:
                pass
            # terminar la función para evitar más errores
            return

    tokens_totales = (respuesta.prompt_eval_count or 0) + (respuesta.eval_count or 0)

    d = duracion(respuesta.total_duration or 0)
    t = tokens(tokens_totales)

    console.print(f"[{Color.GRAY}] duración : {d}[/{Color.GRAY}]")  # duración : 01:12
    console.print(f"[{Color.GRAY}] tokens   : {t}[/{Color.GRAY}]")  # tokens : 120k

    message = _extract_message(respuesta)
    tool_calls = (message or {}).get("tool_calls", [])

    if tool_calls:
        for llamada in tool_calls:
            nombre = llamada["function"]["name"]
            args = llamada["function"].get("arguments", {})

            console.print(
                f"[{Color.TOOL}] Llamando a la herramienta → {nombre}[/{Color.TOOL}]"
            )

            if nombre not in TOOL_IMPL:
                console.print(
                    f"[{Color.ASSISTANT}]Tool no registrada: {nombre}[/{Color.ASSISTANT}]"
                )
                continue

            resultado = TOOL_IMPL[nombre](**args)
            console.print(json.dumps(resultado, ensure_ascii=False, indent=2))

            historial.append(
                {"role": "tool", "name": nombre, "content": json.dumps(resultado)}
            )
            # Segunda llamada: el modelo recibe el resultado de la tool y puede confirmar o explicar
            explicacion  = logo.console.input(f"[{Color.ASSISTANT}]¿Quieres una explicación? [s/N]:[/{Color.ASSISTANT}] ")
            with console.status(
                "[bold green]Esperando respuesta del modelo tras la tool call...",
                spinner="simpleDots",
                spinner_style="green",
            ):
                try:
                    respuesta = ollama.chat(model=modelo, messages=historial) if explicacion.lower() == "s" else "None"
 
                except Exception as e:
                    console.print(
                        f"[{Color.ASSISTANT}]❌ Error tras la llamada a la herramienta: {e}[/{Color.ASSISTANT}]"
                    )
                    try:
                        err_text = getattr(e, "args", [str(e)])[0]
                        console.print(
                            f"[{Color.GRAY}]Detalles: {err_text}[/{Color.GRAY}]"
                        )
                    except Exception:
                        pass
                    # añadir una respuesta de error en el historial para que el modelo pueda continuar si es necesario
                    historial.append(
                        {
                            "role": "tool",
                            "name": nombre,
                            "content": json.dumps({"error": str(e)}),
                        }
                    )
                    # salir del bucle de tool_calls para evitar loops
                    break

    message = _extract_message(respuesta)
    contenido = (message or {}).get("content", "")
    if contenido:
        logo.console.print(f"[{Color.ASSISTANT}]👨‍🏫 Rolux:[/{Color.ASSISTANT}]")
        logo.console.print(Markdown(contenido))

    logo.console.print()


# ============================================================
# 5) LOOP INTERACTIVO ESTILO CLAUDE
# ============================================================


def iniciar_consola(modelo=None):
    # 1. Configuración del modelo (Asegúrate de tenerlo: `ollama pull llama3.2`)
    # MODELO = "gemma4:31b-cloud"  # "qwen3:0.6b"
    # MODELO = "qwen3:0.6b"  # Alternativa más ligera
    # MODELO = "minimax-m3:cloud"  # Alternativa más ligera
    MODELO = ["gemma4:31b-cloud", "qwen3:0.6b", "minimax-m3:cloud"][
        modelo if modelo is not None else 0
    ]  # Cambia el índice según el modelo deseado

    logo.mostrar_logo(MODELO)

    while True:
        try:
            user = logo.console.input(f"[{Color.USER}]Tú:[/{Color.USER}] ")
        except KeyboardInterrupt:
            logo.console.print("\nSaliendo… \n Gracias por usar Rolux. ¡Hasta luego!")
            break

        if user.lower() in ["salir", "exit", "quit"]:
            logo.console.print(
                f"\nSaliendo… \n [{Color.GREEN}]Gracias por usar Rolux. ¡Hasta luego!"
            )
            r=input("Presione Enter para salir...")
            break

        chat(MODELO, user)


def obtener_modelo(argv):
    args = {}
    for item in argv[1:]:
        if "=" in item:
            clave, valor = item.split("=", 1)
            args[clave] = valor

    valor = args.get("modelo", None)
    if valor in (None, ""):
        return 0
    try:
        return int(valor)
    except (TypeError, ValueError):
        return 0


if __name__ == "__main__":
    modelo = obtener_modelo(sys.argv)
    iniciar_consola(modelo)
