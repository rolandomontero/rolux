"""Genera y envía avisos de evaluaciones atrasadas desde una planilla Excel.

En Windows utiliza Outlook instalado localmente mediante pywin32. El modo
predeterminado solo muestra una vista previa; para enviar se debe indicar
--enviar explícitamente.
"""

from __future__ import annotations

import argparse
import re
from datetime import date, datetime
from pathlib import Path

import openpyxl
import win32com.client


CORREO_COPIA_FIJO = "crojas@colsanjavier.cl"
CORREO_REMITENTE = "rolando.montero@colsanjavier.cl"
MESES = (
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
)
DIAS = ("lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo")
CORREO_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
OL_FOLDER_DRAFTS = 16


def parsear_fecha(valor: str) -> date:
    """Acepta una fecha ISO (AAAA-MM-DD) o el formato DD/MM/AAAA."""
    for formato in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(valor, formato).date()
        except ValueError:
            continue
    raise argparse.ArgumentTypeError("La fecha debe tener formato AAAA-MM-DD o DD/MM/AAAA")


def limpiar_correo(valor: object) -> str | None:
    correo = str(valor or "").strip()
    return correo if CORREO_RE.fullmatch(correo) else None


def construir_mensaje(plantilla: str, fila: dict[str, object], fecha: date) -> str:
    tratamiento = "a" if str(fila.get("S", "")).strip().lower() == "a" else "o"
    reemplazos = {
        "[Alumno]": str(fila["Alumno"]).strip(),
        "[S]": tratamiento,
        "[fecha]": f"{DIAS[fecha.weekday()]} {fecha.day} de {MESES[fecha.month - 1]}",
        "[dd]": str(fecha.day),
        "[mes]": MESES[fecha.month - 1],
        "[Contenido]": str(fila["Contenido"]).strip() if fila.get("Contenido") else "   ",
    }
    for marcador, valor in reemplazos.items():
        plantilla = plantilla.replace(marcador, valor)
    return plantilla


def cargar_mensajes(ruta_excel: Path, ruta_plantilla: Path, fecha: date) -> list[dict[str, str]]:
    libro = openpyxl.load_workbook(ruta_excel, data_only=True, read_only=True)
    hoja = libro.active
    encabezados = [str(celda.value or "").strip() for celda in next(hoja.iter_rows())]
    requeridos = {
        "Alumno", "email alumno", "Mail Padre", "Mail Madre", "S", "PJ", "JD", "Curso","Contenido"
    }
    faltantes = requeridos - set(encabezados)
    if faltantes:
        raise ValueError(f"Faltan columnas en la planilla: {', '.join(sorted(faltantes))}")

    plantilla = ruta_plantilla.read_text(encoding="utf-8")
    mensajes = []
    for numero_fila, valores in enumerate(hoja.iter_rows(min_row=2, values_only=True), start=2):
        fila = dict(zip(encabezados, valores))
        alumno = str(fila.get("Alumno") or "").strip()
        destinatario = limpiar_correo(fila.get("email alumno")) # email alumno
        if not alumno or not destinatario:
            print(f"Fila {numero_fila}: omitida por alumno o correo principal inválido")
            continue

        copia = []
        for columna in ("Mail Padre", "Mail Madre", "PJ", "JD"):
            correo = limpiar_correo(fila.get(columna))
            if correo and correo.lower() not in {item.lower() for item in copia}:
                copia.append(correo)
            elif fila.get(columna):
                print(f"Fila {numero_fila}: correo inválido omitido en {columna}: {fila[columna]}")
        if CORREO_COPIA_FIJO.lower() not in {item.lower() for item in copia}:
            copia.append(CORREO_COPIA_FIJO)

        mensajes.append({
            "alumno": alumno,
            "curso": str(fila.get("Curso") or "").strip(),
            "para": destinatario,
            "cc": "; ".join(copia),
            "cuerpo": construir_mensaje(plantilla, fila, fecha),
        })
    return mensajes


def obtener_cuenta_outlook(outlook: object, remitente: str) -> object:
    for cuenta in outlook.Session.Accounts:
        if str(cuenta.SmtpAddress).strip().lower() == remitente.lower():
            return cuenta
    raise RuntimeError(
        f"La cuenta {remitente} no está configurada en Outlook. "
        "Agrégala al perfil de Outlook antes de usar --enviar o --borradores."
    )


def ejecutar(mensajes: list[dict[str, str]], enviar: bool, borradores: bool, remitente: str) -> None:
    print(f"Preparando para {'enviar' if enviar else 'guardar borradores' if borradores else 'mostrar vista previa'}...\n\n")
    outlook = win32com.client.Dispatch("Outlook.Application") if (enviar or borradores) else None
    cuenta = obtener_cuenta_outlook(outlook, remitente) if outlook else None
    for mensaje in mensajes:
        asunto = f"Prueba atrasada | {mensaje['alumno']} | {mensaje['curso']}"
        # print(f"Para: {mensaje['para']};{mensaje['cc']}\n\n")
        # print(asunto)
        # print(f"\n\n{mensaje['cuerpo']}\n\n")
        # print("="*30)

        if not outlook:
            print(f"\n--- {asunto} ---\n No hay Outlook disponible; no se puede enviar ni guardar borrador.\n")
            continue

        correo = outlook.CreateItem(0)
        correo.SendUsingAccount = cuenta
        correo.To = mensaje["para"]
        correo.CC = mensaje["cc"]
        correo.Subject = asunto
        correo.Body = mensaje["cuerpo"]

        if enviar:
            #correo.Send()
            print(f"Enviado: {mensaje['alumno']}")
        else:
            correo.Save()
            print(f"Guardado como borrador: {mensaje['alumno']}")

        carpeta_borradores = (
                     cuenta.DeliveryStore.GetDefaultFolder(OL_FOLDER_DRAFTS))
        
        correo = correo.Move(carpeta_borradores)
        
            


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fecha", type=parsear_fecha, required=True, help="Fecha de la evaluación, por ejemplo 2026-08-29 (predeterminada: 2026-08-26)")
    parser.add_argument("--excel", type=Path, default=Path("AUSENTE.xlsx"))
    parser.add_argument("--plantilla", type=Path, default=Path("carta_ausentes.txt"))
    parser.add_argument("--remitente", default=CORREO_REMITENTE, help=f"Cuenta de Outlook que enviará los correos (predeterminada: {CORREO_REMITENTE})")
    grupo = parser.add_mutually_exclusive_group()
    grupo.add_argument("--enviar", action="store_true", help="Envía los correos mediante Outlook")
    grupo.add_argument("--borradores", action="store_true", help="Guarda los correos en Borradores de Outlook")
    args = parser.parse_args()

    mensajes = cargar_mensajes(args.excel, args.plantilla, args.fecha)
    print(f"Mensajes preparados: {len(mensajes)}")
    ejecutar(mensajes, enviar=args.enviar, borradores=args.borradores, remitente=args.remitente)


if __name__ == "__main__":
    main()