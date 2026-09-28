import os
import sys
import unittest
import tkinter as tk
from unittest.mock import patch, MagicMock

# Asegurar importación de los módulos de restaurante_app
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from modelos.usuario import Usuario, ROLES_PERMITIDOS
from modelos.producto import Producto
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView

class TestSemana16GestionUsuarios(unittest.TestCase):
    """
    Suite de pruebas automatizadas para la Semana 16:
    Valida la evolución del modelo Usuario con roles, la lógica CRUD en RestauranteServicio,
    la persistencia en usuarios.json, las restricciones de acceso por rol,
    y el correcto manejo de eventos en la interfaz (<<TreeviewSelect>>, <Return>, <Escape>, <<ComboboxSelected>>).
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

        # Datos de prueba en memoria
        self.usuarios_prueba = [
            Usuario("ADMIN", "Administrador Principal", "admin@restaurante.com", "Administrador"),
            Usuario("1001", "Carlos Mendoza", "carlos@example.com", "Cliente"),
            Usuario("1002", "Ana Gómez", "ana@example.com", "Empleado"),
            Usuario("1005", "William Crespo", "william@uea.edu.ec", "Administrador")
        ]
        self.productos_prueba = [
            Producto("P001", "Hamburguesa Clásica", "Comida", 6.50, 10)
        ]
        self.ventas_prueba = [
            Venta("V001", "1001", "P001", "2026-09-28 10:00:00", 6.50)
        ]

        self.servicio = RestauranteServicio(
            archivo_servicio=None,
            productos=self.productos_prueba,
            usuarios=self.usuarios_prueba,
            ventas=self.ventas_prueba
        )

    # -------------------------------------------------------------------------
    # 1. Pruebas del Modelo Usuario (Roles y Validaciones)
    # -------------------------------------------------------------------------
    def test_creacion_usuario_con_rol_valido(self) -> None:
        """Verifica la inicialización correcta del usuario con roles permitidos."""
        u1 = Usuario("2001", "Juan Pérez", "juan@test.com", "Administrador")
        u2 = Usuario("2002", "Pedro López", "pedro@test.com", "Empleado")
        u3 = Usuario("2003", "Laura Ruiz", "laura@test.com", "Cliente")

        self.assertEqual(u1.rol, "Administrador")
        self.assertTrue(u1.es_administrador)
        self.assertFalse(u1.es_empleado)
        self.assertFalse(u1.es_cliente)

        self.assertEqual(u2.rol, "Empleado")
        self.assertTrue(u2.es_empleado)

        self.assertEqual(u3.rol, "Cliente")
        self.assertTrue(u3.es_cliente)

    def test_creacion_usuario_rol_por_defecto(self) -> None:
        """Comprueba que si no se indica el rol, se asigna 'Cliente' por defecto."""
        u = Usuario("2004", "Sofía Cruz", "sofia@test.com")
        self.assertEqual(u.rol, "Cliente")
        self.assertTrue(u.es_cliente)

    def test_creacion_usuario_rol_invalido_lanza_error(self) -> None:
        """Verifica que un rol no permitido arroje un ValueError informativo."""
        with self.assertRaises(ValueError):
            Usuario("2005", "Marcos Rey", "marcos@test.com", "SuperAdmin")

    def test_actualizar_datos_usuario(self) -> None:
        """Valida la actualización de atributos del usuario mediante método propio."""
        u = Usuario("2006", "Original", "original@test.com", "Cliente")
        u.actualizar_datos("Modificado", "nuevo@test.com", "Empleado")

        self.assertEqual(u.nombre, "Modificado")
        self.assertEqual(u.correo, "nuevo@test.com")
        self.assertEqual(u.rol, "Empleado")
        self.assertTrue(u.es_empleado)

    def test_serializacion_deserializacion_usuario(self) -> None:
        """Comprueba que a_diccionario y desde_diccionario preserven el atributo rol."""
        u = Usuario("2007", "Elena Gil", "elena@test.com", "Empleado")
        dicc = u.a_diccionario()
        self.assertEqual(dicc["rol"], "Empleado")

        reconstruido = Usuario.desde_diccionario(dicc)
        self.assertEqual(reconstruido.identificacion, "2007")
        self.assertEqual(reconstruido.nombre, "Elena Gil")
        self.assertEqual(reconstruido.correo, "elena@test.com")
        self.assertEqual(reconstruido.rol, "Empleado")

    # -------------------------------------------------------------------------
    # 2. Pruebas de CRUD de Usuarios en RestauranteServicio
    # -------------------------------------------------------------------------
    def test_registrar_usuario_exitoso(self) -> None:
        """Verifica el registro exitoso de un nuevo usuario en RestauranteServicio."""
        exito, msg, nuevo = self.servicio.registrar_usuario(
            "3001", "Lucía Vaca", "lucia@test.com", "Empleado"
        )
        self.assertTrue(exito)
        self.assertIsNotNone(nuevo)
        self.assertEqual(nuevo.identificacion, "3001")
        self.assertEqual(nuevo.rol, "Empleado")
        self.assertEqual(self.servicio.contar_usuarios(), 5)

    def test_registrar_usuario_duplicado_rechazado(self) -> None:
        """Verifica que no se permita registrar un usuario con ID ya existente."""
        exito, msg, nuevo = self.servicio.registrar_usuario(
            "1001", "Duplicado", "dup@test.com", "Cliente"
        )
        self.assertFalse(exito)
        self.assertIn("Ya existe", msg)
        self.assertIsNone(nuevo)

    def test_actualizar_usuario_servicio(self) -> None:
        """Verifica la actualización de un usuario existente a través del servicio."""
        exito, msg, act = self.servicio.actualizar_usuario(
            "1001", "Carlos Mendoza Editado", "carlos.nuevo@example.com", "Empleado"
        )
        self.assertTrue(exito)
        self.assertIsNotNone(act)
        self.assertEqual(act.nombre, "Carlos Mendoza Editado")
        self.assertEqual(act.rol, "Empleado")

    def test_eliminar_usuario_exitoso(self) -> None:
        """Verifica la eliminación de un usuario por su identificación."""
        exito, msg = self.servicio.eliminar_usuario("1001", id_usuario_autenticado="ADMIN")
        self.assertTrue(exito)
        self.assertIsNone(self.servicio.buscar_usuario_por_id("1001"))
        self.assertEqual(self.servicio.contar_usuarios(), 3)

    def test_bloqueo_eliminar_cuenta_autenticada(self) -> None:
        """Verifica que el sistema impida eliminar la cuenta actualmente en sesión."""
        exito, msg = self.servicio.eliminar_usuario("ADMIN", id_usuario_autenticado="ADMIN")
        self.assertFalse(exito)
        self.assertIn("No puede eliminar la cuenta con la que ha iniciado sesión", msg)
        self.assertIsNotNone(self.servicio.buscar_usuario_por_id("ADMIN"))

    def test_bloqueo_eliminar_unico_administrador(self) -> None:
        """Verifica que el sistema impida eliminar al único administrador activo."""
        # Dejamos un solo administrador en una instancia aislada
        servicio_mono_admin = RestauranteServicio(
            usuarios=[
                Usuario("ADMIN", "Admin Solo", "admin@solo.com", "Administrador"),
                Usuario("1001", "Cliente Normal", "cli@normal.com", "Cliente")
            ]
        )
        exito, msg = servicio_mono_admin.eliminar_usuario("ADMIN", id_usuario_autenticado="OTRO")
        self.assertFalse(exito)
        self.assertIn("No se puede eliminar el único Administrador", msg)

    # -------------------------------------------------------------------------
    # 3. Pruebas de Validación de Acceso (Login y Roles)
    # -------------------------------------------------------------------------
    def test_login_administrador_credenciales(self) -> None:
        """Verifica que el login como admin reconozca el rol Administrador."""
        exito, msg, user = self.servicio.validar_acceso("admin", "1234")
        self.assertTrue(exito)
        self.assertIsNotNone(user)
        self.assertTrue(user.es_administrador)

    def test_login_empleado_credenciales(self) -> None:
        """Verifica que un empleado autenticado reciba su rol correspondiente."""
        exito, msg, user = self.servicio.validar_acceso("1002", "1234")
        self.assertTrue(exito)
        self.assertIsNotNone(user)
        self.assertTrue(user.es_empleado)
        self.assertEqual(user.rol, "Empleado")

    def test_login_cliente_credenciales(self) -> None:
        """Verifica que un cliente autenticado reciba su rol correspondiente."""
        exito, msg, user = self.servicio.validar_acceso("1001", "1234")
        self.assertTrue(exito)
        self.assertIsNotNone(user)
        self.assertTrue(user.es_cliente)

    # -------------------------------------------------------------------------
    # 4. Pruebas de Interfaz y Manejo de Eventos en Tkinter (MainView)
    # -------------------------------------------------------------------------
    def test_mainview_administrador_acceso_completo(self) -> None:
        """Verifica que el administrador disponga de los controles del formulario y eventos."""
        root = tk.Tk()
        root.withdraw()
        try:
            admin_user = self.servicio.buscar_usuario_por_id("ADMIN")
            view = MainView(root, self.servicio, admin_user, lambda: None)

            # Verificar que el formulario administrativo existe
            self.assertTrue(hasattr(view, "frame_form_usuario"))
            self.assertTrue(hasattr(view, "txt_user_id"))
            self.assertTrue(hasattr(view, "txt_user_nombre"))
            self.assertTrue(hasattr(view, "txt_user_correo"))
            self.assertTrue(hasattr(view, "combo_user_rol"))
            self.assertTrue(hasattr(view, "tree_user"))

            # Verificar que las columnas incluyan el rol
            cols = view.tree_user["columns"]
            self.assertIn("rol", cols)
            self.assertIn("identificacion", cols)
        finally:
            root.destroy()

    def test_mainview_empleado_acceso_restringido(self) -> None:
        """Verifica que un empleado no disponga del formulario administrativo de gestión."""
        root = tk.Tk()
        root.withdraw()
        try:
            empleado_user = self.servicio.buscar_usuario_por_id("1002")
            view = MainView(root, self.servicio, empleado_user, lambda: None)

            # Para empleado, NO debe existir el formulario de creación/edición de usuarios
            self.assertFalse(hasattr(view, "frame_form_usuario"))
            self.assertFalse(hasattr(view, "txt_user_id"))
            # Pero sí dispone de la tabla en modo solo lectura
            self.assertTrue(hasattr(view, "tree_user"))
        finally:
            root.destroy()

    def test_evento_treeview_select_carga_datos(self) -> None:
        """
        Verifica que el evento <<TreeviewSelect>> cargue automáticamente los datos
        del usuario seleccionado al formulario consultándolo mediante RestauranteServicio.
        """
        root = tk.Tk()
        root.withdraw()
        try:
            admin_user = self.servicio.buscar_usuario_por_id("ADMIN")
            view = MainView(root, self.servicio, admin_user, lambda: None)

            # Seleccionar la fila correspondiente a Carlos Mendoza ('1001')
            items = view.tree_user.get_children()
            item_carlos = None
            for it in items:
                vals = view.tree_user.item(it, "values")
                if vals and vals[0] == "1001":
                    item_carlos = it
                    break

            self.assertIsNotNone(item_carlos, "Debe existir la fila 1001 en el Treeview")
            view.tree_user.selection_set(item_carlos)

            # Disparar callback del evento <<TreeviewSelect>>
            view._al_seleccionar_usuario_treeview()

            # Comprobar que los campos del formulario se poblaron desde RestauranteServicio
            self.assertEqual(view.txt_user_id.get(), "1001")
            self.assertEqual(view.txt_user_nombre.get(), "Carlos Mendoza")
            self.assertEqual(view.txt_user_correo.get(), "carlos@example.com")
            self.assertEqual(view.combo_user_rol.get(), "Cliente")
        finally:
            root.destroy()

    def test_evento_combobox_selected_actualiza_descripcion(self) -> None:
        """
        Verifica que el evento <<ComboboxSelected>> responda inmediatamente
        actualizando la tarjeta informativa del rol seleccionado.
        """
        root = tk.Tk()
        root.withdraw()
        try:
            admin_user = self.servicio.buscar_usuario_por_id("ADMIN")
            view = MainView(root, self.servicio, admin_user, lambda: None)

            view.combo_user_rol.set("Empleado")
            view._al_cambiar_rol_combobox()

            # La tarjeta informativa debe contener la descripción del rol Empleado
            desc = view.lbl_info_rol.cget("text")
            self.assertIn("Empleado", desc)
        finally:
            root.destroy()

    def test_evento_escape_limpia_formulario_y_seleccion(self) -> None:
        """
        Verifica que el evento <Escape> limpie el formulario y cancele la selección en la tabla.
        """
        root = tk.Tk()
        root.withdraw()
        try:
            admin_user = self.servicio.buscar_usuario_por_id("ADMIN")
            view = MainView(root, self.servicio, admin_user, lambda: None)

            # Escribir datos ficticios
            view.txt_user_id.insert(0, "9999")
            view.txt_user_nombre.insert(0, "Temporal")

            # Ejecutar callback de Escape
            res = view._al_presionar_escape_usuario()
            self.assertEqual(res, "break")
            self.assertEqual(view.txt_user_id.get(), "")
            self.assertEqual(view.txt_user_nombre.get(), "")
            self.assertEqual(len(view.tree_user.selection()), 0)
        finally:
            root.destroy()

    def test_evento_return_reutiliza_registro(self) -> None:
        """
        Verifica que el evento <Return> dispare el registro reutilizando _registrar_usuario.
        """
        root = tk.Tk()
        root.withdraw()
        try:
            admin_user = self.servicio.buscar_usuario_por_id("ADMIN")
            view = MainView(root, self.servicio, admin_user, lambda: None)

            with patch.object(view, "_registrar_usuario") as mock_reg:
                res = view._al_presionar_enter_usuario()
                self.assertEqual(res, "break")
                mock_reg.assert_called_once()
        finally:
            root.destroy()

    # -------------------------------------------------------------------------
    # 5. Verificación de Recursos en assets/
    # -------------------------------------------------------------------------
    def test_existencia_recursos_assets(self) -> None:
        """Comprueba que la carpeta assets/ contenga los recursos visuales obligatorios."""
        ruta_assets = os.path.join(BASE_DIR, "assets")
        self.assertTrue(os.path.exists(ruta_assets), "La carpeta assets/ debe existir obligatoriamente.")

        archivos_esperados = ["icono_app.png", "logo_header.png", "logo_login.png", "logo_restaurante.png"]
        for arch in archivos_esperados:
            ruta_f = os.path.join(ruta_assets, arch)
            self.assertTrue(os.path.exists(ruta_f), f"Falta el recurso visual obligatorio: {arch}")

if __name__ == "__main__":
    unittest.main()
