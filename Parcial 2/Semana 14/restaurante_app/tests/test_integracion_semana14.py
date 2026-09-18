import os
import sys
import unittest
import tkinter as tk
from unittest.mock import patch

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

class TestSemana14RestauranteApp(unittest.TestCase):
    """
    Suite de pruebas automatizadas para la Semana 14:
    Verifica arquitectura modular, operaciones CRUD sobre productos,
    persistencia en JSON, consultas de usuarios y componentes de Tkinter.
    """
    def setUp(self) -> None:
        self.ruta_datos = os.path.join(BASE_DIR, "datos")
        self.ruta_productos = os.path.join(self.ruta_datos, "productos.json")
        self.ruta_usuarios = os.path.join(self.ruta_datos, "usuarios.json")
        self.archivo_servicio = ArchivoServicio(self.ruta_productos, self.ruta_usuarios)
        self.servicio = RestauranteServicio(archivo_servicio=self.archivo_servicio)

    # -------------------------------------------------------------------------
    # 1. Pruebas de Modelos
    # -------------------------------------------------------------------------
    def test_01_modelos_integridad_producto(self) -> None:
        """Verifica validaciones de la entidad Producto."""
        p = Producto("P888", "Postre Tres Leches", "Postre", 3.75, 12)
        self.assertEqual(p.codigo, "P888")
        self.assertEqual(p.nombre, "Postre Tres Leches")
        self.assertEqual(p.precio, 3.75)
        self.assertEqual(p.stock, 12)

        # Precios o existencias inválidas
        with self.assertRaises(ValueError):
            Producto("P888", "Invalido", "Postre", -2.5, 5)
        with self.assertRaises(ValueError):
            Producto("P888", "Invalido", "Postre", 2.5, -1)
        with self.assertRaises(ValueError):
            Producto("", "Invalido", "Postre", 2.5, 1)

        # Actualización de datos del producto
        p.actualizar_datos("Postre Tres Leches Gigante", "Postre", 4.50, 15)
        self.assertEqual(p.nombre, "Postre Tres Leches Gigante")
        self.assertEqual(p.precio, 4.50)
        self.assertEqual(p.stock, 15)

    def test_02_modelos_integridad_usuario(self) -> None:
        """Verifica validaciones de la entidad Usuario."""
        u = Usuario("2001", "María Belén", "maria@correo.com")
        self.assertEqual(u.identificacion, "2001")
        self.assertEqual(u.nombre, "María Belén")
        self.assertEqual(u.correo, "maria@correo.com")

        # Correo sin arroba o ID vacío
        with self.assertRaises(ValueError):
            Usuario("", "Nombre", "correo@valido.com")
        with self.assertRaises(ValueError):
            Usuario("2002", "Nombre", "correosin_arroba")

    # -------------------------------------------------------------------------
    # 2. Pruebas de Persistencia (ArchivoServicio)
    # -------------------------------------------------------------------------
    def test_03_archivo_servicio_lectura(self) -> None:
        """Comprueba que ArchivoServicio carga productos y usuarios desde JSON."""
        prods = self.archivo_servicio.cargar_productos()
        users = self.archivo_servicio.cargar_usuarios()

        self.assertIsInstance(prods, list)
        self.assertGreater(len(prods), 0)
        self.assertIsInstance(prods[0], Producto)

        self.assertIsInstance(users, list)
        self.assertGreater(len(users), 0)
        self.assertIsInstance(users[0], Usuario)

    # -------------------------------------------------------------------------
    # 3. Pruebas de Simulación de Acceso (Login)
    # -------------------------------------------------------------------------
    def test_04_validacion_acceso_login(self) -> None:
        """Verifica las reglas pedagógicas de autenticación."""
        # Campos vacíos
        exito, msg, u = self.servicio.validar_acceso("", "")
        self.assertFalse(exito)
        self.assertIsNone(u)

        # Admin correcto
        exito, msg, u = self.servicio.validar_acceso("admin", "1234")
        self.assertTrue(exito)
        self.assertIsNotNone(u)
        self.assertEqual(u.identificacion, "ADMIN")

        # Usuario registrado correcto
        exito, msg, u = self.servicio.validar_acceso("1001", "1234")
        self.assertTrue(exito)
        self.assertIsNotNone(u)

    # -------------------------------------------------------------------------
    # 4. Pruebas de Operaciones CRUD sobre Productos (Criterio Central Semana 14)
    # -------------------------------------------------------------------------
    def test_05_crud_registrar_producto_exitoso(self) -> None:
        """Verifica el registro de un nuevo producto con persistencia."""
        cod_test = "P999_TEST"
        # Limpieza preventiva
        if self.servicio.consultar_producto(cod_test):
            self.servicio.eliminar_producto(cod_test)

        total_inicial = self.servicio.contar_productos()

        exito, msg, nuevo = self.servicio.registrar_producto(
            codigo=cod_test,
            nombre="Platillo Prueba Automatizada",
            categoria="Comida",
            precio=7.50,
            stock=10
        )

        self.assertTrue(exito)
        self.assertIsNotNone(nuevo)
        self.assertEqual(self.servicio.contar_productos(), total_inicial + 1)

        # Comprobar consulta inmediata
        consultado = self.servicio.consultar_producto(cod_test)
        self.assertIsNotNone(consultado)
        self.assertEqual(consultado.nombre, "Platillo Prueba Automatizada")

        # Limpiar producto de prueba
        self.servicio.eliminar_producto(cod_test)

    def test_06_crud_registrar_codigo_duplicado(self) -> None:
        """Verifica que el servicio rechace registrar un código ya existente."""
        # P001 ya existe en datos/productos.json
        exito, msg, prod = self.servicio.registrar_producto(
            codigo="P001",
            nombre="Duplicado Falso",
            categoria="Comida",
            precio=10.0,
            stock=5
        )
        self.assertFalse(exito)
        self.assertIn("Ya existe un producto", msg)
        self.assertIsNone(prod)

    def test_07_crud_actualizar_producto(self) -> None:
        """Verifica la actualización de atributos de un producto."""
        cod_test = "P998_TEST"
        # Crear producto temporal
        self.servicio.registrar_producto(cod_test, "Temporal", "Bebida", 2.0, 5)

        # Actualizar datos
        exito, msg, actualizado = self.servicio.actualizar_producto(
            codigo=cod_test,
            nombre="Temporal Modificado",
            categoria="Postre",
            precio=4.25,
            stock=14
        )

        self.assertTrue(exito)
        self.assertEqual(actualizado.nombre, "Temporal Modificado")
        self.assertEqual(actualizado.categoria, "Postre")
        self.assertEqual(actualizado.precio, 4.25)
        self.assertEqual(actualizado.stock, 14)

        # Limpieza
        self.servicio.eliminar_producto(cod_test)

    def test_08_crud_eliminar_producto(self) -> None:
        """Verifica la eliminación de un producto existente."""
        cod_test = "P997_TEST"
        self.servicio.registrar_producto(cod_test, "Para Borrar", "Comida", 5.0, 2)
        total_antes = self.servicio.contar_productos()

        exito, msg = self.servicio.eliminar_producto(cod_test)
        self.assertTrue(exito)
        self.assertEqual(self.servicio.contar_productos(), total_antes - 1)
        self.assertIsNone(self.servicio.consultar_producto(cod_test))

        # Intentar eliminar un código inexistente
        exito_fail, msg_fail = self.servicio.eliminar_producto("CODIGO_INEXISTENTE_XYZ")
        self.assertFalse(exito_fail)
        self.assertIn("No se encontró ningún producto", msg_fail)

    # -------------------------------------------------------------------------
    # 5. Pruebas de Consultas de Usuarios y Productos
    # -------------------------------------------------------------------------
    def test_09_consultas_y_filtros(self) -> None:
        """Verifica métodos de consulta y cálculo del servicio."""
        prods = self.servicio.listar_productos()
        users = self.servicio.listar_usuarios()

        self.assertEqual(len(prods), self.servicio.contar_productos())
        self.assertEqual(len(users), self.servicio.contar_usuarios())
        self.assertGreater(self.servicio.obtener_stock_total(), 0)

        # Filtro de productos
        res_prods = self.servicio.buscar_productos("Hamburguesa")
        self.assertGreater(len(res_prods), 0)

        # Filtro de usuarios
        res_users = self.servicio.buscar_usuarios("Carlos")
        self.assertGreater(len(res_users), 0)

    # -------------------------------------------------------------------------
    # 6. Separación Estricta de Responsabilidades (Criterio 1)
    # -------------------------------------------------------------------------
    def test_10_separacion_arquitectura_ui(self) -> None:
        """Verifica que ui/ no importe ni manipule directamente 'json' ni archivos."""
        ui_dir = os.path.join(BASE_DIR, "ui")
        for arch in ["login_view.py", "main_view.py"]:
            ruta = os.path.join(ui_dir, arch)
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
                self.assertNotIn("import json", contenido, f"{arch} no debe importar json")
                self.assertNotIn("productos.json", contenido, f"{arch} no debe acceder directamente a productos.json")
                self.assertNotIn("usuarios.json", contenido, f"{arch} no debe acceder directamente a usuarios.json")

    # -------------------------------------------------------------------------
    # 7. Integración de Componentes Gráficos de Tkinter (Criterio 3 y 4)
    # -------------------------------------------------------------------------
    def test_11_componentes_y_contenedores_gui(self) -> None:
        """Verifica la construcción de widgets, contenedores y botones de acción."""
        root = tk.Tk()
        root.withdraw()

        try:
            contenedor = tk.Frame(root)
            contenedor.pack()

            # 1. Instanciación y uso de LoginView
            login_exitoso = []
            login_view = LoginView(
                contenedor,
                self.servicio,
                on_login_success=lambda u: login_exitoso.append(u)
            )
            login_view.pack()

            login_view.txt_usuario.insert(0, "admin")
            login_view.txt_contrasenia.insert(0, "1234")
            login_view._procesar_ingreso()
            self.assertEqual(len(login_exitoso), 1)

            login_view.destroy()

            # 2. Instanciación de MainView
            usuario_demo = Usuario("1001", "Carlos Mendoza", "carlos@example.com")
            main_view = MainView(
                contenedor,
                self.servicio,
                usuario_actual=usuario_demo,
                on_logout=lambda: None
            )
            main_view.pack()

            # Verificar presencia de componentes requeridos de la Semana 14
            self.assertTrue(hasattr(main_view, "frame_formulario"))
            self.assertTrue(hasattr(main_view, "cmb_categoria"))
            self.assertTrue(hasattr(main_view, "spn_stock"))
            self.assertTrue(hasattr(main_view, "tree_prod"))
            self.assertTrue(hasattr(main_view, "tree_user"))

            # Verificar que las tablas tengan datos cargados
            self.assertGreater(len(main_view.tree_prod.get_children()), 0)
            self.assertGreater(len(main_view.tree_user.get_children()), 0)

            # Verificar población y limpieza del formulario
            prod_p001 = self.servicio.consultar_producto("P001")
            self.assertIsNotNone(prod_p001)
            main_view._poblar_formulario(prod_p001)
            self.assertEqual(main_view.txt_codigo.get(), "P001")
            self.assertEqual(main_view.cmb_categoria.get(), prod_p001.categoria)

            main_view._limpiar_formulario()
            self.assertEqual(main_view.txt_codigo.get(), "")
            self.assertEqual(main_view.spn_stock.get(), "0")

            # Simulación de registro desde UI con mocks de messagebox
            with patch("tkinter.messagebox.showinfo"), patch("tkinter.messagebox.showwarning"):
                main_view.txt_codigo.insert(0, "P996_GUI")
                main_view.txt_nombre.insert(0, "Item GUI Test")
                main_view.cmb_categoria.set("Bebida")
                main_view.txt_precio.insert(0, "2.50")
                main_view.spn_stock.delete(0, tk.END)
                main_view.spn_stock.insert(0, "8")

                main_view._registrar_producto()
                self.assertIsNotNone(self.servicio.consultar_producto("P996_GUI"))

                # Eliminar el item de prueba
                self.servicio.eliminar_producto("P996_GUI")

            main_view.destroy()

        finally:
            root.destroy()

if __name__ == "__main__":
    unittest.main()
