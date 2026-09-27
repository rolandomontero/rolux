import builtins
import importlib
import sys
import unittest


class CrossPlatformImportTests(unittest.TestCase):
    def test_import_module_without_win32com_on_macos(self):
        original_import = builtins.__import__

        def guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "win32com" or name.startswith("win32com."):
                raise ImportError("No module named win32com")
            return original_import(name, globals, locals, fromlist, level)

        builtins.__import__ = guarded_import
        original_platform = sys.platform
        sys.platform = "darwin"
        sys.modules.pop("notificar", None)

        try:
            module = importlib.import_module("notificar")
            self.assertIsNone(module.win32com_client)
            self.assertIsNone(module.crear_cliente_outlook())
        finally:
            builtins.__import__ = original_import
            sys.platform = original_platform
            sys.modules.pop("notificar", None)


if __name__ == "__main__":
    unittest.main()
