"""Lee e imprime un archivo CSV usando pandas."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def mostrar_csv(ruta: Path) -> None:
    """Lee y muestra el contenido tabular de un archivo CSV."""
    if not ruta.is_file():
        raise FileNotFoundError(f"No existe el archivo: {ruta}")

    dataframe = pd.read_csv(ruta, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    print(f"Archivo: {ruta}\n")
    if dataframe.empty:
        print("El archivo no contiene filas de datos.")
    else:
        print(dataframe.to_string(index=False))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "archivo",
        nargs="?",
        type=Path,
        default=Path("google_sheets/curso_1EM-A.csv"),
        help="Ruta al CSV (predeterminado: google_sheets/curso_1EM-A.csv)",
    )
    args = parser.parse_args()
    mostrar_csv(args.archivo)


if __name__ == "__main__":
    main()