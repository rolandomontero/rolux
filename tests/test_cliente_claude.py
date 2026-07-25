import os
import sys
import tempfile
import types
import unittest
from pathlib import Path

sys.modules.setdefault("ollama", types.SimpleNamespace(chat=lambda *args, **kwargs: []))
sys.modules.setdefault("servidor_mcp", types.SimpleNamespace(crear_presentacion_desde_plantilla=lambda *args, **kwargs: None))

import start


class ProcesarReferenciasArchivoTests(unittest.TestCase):
    def test_lee_archivo_con_nombre_con_espacios(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            archivo = Path(tmpdir) / "clase 20.txt"
            archivo.write_text("Contenido de instrucción", encoding="utf-8")

            mensaje = "Resume @file:clase 20.txt"
            mensaje_procesado, archivos = start.procesar_referencias_archivo(
                mensaje,
                base_dir=Path(tmpdir),
                workspace_root=Path(tmpdir),
            )

            self.assertNotIn("@file:", mensaje_procesado)
            self.assertEqual(1, len(archivos))
            self.assertIn("Contenido de instrucción", mensaje_procesado)
            self.assertEqual("clase 20.txt", archivos[0]["nombre"])

    def test_devuelve_mensaje_original_sin_referencias(self):
        mensaje = "Solo necesito una respuesta"
        mensaje_procesado, archivos = start.procesar_referencias_archivo(
            mensaje,
            base_dir=Path.cwd(),
            workspace_root=Path.cwd(),
        )

        self.assertEqual(mensaje, mensaje_procesado)
        self.assertEqual([], archivos)


if __name__ == "__main__":
    unittest.main()
