import os
import sys
import unittest
import tkinter as tk
from typing import List

# Asegurar importación de los módulos de la aplicación
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView

class TestSemana13RestauranteApp(unittest.TestCase):
    """
    Suite de pruebas automatizadas para verificar el cumplimiento de los criterios
    de evaluación de la Semana 13.
    """
    def setUp(self) -> None:
        self.ruta_datos = os.path.join(BASE_DIR, "datos")
        self.ruta_productos = os.path.join(self.ruta_datos, "productos.json")
        self.ruta_usuarios = os.path.join(self.ruta_datos, "usuarios.json")
        self.archivo_servicio = ArchivoServicio(self.ruta_productos, self.ruta_usuarios)
        self.servicio = RestauranteServicio(archivo_servicio=self.archivo_servicio)

    def test_01_modelos_integridad(self) -> None:
        """Verifica las validaciones de las entidades Producto y Usuario."""
        # Producto válido
        p = Producto("P999", "Taco Especial", "Comida", 4.5, 10)
        self.assertEqual(p.codigo, "P999")
        self.assertEqual(p.nombre, "Taco Especial")
        self.assertEqual(p.precio, 4.5)
        self.assertEqual(p.stock, 10)

        # Producto con precio o stock negativo
        with self.assertRaises(ValueError):
            Producto("P000", "Inválido", "Comida", -1.0, 5)
        with self.assertRaises(ValueError):
            Producto("P000", "Inválido", "Comida", 1.0, -5)

        # Usuario válido
        u = Usuario("9999", "Test User", "test@example.com")
        self.assertEqual(u.identificacion, "9999")
        self.assertEqual(u.correo, "test@example.com")

        # Usuario con correo inválido
        with self.assertRaises(ValueError):
            Usuario("9999", "Test User", "sin_arroba")

    def test_02_archivo_servicio_carga_json(self) -> None:
        """Comprueba que ArchivoServicio lee los archivos JSON correctamente."""
        productos = self.archivo_servicio.cargar_productos()
        usuarios = self.archivo_servicio.cargar_usuarios()

        self.assertIsInstance(productos, list)
        self.assertGreater(len(productos), 0)
        self.assertIsInstance(productos[0], Producto)

        self.assertIsInstance(usuarios, list)
        self.assertGreater(len(usuarios), 0)
        self.assertIsInstance(usuarios[0], Usuario)

    def test_03_validacion_acceso_campos_vacios(self) -> None:
        """Criterio 2: Campos vacíos producen respuesta de rechazo con mensaje."""
        exito, msg, user = self.servicio.validar_acceso("", "")
        self.assertFalse(exito)
        self.assertIn("complete todos los campos", msg)
        self.assertIsNone(user)

        exito, msg, user = self.servicio.validar_acceso("admin", "")
        self.assertFalse(exito)
        self.assertIsNone(user)

    def test_04_validacion_acceso_credenciales_incorrectas(self) -> None:
        """Criterio 2: Credenciales incorrectas producen respuesta de rechazo."""
        # Usuario inexistente
        exito, msg, user = self.servicio.validar_acceso("usuario_fantasma_xyz", "1234")
        self.assertFalse(exito)
        self.assertIn("no existe", msg)
        self.assertIsNone(user)

        # Usuario admin con contraseña incorrecta
        exito, msg, user = self.servicio.validar_acceso("admin", "clave_erronea_999")
        self.assertFalse(exito)
        self.assertIn("Contraseña incorrecta", msg)
        self.assertIsNone(user)

    def test_05_validacion_acceso_credenciales_correctas(self) -> None:
        """Criterio 2: Credenciales válidas conceden acceso e instancian Usuario."""
        # Acceso Admin
        exito, msg, user = self.servicio.validar_acceso("admin", "1234")
        self.assertTrue(exito)
        self.assertIsNotNone(user)
        self.assertEqual(user.identificacion, "ADMIN")

        # Acceso con usuario registrado (ej. 1001)
        exito, msg, user = self.servicio.validar_acceso("1001", "1234")
        self.assertTrue(exito)
        self.assertIsNotNone(user)
        self.assertEqual(user.identificacion, "1001")

    def test_06_consultas_restaurante_servicio(self) -> None:
        """Criterio 3: RestauranteServicio provee consultas de productos y usuarios."""
        prods = self.servicio.listar_productos()
        users = self.servicio.listar_usuarios()

        self.assertEqual(len(prods), self.servicio.contar_productos())
        self.assertEqual(len(users), self.servicio.contar_usuarios())
        self.assertGreater(self.servicio.obtener_stock_total(), 0)

        # Búsqueda de productos
        res_prods = self.servicio.buscar_productos("Hamburguesa")
        self.assertGreater(len(res_prods), 0)

        # Búsqueda de usuarios
        res_users = self.servicio.buscar_usuarios("Carlos")
        self.assertGreater(len(res_users), 0)

    def test_07_separacion_responsabilidades_ui(self) -> None:
        """Criterio 1 y 3: Verifica que ui/ no importe ni use directamente 'json'."""
        ui_dir = os.path.join(BASE_DIR, "ui")
        for arch in ["login_view.py", "main_view.py"]:
            ruta = os.path.join(ui_dir, arch)
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
                self.assertNotIn("import json", contenido, f"{arch} no debe importar json")
                self.assertNotIn("productos.json", contenido, f"{arch} no debe acceder a productos.json")
                self.assertNotIn("usuarios.json", contenido, f"{arch} no debe acceder a usuarios.json")

    def test_08_flujo_grafico_tkinter(self) -> None:
        """Criterio 4: Comprueba instanciación gráfica de vistas en ventana única."""
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana durante la prueba

        try:
            contenedor = tk.Frame(root)
            contenedor.pack()

            # 1. Probar LoginView
            login_exitoso = []
            login_view = LoginView(
                contenedor,
                self.servicio,
                on_login_success=lambda u: login_exitoso.append(u)
            )
            login_view.pack()

            # Simular ingreso en campos
            login_view.txt_usuario.insert(0, "admin")
            login_view.txt_contrasenia.insert(0, "1234")
            login_view._procesar_ingreso()

            # 2. Probar transición a MainView
            usuario_demo = Usuario("1001", "Carlos Mendoza", "carlos@example.com")
            login_view.destroy()

            logout_invocado = []
            main_view = MainView(
                contenedor,
                self.servicio,
                usuario_actual=usuario_demo,
                on_logout=lambda: logout_invocado.append(True)
            )
            main_view.pack()

            # Verificar que los Treeview se hayan poblado
            self.assertGreater(len(main_view.tree_prod.get_children()), 0)
            self.assertGreater(len(main_view.tree_user.get_children()), 0)

            # Verificar retorno a login
            main_view.on_logout()
            self.assertTrue(len(logout_invocado) > 0)
            main_view.destroy()

        finally:
            root.destroy()

if __name__ == "__main__":
    unittest.main()
