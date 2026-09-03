import unittest
import os
import tempfile
import json
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.restaurante import Restaurante
from servicios.archivo_servicio import ArchivoServicio

class TestRestauranteOptimizacion(unittest.TestCase):
    def setUp(self) -> None:
        self.productos_muestra = [
            Producto("P001", "Hamburguesa", "Comida", 5.0, 10),
            Producto("P002", "Papas Fritas", "Acompañamiento", 2.5, 20),
            Producto("P003", "Gaseosa", "Bebida", 1.5, 15)
        ]
        self.usuarios_muestra = [
            Usuario("U001", "Juan Perez", "juan@test.com"),
            Usuario("U002", "Maria Lopez", "maria@test.com")
        ]
        self.ventas_muestra = [
            Venta("U001", "P001", 2),
            Venta("U002", "P003", 1),
            Venta("U001", "P002", 1)
        ]
        self.restaurante = Restaurante(
            productos_iniciales=list(self.productos_muestra),
            usuarios_iniciales=list(self.usuarios_muestra),
            ventas_iniciales=list(self.ventas_muestra)
        )

    def test_reconstruccion_indices_al_iniciar(self) -> None:
        """Verifica que los índices se reconstruyan correctamente a partir de las listas iniciales."""
        # Comprobar índice de productos
        self.assertEqual(len(self.restaurante._indice_productos), 3)
        self.assertIn("P001", self.restaurante._indice_productos)
        self.assertIn("P002", self.restaurante._indice_productos)
        self.assertIn("P003", self.restaurante._indice_productos)

        # Comprobar categorías únicas en el set
        self.assertEqual(self.restaurante.obtener_categorias_unicas(), {"Comida", "Acompañamiento", "Bebida"})

        # Comprobar índice de usuarios y correos registrados
        self.assertEqual(len(self.restaurante._indice_usuarios), 2)
        self.assertIn("U001", self.restaurante._indice_usuarios)
        self.assertTrue(self.restaurante.existe_correo("juan@test.com"))

        # Comprobar índice de ventas agrupadas por usuario
        ventas_u1 = self.restaurante.consultar_ventas_usuario("U001")
        self.assertEqual(len(ventas_u1), 2)
        self.assertEqual(ventas_u1[0].producto_codigo, "P001")
        self.assertEqual(ventas_u1[1].producto_codigo, "P002")

        ventas_u2 = self.restaurante.consultar_ventas_usuario("U002")
        self.assertEqual(len(ventas_u2), 1)
        self.assertEqual(ventas_u2[0].producto_codigo, "P003")

    def test_busqueda_producto_o1(self) -> None:
        """Verifica la búsqueda por código de producto optimizada O(1)."""
        prod = self.restaurante.buscar_producto("P002")
        self.assertIsNotNone(prod)
        self.assertEqual(prod.nombre, "Papas Fritas")
        self.assertEqual(prod.precio, 2.5)

        # Producto inexistente
        self.assertIsNone(self.restaurante.buscar_producto("INEXISTENTE"))

    def test_busqueda_usuario_o1(self) -> None:
        """Verifica la búsqueda por identificación de usuario optimizada O(1)."""
        usr = self.restaurante.buscar_usuario("U002")
        self.assertIsNotNone(usr)
        self.assertEqual(usr.nombre, "Maria Lopez")

        # Usuario inexistente
        self.assertIsNone(self.restaurante.buscar_usuario("9999"))

    def test_sincronizacion_registro_producto(self) -> None:
        """Verifica que registrar un producto mantenga sincronizada la lista, el índice y las categorías."""
        nuevo = Producto("P004", "Helado", "Postre", 2.0, 5)
        resultado = self.restaurante.registrar_producto(nuevo)
        self.assertTrue(resultado)

        # Está en la lista principal
        self.assertIn(nuevo, self.restaurante.obtener_productos())
        # Está en el índice hash
        self.assertIs(self.restaurante.buscar_producto("P004"), nuevo)
        # La categoría 'Postre' fue agregada al set
        self.assertIn("Postre", self.restaurante.obtener_categorias_unicas())

        # No permite registrar producto con código duplicado
        duplicado = Producto("P004", "Otro Helado", "Postre", 3.0, 2)
        self.assertFalse(self.restaurante.registrar_producto(duplicado))

    def test_sincronizacion_actualizacion_producto(self) -> None:
        """Verifica que actualizar un producto conserve coherencia e impacte en categorías si corresponde."""
        resultado = self.restaurante.actualizar_producto(
            codigo="P001",
            nombre="Hamburguesa Especial",
            categoria="Plato Fuerte",
            precio=6.5,
            stock=12
        )
        self.assertTrue(resultado)

        prod = self.restaurante.buscar_producto("P001")
        self.assertEqual(prod.nombre, "Hamburguesa Especial")
        self.assertEqual(prod.categoria, "Plato Fuerte")
        self.assertEqual(prod.precio, 6.5)
        self.assertEqual(prod.stock, 12)

        # La categoría antigua ya no debería estar si ningún otro producto la tiene
        categorias = self.restaurante.obtener_categorias_unicas()
        self.assertIn("Plato Fuerte", categorias)
        self.assertNotIn("Comida", categorias)

    def test_sincronizacion_eliminacion_producto(self) -> None:
        """Verifica que eliminar un producto lo remueva de la lista, del índice y actualice el set de categorías."""
        self.assertTrue(self.restaurante.eliminar_producto("P003"))
        self.assertIsNone(self.restaurante.buscar_producto("P003"))
        self.assertEqual(len(self.restaurante.obtener_productos()), 2)
        # La categoría Bebida ya no existe porque solo P003 la tenía
        self.assertNotIn("Bebida", self.restaurante.obtener_categorias_unicas())

        # Eliminar producto inexistente retorna False
        self.assertFalse(self.restaurante.eliminar_producto("P999"))

    def test_sincronizacion_registro_usuario(self) -> None:
        """Verifica el registro de usuario, indexación de ID y validación de correo con set."""
        nuevo_u = Usuario("U003", "Carlos Andrade", "carlos@test.com")
        self.assertTrue(self.restaurante.registrar_usuario(nuevo_u))
        self.assertIs(self.restaurante.buscar_usuario("U003"), nuevo_u)
        self.assertTrue(self.restaurante.existe_correo("carlos@test.com"))

        # Rechazo por ID duplicada
        u_mismo_id = Usuario("U003", "Otro Nombre", "otro@test.com")
        self.assertFalse(self.restaurante.registrar_usuario(u_mismo_id))

        # Rechazo por correo duplicado
        u_mismo_correo = Usuario("U004", "Tercero", "carlos@test.com")
        self.assertFalse(self.restaurante.registrar_usuario(u_mismo_correo))

    def test_vender_producto_y_sincronizacion_ventas(self) -> None:
        """Verifica que vender descuente stock y sincronice lista de ventas e índice por usuario."""
        prod = self.restaurante.buscar_producto("P001")
        stock_inicial = prod.stock  # 10
        
        # Realizar venta de 3 unidades al usuario U002
        resultado = self.restaurante.vender_producto("P001", "U002", 3)
        self.assertTrue(resultado)

        # Stock disminuido a 7
        self.assertEqual(prod.stock, stock_inicial - 3)

        # Venta agregada a la lista principal
        self.assertEqual(len(self.restaurante.obtener_ventas()), 4)

        # Venta indexada directamente en el usuario U002
        ventas_u2 = self.restaurante.consultar_ventas_usuario("U002")
        self.assertEqual(len(ventas_u2), 2)
        self.assertEqual(ventas_u2[-1].producto_codigo, "P001")
        self.assertEqual(ventas_u2[-1].cantidad, 3)

    def test_validacion_stock_insuficiente_y_cantidad_invalida(self) -> None:
        """Verifica que la venta no se concrete ante stock insuficiente o cantidades no positivas."""
        # Cantidad mayor al stock
        with self.assertRaises(ValueError):
            self.restaurante.vender_producto("P001", "U001", 100)

        # Cantidad negativa o cero
        with self.assertRaises(ValueError):
            self.restaurante.vender_producto("P001", "U001", 0)

        with self.assertRaises(ValueError):
            self.restaurante.vender_producto("P001", "U001", -5)

    def test_persistencia_y_reconstruccion_desde_json(self) -> None:
        """Prueba integral de persistencia en disco y reconstrucción de índices."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ruta_prod = os.path.join(tmpdir, "prod.json")
            ruta_usr = os.path.join(tmpdir, "usr.json")
            ruta_vnt = os.path.join(tmpdir, "vnt.json")

            archivo_serv = ArchivoServicio(ruta_prod, ruta_usr, ruta_vnt)
            # Guardar datos iniciales
            archivo_serv.guardar_productos(self.restaurante.obtener_productos())
            archivo_serv.guardar_usuarios(self.restaurante.obtener_usuarios())
            archivo_serv.guardar_ventas(self.restaurante.obtener_ventas())

            # Cargar en una nueva instancia del servicio
            cargados_prod = archivo_serv.cargar_productos()
            cargados_usr = archivo_serv.cargar_usuarios()
            cargados_vnt = archivo_serv.cargar_ventas()

            nuevo_restaurante = Restaurante(cargados_prod, cargados_usr, cargados_vnt)

            # Verificar que los índices estén perfectamente reconstruidos
            self.assertEqual(len(nuevo_restaurante.obtener_productos()), 3)
            self.assertIsNotNone(nuevo_restaurante.buscar_producto("P001"))
            self.assertIsNotNone(nuevo_restaurante.buscar_usuario("U001"))
            self.assertEqual(len(nuevo_restaurante.consultar_ventas_usuario("U001")), 2)
            self.assertEqual(len(nuevo_restaurante.consultar_ventas_usuario("U002")), 1)
            self.assertEqual(nuevo_restaurante.obtener_categorias_unicas(), {"Comida", "Acompañamiento", "Bebida"})

if __name__ == "__main__":
    unittest.main()
