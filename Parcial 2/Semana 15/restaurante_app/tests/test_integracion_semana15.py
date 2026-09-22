import os
import sys
import unittest
import tkinter as tk
from unittest.mock import patch, MagicMock

# Asegurar importación de los módulos de restaurante_app
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView

class TestSemana15RestauranteApp(unittest.TestCase):
    """
    Suite de pruebas automatizadas para la Semana 15:
    Verifica modelo Venta, persistencia en ventas.json, lógica transaccional de ventas,
    descuento de existencias, flujo de eventos con command= y callbacks en la interfaz,
    separación de responsabilidades y presencia de recursos en assets/.
    """
    def setUp(self) -> None:
        self.ruta_datos = os.path.join(BASE_DIR, "datos")
        self.ruta_productos = os.path.join(self.ruta_datos, "productos.json")
        self.ruta_usuarios = os.path.join(self.ruta_datos, "usuarios.json")
        self.ruta_ventas = os.path.join(self.ruta_datos, "ventas.json")

        self.archivo_servicio = ArchivoServicio(
            ruta_productos=self.ruta_productos,
            ruta_usuarios=self.ruta_usuarios,
            ruta_ventas=self.ruta_ventas
        )

        # Usar copias en memoria para pruebas aisladas
        self.productos_prueba = [
            Producto("P001", "Hamburguesa Clásica", "Comida", 6.50, 10),
            Producto("P002", "Gaseosa Personal", "Bebida", 1.50, 0)  # Producto sin stock
        ]
        self.usuarios_prueba = [
            Usuario("1001", "Carlos Mendoza", "carlos@example.com"),
            Usuario("1002", "Ana Gómez", "ana@example.com")
        ]
        self.ventas_prueba = [
            Venta("V001", "1001", "P001", "2026-09-21 10:00:00", 6.50)
        ]

        self.servicio = RestauranteServicio(
            archivo_servicio=None,
            productos=self.productos_prueba,
            usuarios=self.usuarios_prueba,
            ventas=self.ventas_prueba
        )

    # -------------------------------------------------------------------------
    # 1. Pruebas del Modelo Venta
    # -------------------------------------------------------------------------
    def test_01_modelo_venta_integridad(self) -> None:
        """Verifica la correcta inicialización y validaciones del modelo Venta."""
        v = Venta("V100", "1001", "P001", "2026-09-21 14:00:00", 8.50)
        self.assertEqual(v.id_venta, "V100")
        self.assertEqual(v.usuario_id, "1001")
        self.assertEqual(v.producto_codigo, "P001")
        self.assertEqual(v.fecha, "2026-09-21 14:00:00")
        self.assertEqual(v.total, 8.50)

        # Campos obligatorios vacíos deben lanzar ValueError
        with self.assertRaises(ValueError):
            Venta("", "1001", "P001", "2026-09-21 14:00:00", 8.50)
        with self.assertRaises(ValueError):
            Venta("V101", "", "P001", "2026-09-21 14:00:00", 8.50)
        with self.assertRaises(ValueError):
            Venta("V102", "1001", "", "2026-09-21 14:00:00", 8.50)
        with self.assertRaises(ValueError):
            Venta("V103", "1001", "P001", "", 8.50)

        # Total negativo o inválido
        with self.assertRaises(ValueError):
            Venta("V104", "1001", "P001", "2026-09-21 14:00:00", -5.0)
        with self.assertRaises(ValueError):
            Venta("V105", "1001", "P001", "2026-09-21 14:00:00", "invalido")

    def test_02_modelo_venta_serializacion(self) -> None:
        """Verifica serialización y reconstrucción de Venta desde diccionario JSON."""
        v_original = Venta("V200", "1002", "P003", "2026-09-21 15:30:00", 3.75)
        dicc = v_original.a_diccionario()

        self.assertIsInstance(dicc, dict)
        self.assertEqual(dicc["id_venta"], "V200")
        self.assertEqual(dicc["usuario_id"], "1002")
        self.assertEqual(dicc["total"], 3.75)

        v_reconstruida = Venta.desde_diccionario(dicc)
        self.assertEqual(v_reconstruida.id_venta, v_original.id_venta)
        self.assertEqual(v_reconstruida.usuario_id, v_original.usuario_id)
        self.assertEqual(v_reconstruida.producto_codigo, v_original.producto_codigo)
        self.assertEqual(v_reconstruida.total, v_original.total)

    # -------------------------------------------------------------------------
    # 2. Pruebas de Persistencia de Ventas (ArchivoServicio)
    # -------------------------------------------------------------------------
    def test_03_archivo_servicio_ventas(self) -> None:
        """Comprueba que ArchivoServicio lee y persiste ventas en formato JSON."""
        ventas_cargadas = self.archivo_servicio.cargar_ventas()
        self.assertIsInstance(ventas_cargadas, list)
        self.assertGreater(len(ventas_cargadas), 0)
        self.assertIsInstance(ventas_cargadas[0], Venta)

    # -------------------------------------------------------------------------
    # 3. Pruebas de Negocio en RestauranteServicio (Registro de Ventas)
    # -------------------------------------------------------------------------
    def test_04_restaurante_servicio_registrar_venta_exitosa(self) -> None:
        """
        Verifica el registro exitoso de una venta:
        relaciona usuario + producto, descuenta 1 unidad de stock y crea la venta.
        """
        stock_inicial = self.servicio.consultar_producto("P001").stock
        total_ventas_inicial = self.servicio.contar_ventas()

        exito, mensaje, nueva_venta = self.servicio.registrar_venta(
            usuario_id="1001",
            producto_codigo="P001"
        )

        self.assertTrue(exito)
        self.assertIsNotNone(nueva_venta)
        self.assertIn("registrada exitosamente", mensaje)

        # Comprobar que el stock disminuyó en 1
        stock_final = self.servicio.consultar_producto("P001").stock
        self.assertEqual(stock_final, stock_inicial - 1)

        # Comprobar que la venta se sumó a la colección
        self.assertEqual(self.servicio.contar_ventas(), total_ventas_inicial + 1)
        self.assertEqual(nueva_venta.usuario_id, "1001")
        self.assertEqual(nueva_venta.producto_codigo, "P001")
        self.assertEqual(nueva_venta.total, 6.50)

    def test_05_restaurante_servicio_registrar_venta_usuario_inexistente(self) -> None:
        """Verifica rechazo con mensaje claro si el usuario no existe."""
        exito, mensaje, venta = self.servicio.registrar_venta("9999", "P001")
        self.assertFalse(exito)
        self.assertIsNone(venta)
        self.assertIn("no está registrado", mensaje)

    def test_06_restaurante_servicio_registrar_venta_producto_inexistente(self) -> None:
        """Verifica rechazo con mensaje claro si el producto no existe."""
        exito, mensaje, venta = self.servicio.registrar_venta("1001", "P999")
        self.assertFalse(exito)
        self.assertIsNone(venta)
        self.assertIn("no existe", mensaje)

    def test_07_restaurante_servicio_registrar_venta_sin_stock(self) -> None:
        """Verifica rechazo si el producto tiene 0 existencias."""
        # P002 fue inicializado con stock = 0
        exito, mensaje, venta = self.servicio.registrar_venta("1001", "P002")
        self.assertFalse(exito)
        self.assertIsNone(venta)
        self.assertIn("No hay existencias", mensaje)

    def test_08_restaurante_servicio_metricas_ventas(self) -> None:
        """Verifica el cálculo de métricas y resumen de ventas."""
        self.assertEqual(self.servicio.contar_ventas(), 1)
        self.assertEqual(self.servicio.calcular_total_ventas(), 6.50)

        detalle = self.servicio.obtener_detalle_venta(self.ventas_prueba[0])
        self.assertEqual(detalle["id_venta"], "V001")
        self.assertEqual(detalle["usuario_nombre"], "Carlos Mendoza")
        self.assertEqual(detalle["producto_nombre"], "Hamburguesa Clásica")
        self.assertEqual(detalle["total"], 6.50)

    # -------------------------------------------------------------------------
    # 4. Pruebas de Arquitectura y Separación de Capas
    # -------------------------------------------------------------------------
    def test_09_separacion_arquitectura_ui(self) -> None:
        """Comprueba que la interfaz gráfica no importe json ni manipule archivos directamente."""
        ruta_main_view = os.path.join(BASE_DIR, "ui", "main_view.py")
        with open(ruta_main_view, "r", encoding="utf-8") as f:
            contenido = f.read()

        # No debe haber 'import json' en la vista
        self.assertNotIn("import json", contenido)
        # No debe haber referencias directas a lectura de .json en la vista
        self.assertNotIn("open('ventas.json'", contenido)
        self.assertNotIn('open("ventas.json"', contenido)

    # -------------------------------------------------------------------------
    # 5. Pruebas de Fundamentos de Eventos (command= y Callbacks en UI)
    # -------------------------------------------------------------------------
    def test_10_fundamentos_eventos_callback_command(self) -> None:
        """
        Verifica el flujo del botón 'Registrar Venta' y el callback de evento:
        1. El botón de registrar venta está asociado mediante command=
        2. El callback obtiene valores, valida y delega a RestauranteServicio.
        """
        root = tk.Tk()
        root.withdraw()

        try:
            admin_user = Usuario("ADMIN", "Administrador", "admin@restaurante.com")
            vista = MainView(
                parent=root,
                servicio=self.servicio,
                usuario_actual=admin_user,
                on_logout=lambda: None
            )

            # Verificar que el botón existe y tiene configurado un command
            btn_venta = vista.btn_registrar_venta
            self.assertIsNotNone(btn_venta)
            self.assertTrue(callable(btn_venta.cget("command")) or str(btn_venta.cget("command")))

            # Simular selección en Comboboxes
            vista.combo_venta_usuario.set("1001 - Carlos Mendoza")
            vista.combo_venta_producto.set("P001 - Hamburguesa Clásica ($6.50 | Stock: 10)")

            # Invocar el callback como si el usuario hubiera pulsado el botón
            with patch("tkinter.messagebox.showinfo") as mock_info:
                vista._al_registrar_venta()
                mock_info.assert_called_once()

            # Verificar que se actualizó el Treeview de ventas
            items_ventas = vista.tree_ventas.get_children()
            self.assertEqual(len(items_ventas), 2)  # 1 inicial + 1 registrada

            # Verificar que el stock disminuyó a 9
            prod_actual = self.servicio.consultar_producto("P001")
            self.assertEqual(prod_actual.stock, 9)

            vista.destroy()
        finally:
            root.destroy()

    # -------------------------------------------------------------------------
    # 6. Pruebas de Recursos Visuales Obligatorios (assets/)
    # -------------------------------------------------------------------------
    def test_11_existencia_y_carga_assets(self) -> None:
        """Verifica la existencia física de la carpeta assets/ y de sus recursos."""
        ruta_assets = os.path.join(BASE_DIR, "assets")
        self.assertTrue(os.path.isdir(ruta_assets), "La carpeta assets/ debe existir obligatoriamente.")

        archivos = os.listdir(ruta_assets)
        self.assertTrue(
            any("logo" in a.lower() for a in archivos),
            "assets/ debe contener el logo o logotipo del restaurante."
        )
        self.assertTrue(
            any("icono" in a.lower() for a in archivos),
            "assets/ debe contener íconos para la interfaz."
        )

if __name__ == "__main__":
    unittest.main()
