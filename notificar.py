"""Genera y envía avisos de evaluaciones atrasadas desde una planilla Excel.

En Windows utiliza Outlook instalado localmente mediante pywin32. El modo
predeterminado solo muestra una vista previa; para enviar se debe indicar
--enviar explícitamente.
"""

# python google_sheets_monitor.py "https://docs.google.com/spreadsheets/d/1o_RJX87N5u1wD5czzztli-RAt-sFYF_k" --curso "1EM-B"


from __future__ import annotations

import argparse
import json
import re
from datetime import date, datetime, time
from pathlib import Path

import openpyxl
import win32com.client

PLANILLA_CATALOGO = "https://docs.google.com/spreadsheets/d/1o_RJX87N5u1wD5czzztli-RAt-sFYF_k"

CORREO_COPIA_FIJO = "crojas@colsanjavier.cl; guillermo.garcia@colsanjavier.cl;"
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
    for formato in ("%Y-%m-%d", "%d/%m/%Y","%d-%m-%Y"):
        try:
            return datetime.strptime(valor, formato).date()
        except ValueError:
            continue
    raise argparse.ArgumentTypeError("La fecha debe tener formato AAAA-MM-DD o DD/MM/AAAA")


def limpiar_correo(valor: object) -> str | None:
    correo = str(valor or "").strip()
    return correo if CORREO_RE.fullmatch(correo) else None


def formatear_hora(valor: object) -> str:
    if isinstance(valor, datetime):
        return valor.strftime("%H:%M")
    if isinstance(valor, time):
        return valor.strftime("%H:%M")
    return str(valor or "").strip()[:5]


def obtener_datos_curso(ruta_pj: Path, nombre_curso: str) -> dict[str, str] | None:
    """Devuelve los datos del curso indicado en pj.json."""
    datos = json.loads(ruta_pj.read_text(encoding="utf-8"))
    curso_buscado = nombre_curso.strip().casefold()
    return next(
        (
            curso
            for curso in datos.get("CURSOS", [])
            if str(curso.get("Curso", "")).strip().casefold() == curso_buscado
        ),
        None,
    )


def construir_mensaje(plantilla: str, fila: dict[str, object], hora, fecha: date) -> str:
    tratamiento = "a" if str(fila.get("S", "")).strip().lower() == "a" else "o"
    reemplazos = {
        "[Alumno]": str(fila["Alumno"]).strip(),
        "[S]": tratamiento,
        "[fecha]": f"{DIAS[fecha.weekday()]} {fecha.day} de {MESES[fecha.month - 1]}",
        "[hora]": str(hora).strip() if hora else "   ",
        "[dd]": str(fecha.day),
        "[mes]": MESES[fecha.month - 1],
        "[Contenido]": str(fila["Contenido"]).strip() if fila.get("Contenido") else "   ",
    }
    for marcador, valor in reemplazos.items():
        plantilla = plantilla.replace(marcador, valor)
    return plantilla


def cargar_mensajes(ruta_excel: Path, ruta_plantilla: Path) -> list[dict[str, str]]:
    libro = openpyxl.load_workbook(ruta_excel, data_only=True, read_only=True)
    hoja = libro.active
    encabezados = [str(celda.value or "").strip() for celda in next(hoja.iter_rows())]
    requeridos = {
       "Enviar", "Curso","Alumno", "email alumno", "Mail Padre", "Mail Madre", "S", "fecha", "hora", "Contenido"
    }
    faltantes = requeridos - set(encabezados)
    if faltantes:
        raise ValueError(f"Faltan columnas en la planilla: {', '.join(sorted(faltantes))}")

    plantilla = ruta_plantilla.read_text(encoding="utf-8")
    ruta_pj = Path(__file__).parent / "pj.json"
    mensajes = []
    for numero_fila, valores in enumerate(hoja.iter_rows(min_row=2, values_only=True), start=2):
        fila = dict(zip(encabezados, valores))
        alumno = str(fila.get("Alumno") or "").strip()
        nombre_curso = str(fila.get("Curso") or "").strip()
        datos_curso = obtener_datos_curso(ruta_pj, nombre_curso)
        fecha = fila.get("fecha")
        if isinstance(fecha, datetime):
            fecha = fecha.date()
        hora = formatear_hora(fila.get("hora"))
        destinatario = limpiar_correo(fila.get("email alumno")) # email alumno
        enviar = str(fila.get("Enviar") or "").strip().lower() == "si"
        if not alumno or not destinatario:
            print(f"Fila {numero_fila}: omitida por alumno o correo principal inválido")
            continue
        if not enviar:
            print(f"Fila {numero_fila}: omitida por columna 'Enviar' distinta de 'si'")
            continue
        

        copia = []
        for columna in ("Mail Padre", "Mail Madre"):
            correo = limpiar_correo(fila.get(columna))
            if correo and correo.lower() not in {item.lower() for item in copia}:
                copia.append(correo)
            elif fila.get(columna):
                print(f"Fila {numero_fila}: correo inválido omitido en {columna}: {fila[columna]}")
        

        if CORREO_COPIA_FIJO.lower() not in {item.lower() for item in copia}:
            copia.append(CORREO_COPIA_FIJO)

        copia.append(str(datos_curso.get("email", "")) if datos_curso else "")
        copia.append(str(datos_curso.get("email_psicopedagogo", "")) if datos_curso else "")

        mensajes.append({
            "alumno": alumno,
            "curso": nombre_curso,
            "para": destinatario,
            "cc": "; ".join(copia),
            "cuerpo": construir_mensaje(plantilla, fila, hora, fecha),
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


def ejecutar(mensajes: list[dict[str, str]], remitente: str) -> None:
    
    outlook = win32com.client.Dispatch("Outlook.Application")
    cuenta = obtener_cuenta_outlook(outlook, remitente) if outlook else None
    for mensaje in mensajes:
        asunto = f"Prueba atrasada | {mensaje['alumno']} | {mensaje['curso']}"
        # print(f"Para: {mensaje['para']};{mensaje['cc']}\n\n")
        print(asunto)
        # print(f"\n\n{mensaje['cuerpo']}\n\n")
        print("="*30)

        if not outlook:
            print(f"\n--- {asunto} ---\n No hay Outlook disponible; no se puede enviar ni guardar borrador.\n")
            continue

        correo = outlook.CreateItem(0)
        correo.SendUsingAccount = cuenta
        correo.To = mensaje["para"]
        correo.CC = mensaje["cc"]
        correo.Subject = asunto
        correo.Body = mensaje["cuerpo"]

        # if enviar:
        #     #correo.Send()
        #     print(f"Enviado: {mensaje['alumno']}")
        # else:
        #     correo.Save()
        #     print(f"Guardado como borrador: {mensaje['alumno']}")
        correo.Save()
        carpeta_borradores = (
                     cuenta.DeliveryStore.GetDefaultFolder(OL_FOLDER_DRAFTS))
        
        correo = correo.Move(carpeta_borradores)
           


def main() -> None:
    mensajes = cargar_mensajes(Path("AUSENTE.xlsx"), Path("carta_ausentes.txt"))
    print(f"Mensajes preparados: {len(mensajes)}")
    ejecutar(mensajes, remitente=CORREO_REMITENTE)


if __name__ == "__main__":
    main()