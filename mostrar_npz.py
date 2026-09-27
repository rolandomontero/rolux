"""Lee e imprime el contenido de un archivo NumPy .npz de confianza."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np


def mostrar_npz(ruta: Path) -> None:
    """Muestra los nombres y valores de los arreglos guardados en un .npz."""
    if not ruta.is_file():
        raise FileNotFoundError(f"No existe el archivo: {ruta}")

    # Este .npz contiene arreglos dtype=object; solo debe abrirse si es de confianza.
    with np.load(ruta, allow_pickle=True) as archivo:
        print(f"Archivo: {ruta}\n")
        for nombre in archivo.files:
            arreglo = archivo[nombre]
            print(f"{nombre} ({arreglo.shape}):")
            if nombre == "datos" and "encabezados" in archivo.files:
                encabezados = archivo["encabezados"].tolist()
                print(" | ".join(str(valor) for valor in encabezados))
                for fila in arreglo.tolist():
                    print(" | ".join(str(valor) for valor in fila))
            else:
                print(arreglo.tolist())
            print()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "archivo",
        nargs="?",
        type=Path,
        default=Path("google_sheets/curso_1EM-A.npz"),
        help="Ruta al .npz (predeterminado: google_sheets/curso_1EM-A.npz)",
    )
    args = parser.parse_args()
    mostrar_npz(args.archivo)


if __name__ == "__main__":
    main()
