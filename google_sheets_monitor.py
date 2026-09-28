"""Consulta una hoja de Google con OAuth de usuario y detecta cambios en sus datos."""

from __future__ import annotations

import argparse
from io import BytesIO
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]
SHEET_ID_RE = re.compile(r"/spreadsheets/d/([a-zA-Z0-9_-]+)")


@dataclass(frozen=True)
class RowChange:
    kind: str
    row_number: int
    previous: list[Any] | None
    current: list[Any] | None


@dataclass(frozen=True)
class CheckResult:
    status: str
    changes: list[RowChange]

    @property
    def has_changes(self) -> bool:
        return bool(self.changes)


def extraer_id_planilla(valor: str) -> str:
    """Acepta el ID de la planilla o su URL completa."""
    coincidencia = SHEET_ID_RE.search(valor)
    spreadsheet_id = coincidencia.group(1) if coincidencia else valor.strip()
    if not spreadsheet_id or "/" in spreadsheet_id:
        raise ValueError("Indica el ID de la planilla o su URL de Google Sheets.")
    return spreadsheet_id


def _autenticar(credentials_file: Path, token_file: Path) -> Any:
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError as error:
        raise RuntimeError(
            "Faltan dependencias de Google. Instala las dependencias indicadas en "
            "requirements.txt."
        ) from error

    if not credentials_file.is_file():
        raise FileNotFoundError(
            f"No se encontró {credentials_file}. Descarga el cliente OAuth de escritorio "
            "de Google Cloud y guárdalo en esa ruta."
        )

    creds = None
    stored_scopes: set[str] = set()
    if token_file.is_file():
        stored_token = json.loads(token_file.read_text(encoding="utf-8"))
        stored_scopes = set(stored_token.get("scopes", []))
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)

    if not creds or not creds.valid or not set(SCOPES).issubset(stored_scopes):
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(credentials_file), SCOPES)
            creds = flow.run_local_server(port=0)
        token_file.parent.mkdir(parents=True, exist_ok=True)
        token_file.write_text(creds.to_json(), encoding="utf-8")
        try:
            token_file.chmod(0o600)
        except OSError:
            pass
    return creds


def leer_planilla(
    spreadsheet_id: str,
    range_name: str,
    credentials_file: Path,
    token_file: Path,
    mostrar_primeras_filas: bool = False,
) -> list[list[Any]]:
    """Lee los valores de la planilla autenticando a la cuenta Google del usuario."""
    try:
        from googleapiclient.discovery import build
        from googleapiclient.errors import HttpError
    except ImportError as error:
        raise RuntimeError(
            "Faltan dependencias de Google. Instala las dependencias indicadas en "
            "requirements.txt."
        ) from error

    creds = _autenticar(credentials_file, token_file)
    service = build("sheets", "v4", credentials=creds, cache_discovery=False)
    try:
        response = (
            service.spreadsheets()
            .values()
            .get(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueRenderOption="UNFORMATTED_VALUE",
            )
            .execute()
        )
        rows = response.get("values", [])
        if mostrar_primeras_filas:
            _imprimir_primeras_filas(rows)
        return rows
    except HttpError as error:
        if error.resp.status != 400 or "Office file" not in str(error):
            raise
        rows = _leer_archivo_office(spreadsheet_id, range_name, creds)
        if mostrar_primeras_filas:
            _imprimir_primeras_filas(rows)
        return rows


def _imprimir_primeras_filas(rows: list[list[Any]]) -> None:
    print("\nPrimeras 3 filas sin filtrar:")
    for row_number, row in enumerate(rows[:3], start=1):
        print(f"Fila {row_number}: {json.dumps(row, ensure_ascii=False, default=str)}")


def _leer_archivo_office(spreadsheet_id: str, range_name: str, credentials: Any) -> list[list[Any]]:
    """Descarga un Excel compartido y devuelve el rango de su hoja activa."""
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload
    import openpyxl

    service = build("drive", "v3", credentials=credentials, cache_discovery=False)
    request = service.files().get_media(fileId=spreadsheet_id)
    buffer = BytesIO()
    downloader = MediaIoBaseDownload(buffer, request)
    finished = False
    while not finished:
        _, finished = downloader.next_chunk()

    match = re.search(r"(?:[^!]+!)?([A-Z]+)(?::([A-Z]+))?", range_name.upper().replace("$", ""))
    if not match:
        raise ValueError(f"Rango no válido: {range_name}")
    first_column = _numero_columna(match.group(1))
    last_column = _numero_columna(match.group(2) or match.group(1))
    workbook = openpyxl.load_workbook(BytesIO(buffer.getvalue()), data_only=True, read_only=True)
    worksheet = workbook.active
    if worksheet is None:
        raise ValueError("El archivo Excel no contiene una hoja activa.")
    return [
        list(values)
        for values in worksheet.iter_rows(
            min_col=first_column, max_col=last_column, values_only=True
        )
    ]


def _numero_columna(column: str) -> int:
    number = 0
    for character in column:
        number = number * 26 + ord(character) - ord("A") + 1
    return number


def _normalizar_filas(rows: list[list[Any]]) -> list[list[Any]]:
    """Quita celdas y filas vacías solo al final, como hace la respuesta de Sheets."""
    normalized = [list(row) for row in rows]
    while normalized and not any(value not in (None, "") for value in normalized[-1]):
        normalized.pop()
    for row in normalized:
        while row and row[-1] in (None, ""):
            row.pop()
    return normalized


def _encontrar_encabezados(rows: list[list[Any]], requeridos: tuple[str, ...]) -> tuple[int, list[str]]:
    for row_index, row in enumerate(rows[:10]):
        headers = [str(value or "").strip() for value in row]
        normalized_headers = {header.casefold() for header in headers}
        if all(requerido.casefold() in normalized_headers for requerido in requeridos):
            return row_index, headers
    raise ValueError(
        "No se encontró la fila de encabezados con: " + ", ".join(requeridos) + "."
    )


def filtrar_correos(
    rows: list[list[Any]], curso: str, rut: str,
    curso_header: str = "Curso", rut_header: str = "RUT",
) -> list[dict[str, Any]]:
    """Filtra por curso y RUT y devuelve los valores de las columnas H y K."""
    if not rows:
        return []

    header_row_index, header_values = _encontrar_encabezados(rows, (curso_header, rut_header))
    headers = [value.casefold() for value in header_values]
    try:
        curso_index = headers.index(curso_header.strip().casefold())
        rut_index = headers.index(rut_header.strip().casefold())
    except ValueError as error:
        raise ValueError(
            f"No se encontraron las columnas '{curso_header}' y '{rut_header}'."
        ) from error

    def normalizar(valor: Any) -> str:
        return str(valor or "").strip().casefold()

    resultados = []
    for row_number, row in enumerate(rows[header_row_index + 1:], start=header_row_index + 2):
        if normalizar(row[curso_index] if curso_index < len(row) else "") != normalizar(curso):
            continue
        if normalizar(row[rut_index] if rut_index < len(row) else "") != normalizar(rut):
            continue
        resultados.append({
            "fila": row_number,
            "H": row[7] if len(row) > 7 else "",
            "K": row[10] if len(row) > 10 else "",
        })
    return resultados


def filtrar_curso(rows: list[list[Any]], curso: str, curso_header: str = "Curso") -> tuple[list[str], list[list[Any]]]:
    """Devuelve los encabezados y las filas que pertenecen a un curso."""
    if not rows:
        return [], []

    header_row_index, headers = _encontrar_encabezados(rows, (curso_header,))
    normalized_headers = [header.casefold() for header in headers]
    try:
        curso_index = normalized_headers.index(curso_header.strip().casefold())
    except ValueError as error:
        raise ValueError(f"No se encontró la columna '{curso_header}'.") from error

    curso_buscado = str(curso).strip().casefold()
    filtered_rows = [
        list(row)
        for row in rows[header_row_index + 1:]
        if str(row[curso_index] if curso_index < len(row) else "").strip().casefold() == curso_buscado
    ]
    return headers, filtered_rows


def guardar_curso_pandas(
    rows: list[list[Any]], curso: str, output_file: Path, curso_header: str = "Curso"
) -> int:
    """Filtra un curso y lo guarda como CSV usando un DataFrame de pandas."""
    if output_file.suffix.lower() != ".csv":
        raise ValueError("El archivo de salida debe tener extensión .csv.")
    try:
        import pandas as pd
    except ImportError as error:
        raise RuntimeError("Falta pandas. Instálalo con: utp/bin/python -m pip install pandas") from error

    headers, filtered_rows = filtrar_curso(rows, curso, curso_header)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    rows_with_fixed_width = [row[:len(headers)] + [""] * max(0, len(headers) - len(row)) for row in filtered_rows]
    dataframe = pd.DataFrame(rows_with_fixed_width, columns=headers)
    dataframe.to_csv(output_file, index=False, encoding="utf-8-sig")
    return len(filtered_rows)


def comparar_filas(previous: list[list[Any]], current: list[list[Any]]) -> list[RowChange]:
    """Compara por número de fila; los números reportados son los de la hoja."""
    old_rows = _normalizar_filas(previous)
    new_rows = _normalizar_filas(current)
    changes = []
    for index in range(max(len(old_rows), len(new_rows))):
        old = old_rows[index] if index < len(old_rows) else None
        new = new_rows[index] if index < len(new_rows) else None
        if old == new:
            continue
        if old is None:
            kind = "agregada"
        elif new is None:
            kind = "eliminada"
        else:
            kind = "modificada"
        changes.append(RowChange(kind, index + 1, old, new))
    return changes


def _guardar_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        path.chmod(0o600)
    except OSError:
        pass


def verificar_cambios(
    spreadsheet: str,
    range_name: str,
    credentials_file: Path = Path("credentials.json"),
    token_file: Path = Path(".google_sheets/token.json"),
    snapshot_file: Path = Path(".google_sheets/snapshot.json"),
    accept_current: bool = False,
) -> CheckResult:
    """Compara la hoja con la última versión aceptada y conserva el reporte pendiente."""
    spreadsheet_id = extraer_id_planilla(spreadsheet)
    current = _normalizar_filas(
        leer_planilla(
            spreadsheet_id, range_name, credentials_file, token_file,
            mostrar_primeras_filas=True,
        )
    )
    identity = {"spreadsheet_id": spreadsheet_id, "range": range_name}
    snapshot: dict[str, Any] | None = None

    if snapshot_file.is_file() and not accept_current:
        snapshot_data = json.loads(snapshot_file.read_text(encoding="utf-8"))
        if not isinstance(snapshot_data, dict):
            raise ValueError(f"El archivo de referencia {snapshot_file} no contiene un objeto JSON válido.")
        snapshot = snapshot_data
        if any(snapshot.get(key) != value for key, value in identity.items()):
            raise ValueError(
                "El archivo de referencia pertenece a otra planilla o rango. "
                "Usa otro --snapshot o ejecuta con --accept-current para crear una referencia nueva."
            )

    if accept_current:
        _guardar_json(snapshot_file, {**identity, "values": current})
        return CheckResult("referencia_actualizada", [])

    if snapshot is None:
        _guardar_json(snapshot_file, {**identity, "values": current})
        return CheckResult("referencia_creada", [])

    changes = comparar_filas(snapshot.get("values", []), current)
    return CheckResult("cambios_detectados" if changes else "sin_cambios", changes)


def _imprimir_resultado(result: CheckResult, details: bool) -> None:
    if result.status == "referencia_creada":
        print("Referencia inicial guardada. Desde la próxima ejecución se detectarán cambios.")
    elif result.status == "referencia_actualizada":
        print("Referencia actualizada con los datos actuales de la planilla.")
    elif not result.changes:
        print("Sin cambios en los datos de la planilla.")
    else:
        counts = {
            kind: sum(change.kind == kind for change in result.changes)
            for kind in ("modificada", "agregada", "eliminada")
        }
        print(
            "Cambios detectados: "
            f"{counts['modificada']} fila(s) modificada(s), "
            f"{counts['agregada']} agregada(s), {counts['eliminada']} eliminada(s)."
        )
        print("Filas: " + ", ".join(str(change.row_number) for change in result.changes))
        if details:
            for change in result.changes:
                print(
                    f"Fila {change.row_number} ({change.kind}): "
                    f"antes={json.dumps(change.previous, ensure_ascii=False)}; "
                    f"ahora={json.dumps(change.current, ensure_ascii=False)}"
                )
        print(
            "La referencia no se modificó. Tras revisar/procesar los cambios, "
            "usa --accept-current para aceptarlos."
        )


def _imprimir_correos(resultados: list[dict[str, Any]]) -> None:
    if not resultados:
        print("No se encontraron coincidencias.")
        return
    for resultado in resultados:
        print(json.dumps(resultado, ensure_ascii=False))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spreadsheet", help="URL o ID de la planilla compartida")
    parser.add_argument("--range", default="A:ZZ", help="Rango A1, por ejemplo 'Datos!A:Z'")
    parser.add_argument("--curso", help="Filtra por el valor de la columna Curso y lo guarda en CSV con pandas")
    parser.add_argument("--rut", help="Filtra por el valor de la columna RUT y muestra H y K")
    parser.add_argument("--curso-header", default="Curso", help="Encabezado de la columna del curso")
    parser.add_argument("--rut-header", default="RUT", help="Encabezado de la columna del RUT")
    parser.add_argument(
        "--salida-curso", type=Path, default=Path("google_sheets/curso_filtrado.csv"),
        help="Archivo .csv donde se guardan los datos filtrados del curso",
    )
    parser.add_argument("--credentials", type=Path, default=Path("google_sheets/credentials.json"))
    parser.add_argument("--token", type=Path, default=Path("google_sheets/token.json"))
    parser.add_argument("--snapshot", type=Path, default=Path("google_sheets/snapshot.json"))
    parser.add_argument(
        "--accept-current", action="store_true",
        help="Guarda los datos actuales como nueva referencia, aceptando los cambios.",
    )
    parser.add_argument(
        "--details", action="store_true",
        help="Muestra valores anteriores y actuales (pueden incluir datos personales).",
    )
    parser.add_argument(
        "--fail-on-change", action="store_true",
        help="Termina con código 1 si detecta cambios, para detener una tarea automatizada.",
    )
    args = parser.parse_args()

    try:
        if args.rut is not None and args.curso is None:
            parser.error("Debes indicar --curso junto con --rut.")
        if args.curso is not None:
            rows = leer_planilla(
                extraer_id_planilla(args.spreadsheet),
                args.range,
                args.credentials,
                args.token,
                mostrar_primeras_filas=True,
            )
            if args.rut is not None:
                _imprimir_correos(filtrar_correos(rows, args.curso, args.rut, args.curso_header, args.rut_header))
                return 0
            count = guardar_curso_pandas(rows, args.curso, args.salida_curso, args.curso_header)
            print(f"{count} fila(s) del curso {args.curso} guardadas en {args.salida_curso}.")
            return 0
        result = verificar_cambios(
            args.spreadsheet,
            args.range,
            args.credentials,
            args.token,
            args.snapshot,
            args.accept_current,
        )
    except Exception as error:
        parser.exit(2, f"Error: {error}\n")

    _imprimir_resultado(result, args.details)
    return 1 if args.fail_on_change and result.has_changes else 0


if __name__ == "__main__":
    raise SystemExit(main())