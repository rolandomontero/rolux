# cliente_claude_console.py
import os
import json
import ollama
import logging 

# Tools MCP reales
from servidor_mcp import crear_presentacion_desde_plantilla
# ---------------------------------------------------------
# 1) DESACTIVAR LOGS DE OLLAMA Y HTTPX
# ---------------------------------------------------------
logging.getLogger("ollama").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("httpcore").setLevel(logging.ERROR)

# Opcional: silenciar todos los logs del sistema
# logging.basicConfig(level=logging.CRITICAL)

# ============================================================
# 1) COLORES ESTILO CLAUDE
# ============================================================

class Color:
    USER = "\033[38;5;81m"
    ASSISTANT = "\033[38;5;220m"
    TOOL = "\033[38;5;214m"
    RESET = "\033[0m"
    GRAY = "\033[38;5;245m"


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


# ============================================================
# 3) TOOLS DISPONIBLES
# ============================================================

TOOLS = {

    "crear_presentacion_desde_plantilla": crear_presentacion_desde_plantilla,
}


# ============================================================
# 4) FUNCIÓN PRINCIPAL DE CHAT ESTILO CLAUDE
# ============================================================

def claude_chat(modelo, mensaje_usuario):
    contexto = cargar_contexto()

    print(f"{Color.ASSISTANT}Claude‑Local:{Color.RESET} ", end="", flush=True)

    # Inicio Chat con el modelo, habilitando el streaming
    stream = ollama.chat(
        model=modelo,
        stream=True,
        messages=[
            {"role": "system", "content": contexto},
            {"role": "user", "content": mensaje_usuario}
        ]
    )

    for parte in stream:
        msg = parte.get("message", {})

        # ------------------------------
        # STREAM NORMAL
        # ------------------------------
        if "content" in msg:
            print(msg["content"], end="", flush=True)

        # ------------------------------
        # TOOL CALLS
        # ------------------------------
        if "tool_calls" in msg:
            for llamada in msg["tool_calls"]:
                nombre = llamada["function"]["name"]
                args = llamada["function"].get("arguments", {})
                tool_id = llamada["id"]

                print(f"\n{Color.TOOL}[Tool → {nombre}]{Color.RESET}")

                if nombre not in TOOLS:
                    print(f"{Color.GRAY}Tool no registrada: {nombre}{Color.RESET}")
                    continue

                resultado = TOOLS[nombre](**args)

                follow = ollama.chat(
                    model=modelo,
                    stream=True,
                    messages=[
                        {"role": "system", "content": contexto},
                        {"role": "user", "content": mensaje_usuario},
                        {
                            "role": "tool",
                            "tool_call_id": tool_id,
                            "content": json.dumps(resultado)
                        }
                    ]
                )

                print(f"{Color.ASSISTANT}Claude‑Local:{Color.RESET} ", end="", flush=True)

                for f in follow:
                    if "content" in f.get("message", {}):
                        print(f["message"]["content"], end="", flush=True)

    print("\n")


# ============================================================
# 5) LOOP INTERACTIVO ESTILO CLAUDE
# ============================================================
# 1. Configuración del modelo (Asegúrate de tenerlo: `ollama pull llama3.2`)
MODELO = "gemma4:31b-cloud" # "qwen3:0.6b" 
def iniciar_consola():
    print(f"{Color.GRAY}=== Claude‑Local (Ollama + MCP) ==={Color.RESET}")
    print(f"{Color.GRAY}Escribe 'salir' para terminar.{Color.RESET}")

    while True:
        try:
            user = input(f"{Color.USER}Tú:{Color.RESET} ")
        except KeyboardInterrupt:
            print("\nSaliendo…")
            break

        if user.lower() in ["salir", "exit", "quit"]:
            break

        claude_chat(MODELO, user)


if __name__ == "__main__":
    iniciar_consola()
