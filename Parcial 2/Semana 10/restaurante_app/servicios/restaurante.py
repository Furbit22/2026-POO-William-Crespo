from typing import List, Optional, Set
from modelos.producto import Producto
from modelos.usuario import Usuario

class Restaurante:
    def __init__(self, productos_iniciales: Optional[List[Producto]] = None, usuarios_iniciales: Optional[List[Usuario]] = None) -> None:
        self._productos: List[Producto] = productos_iniciales if productos_iniciales is not None else []
        self._usuarios: List[Usuario] = usuarios_iniciales if usuarios_iniciales is not None else []

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

    def actualizar_producto(self, codigo: str, nombre: str, categoria: str, precio: float) -> bool:
        producto = self.buscar_producto(codigo)
        if producto:
            # Validar antes de asignar para cumplir con las reglas de negocio
            # Si lanza ValueError, se propagará a main.py
            temp = Producto(codigo, nombre, categoria, precio)
            producto.nombre = temp.nombre
            producto.categoria = temp.categoria
            producto.precio = temp.precio
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

    def obtener_usuarios(self) -> List[Usuario]:
        return self._usuarios

    def obtener_categorias_unicas(self) -> Set[str]:
        return {prod.categoria for prod in self._productos if prod.categoria}
