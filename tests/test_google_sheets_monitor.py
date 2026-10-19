from __future__ import annotations

import unittest
from contextlib import redirect_stdout
from datetime import datetime
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

from planilla import (
    _imprimir_primeras_filas,
    comparar_filas,
    extraer_id_planilla,
    filtrar_correos,
    filtrar_curso,
    guardar_curso_pandas,
)


class GoogleSheetsMonitorTests(unittest.TestCase):
    def test_extrae_id_desde_url(self) -> None:
        self.assertEqual(
            extraer_id_planilla("https://docs.google.com/spreadsheets/d/abc_123/edit#gid=0"),
            "abc_123",
        )

    def test_acepta_id_directo(self) -> None:
        self.assertEqual(extraer_id_planilla("abc_123"), "abc_123")

    def test_detecta_filas_modificadas_agregadas_y_eliminadas(self) -> None:
        changes = comparar_filas(
            [["nombre", "curso"], ["Ana", "1A"], ["Luis", "1B"]],
            [["nombre", "curso"], ["Ana", "2A"], ["Luis", "1B"], ["Eva", "1C"]],
        )
        self.assertEqual(
            [(change.kind, change.row_number) for change in changes],
            [("modificada", 2), ("agregada", 4)],
        )

    def test_detecta_fila_eliminada(self) -> None:
        changes = comparar_filas([["nombre"], ["Ana"]], [["nombre"]])
        self.assertEqual([(change.kind, change.row_number) for change in changes], [("eliminada", 2)])

    def test_ignora_celdas_vacias_al_final(self) -> None:
        self.assertEqual(comparar_filas([["dato", ""]], [["dato"]]), [])

    def test_filtra_por_curso_y_rut_y_devuelve_h_y_k(self) -> None:
        rows = [
            ["Curso", "RUT", "C", "D", "E", "F", "G", "Mail H", "I", "J", "Mail K"],
            ["1A", "12-3", "", "", "", "", "", "h@example.com", "", "", "k@example.com"],
            ["1B", "12-3", "", "", "", "", "", "otro@example.com", "", "", "otro@example.com"],
        ]
        self.assertEqual(
            filtrar_correos(rows, "1a", "12-3"),
            [{"fila": 2, "H": "h@example.com", "K": "k@example.com"}],
        )

    def test_filtra_todas_las_filas_de_un_curso(self) -> None:
        rows = [["Nombre", "Curso"], ["Ana", "1EM-A"], ["Luis", "1EM-B"], ["Eva", "1EM-A"]]
        self.assertEqual(
            filtrar_curso(rows, "1em-a"),
            (["Nombre", "Curso"], [["Ana", "1EM-A"], ["Eva", "1EM-A"]]),
        )

    def test_detecta_encabezados_en_la_segunda_fila(self) -> None:
        rows = [["Listado de estudiantes"], ["Nombre", "Curso"], ["Ana", "1EM-A"]]
        self.assertEqual(
            filtrar_curso(rows, "1EM-A"),
            (["Nombre", "Curso"], [["Ana", "1EM-A"]]),
        )

    def test_guarda_filas_filtradas_en_csv_con_pandas(self) -> None:
        rows = [["Nombre", "Curso"], ["Ana", "1EM-A"], ["Luis", "1EM-B"]]
        with TemporaryDirectory() as directory:
            ruta = Path(directory) / "curso.csv"
            self.assertEqual(guardar_curso_pandas(rows, "1EM-A", ruta), 1)
            import pandas as pd

            dataframe = pd.read_csv(ruta, dtype=str)
            self.assertEqual(dataframe.to_dict(orient="records"), [{"Nombre": "Ana", "Curso": "1EM-A"}])

    def test_muestra_sin_filtrar_las_tres_primeras_filas(self) -> None:
        salida = StringIO()
        with redirect_stdout(salida):
            _imprimir_primeras_filas(
                [["encabezado"], [datetime(2010, 1, 2)], ["dos"], ["tres"], ["cuatro"]]
            )
        self.assertIn('Fila 1: ["encabezado"]', salida.getvalue())
        self.assertIn('Fila 2: ["2010-01-02 00:00:00"]', salida.getvalue())
        self.assertIn('Fila 3: ["dos"]', salida.getvalue())
        self.assertNotIn("cuatro", salida.getvalue())


if __name__ == "__main__":
    unittest.main()