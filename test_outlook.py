"""Prueba la automatización COM del Outlook clásico sin enviar correos."""

from __future__ import annotations

import sys

import pywintypes
import win32com.client

REMITENTE_PRUEBA = "rolando.montero@colsanjavier.cl"


def main() -> int:
    print("1. Intentando conectar con Outlook.Application...")
    try:
        outlook = win32com.client.Dispatch("Outlook.Application")
    except pywintypes.com_error as error:
        print("ERROR: Outlook no está disponible mediante COM.")
        print(f"Detalle: {error}")
        print("Comprueba que Outlook clásico esté instalado y configurado.")
        print("El Nuevo Outlook no admite esta automatización COM.")
        return 1

    print("OK: conexión COM establecida.")
    print("\n2. Cuentas visibles para COM:")
    cuentas = list(outlook.Session.Accounts)
    if not cuentas:
        print("  (ninguna)")
    else:
        for cuenta in cuentas:
            print(f"  - {cuenta.SmtpAddress}")

    print("\n3. Intentando crear un correo de prueba...")
    try:
        correo = outlook.CreateItem(0)
        cuenta_remitente = next(
            (
                cuenta
                for cuenta in cuentas
                if str(cuenta.SmtpAddress).strip().lower() == REMITENTE_PRUEBA.lower()
            ),
            None,
        )
        if cuenta_remitente is None:
            print(f"ERROR: no se encontró la cuenta {REMITENTE_PRUEBA}.")
            return 1
        OL_FOLDER_DRAFTS = 16
        correo.SendUsingAccount = cuenta_remitente
        correo.Subject = "Prueba COM de Outlook (no enviado)"
        correo.Body = "Este mensaje solo comprueba la automatización COM."
        correo.To = 'rolandomontero@hotmail.com'#REMITENTE_PRUEBA
        correo.Send()
        carpeta_borradores = (
             cuenta_remitente.DeliveryStore.GetDefaultFolder(OL_FOLDER_DRAFTS))

        correo = correo.Move(carpeta_borradores)


        print(f"OK: remitente seleccionado: {cuenta_remitente.SmtpAddress}")
        print("OK: elemento de correo creado; no se guardó ni envió.")
    except pywintypes.com_error as error:
        print("ERROR: COM conectó, pero no pudo crear el correo.")
        print(f"Detalle: {error}")
        return 1

    print("\nDiagnóstico finalizado correctamente.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
