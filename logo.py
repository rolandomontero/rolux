from rich.console import Console
from rich.text import Text
import os

console = Console()


class Color:
    # Transformados de ANSI 256 a Hexadecimal
    USER = "#33CCFF"  # Cian brillante
    ASSISTANT = "#FFFF00"  # Amarillo/Oro
    TOOL = "#FFB74D"  # Naranja/Dorado
    GRAY = "#8C8C8C"  # Gris
    ORANGE = "#D97757"  # Naranja (ya era hex)
    GREEN = "#00FF00"  # Verde brillante
    RESET = "#FFFFFF"  # Blanco


__all__ = ["console", "Color", "mostrar_logo"]

avatar = [
    "  o  o        ",
    " o  ===o== o  ",
    "     |o |     ",
    "     | o|     ",
    "    ╱   o╲    ",
    "   ╱ ~~~~ ╲   ",
    "  |▒▒▒▒▒▒▒▒|  ",
    "  ╰────────╯  ",
]


# Usamos console.print con el parámetro style para consistencia total


def mostrar_logo(model):
    """Muestra el logo y el banner inicial del asistente."""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    ancho = console.size.width
    console.print(f"[{Color.USER}]{'=' * ancho}[/{Color.USER}]")

    # Definición del texto formateado
    text_0 = Text()
    text_0.append("Rolux UTP", style="bold green")
    text_0.append(" v0.1.2126", style="dim white")

    text_1 = Text(f"{model} · API Usage Billing", style="dim white")
    text_2 = Text(os.getcwd(), style="dim white")

    text_3 = Text("Powered by MC Lautaro's (c) 2026", style="dim white")
    text_4 = Text("================================", style=Color.GRAY)
    text_5 = Text("Asistente Pedagógico para el Aula", style=Color.GREEN)
    texts = ["", text_0, text_1, text_2, text_4, text_3, text_4, text_5]

    for img_line, txt in zip(avatar, texts):
        console.print(f"[{Color.GREEN}]{img_line}[/{Color.GREEN}]   ", end="")
        console.print(txt)

    console.print(f"[{Color.USER}]{'=' * ancho}[/{Color.USER}]")
    console.print("\n\n")


if __name__ == "__main__":
    mostrar_logo("gemma4:31b-cloud") # Ejemplo de uso
