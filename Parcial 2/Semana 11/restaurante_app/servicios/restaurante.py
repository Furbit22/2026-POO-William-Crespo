from typing import List, Optional, Set
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta

class Restaurante:
    def __init__(
        self,
        productos_iniciales: Optional[List[Producto]] = None,
        usuarios_iniciales: Optional[List[Usuario]] = None,
        ventas_iniciales: Optional[List[Venta]] = None
    ) -> None:
        self._productos: List[Producto] = productos_iniciales if productos_iniciales is not None else []
        self._usuarios: List[Usuario] = usuarios_iniciales if usuarios_iniciales is not None else []
        self._ventas: List[Venta] = ventas_iniciales if ventas_iniciales is not None else []

    def registrar_producto(self, producto: Producto) -> bool:
        for prod in self._productos:
            if prod.codigo == producto.codigo:
                return False
        self._productos.append(producto)
        return True

    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        for prod in self._productos:
            if prod.codigo == codigo:
                return prod
        return None

    def actualizar_producto(self, codigo: str, nombre: str, categoria: str, precio: float, stock: int) -> bool:
        producto = self.buscar_producto(codigo)
        if producto:
            # Validar antes de asignar para cumplir con las reglas de negocio
            # Si lanza ValueError, se propagará a main.py
            temp = Producto(codigo, nombre, categoria, precio, stock)
            producto.nombre = temp.nombre
            producto.categoria = temp.categoria
            producto.precio = temp.precio
            producto.stock = temp.stock
            return True
        return False

    def eliminar_producto(self, codigo: str) -> bool:
        producto = self.buscar_producto(codigo)
        if producto:
            self._productos.remove(producto)
            return True
        return False

    def obtener_productos(self) -> List[Producto]:
        return self._productos

    def registrar_usuario(self, usuario: Usuario) -> bool:
        for usr in self._usuarios:
            if usr.identificacion == usuario.identificacion:
                return False
        self._usuarios.append(usuario)
        return True

    def buscar_usuario(self, identificacion: str) -> Optional[Usuario]:
        for usr in self._usuarios:
            if usr.identificacion == identificacion:
                return usr
        return None

    def obtener_usuarios(self) -> List[Usuario]:
        return self._usuarios

    def obtener_categorias_unicas(self) -> Set[str]:
        return {prod.categoria for prod in self._productos if prod.categoria}

    def vender_producto(self, codigo_producto: str, identificacion_usuario: str, cantidad: int) -> bool:
        usuario = self.buscar_usuario(identificacion_usuario)
        producto = self.buscar_producto(codigo_producto)

        if usuario is None or producto is None:
            return False

        # Si cantidad es <= 0 o stock insuficiente, ValueError se lanzará en Producto.vender
        # o lo controlamos aquí y en Producto.vender()
        try:
            cantidad_int = int(cantidad)
        except (TypeError, ValueError):
            raise ValueError("La cantidad solicitada debe ser un número entero válido.")

        if cantidad_int <= 0:
            raise ValueError("La cantidad a vender debe ser mayor que cero.")

        if producto.stock < cantidad_int:
            raise ValueError(f"Stock insuficiente para {producto.nombre}. Stock disponible: {producto.stock}, solicitado: {cantidad_int}")

        venta = Venta(usuario.identificacion, producto.codigo, cantidad_int)
        self._ventas.append(venta)
        producto.vender(cantidad_int)
        return True

    def consultar_ventas_usuario(self, identificacion_usuario: str) -> List[Venta]:
        ventas_usuario: list[Venta] = []
        for venta in self._ventas:
            if venta.usuario_id == identificacion_usuario:
                ventas_usuario.append(venta)
        return ventas_usuario

    def obtener_ventas(self) -> List[Venta]:
        return self._ventas
