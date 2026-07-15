from typing import List
from modelos.producto import Producto
from modelos.cliente import Cliente

class Restaurante:
    def __init__(self) -> None:
        self._productos: List[Producto] = []
        self._clientes: List[Cliente] = []

    def registrar_producto(self, producto: Producto) -> bool:
        for prod in self._productos:
            if prod.codigo == producto.codigo:
                return False
        self._productos.append(producto)
        return True

    def registrar_cliente(self, cliente: Cliente) -> bool:
        for cli in self._clientes:
            if cli.identificacion == cliente.identificacion:
                return False
        self._clientes.append(cliente)
        return True

    def obtener_productos(self) -> List[Producto]:
        return self._productos

    def obtener_clientes(self) -> List[Cliente]:
        return self._clientes
