from typing import Any, Dict

class Venta:
    def __init__(self, usuario_id: str, producto_codigo: str, cantidad: int) -> None:
        if not isinstance(usuario_id, str) or not usuario_id.strip():
            raise ValueError("El identificador del usuario no puede estar vacío.")
        if not isinstance(producto_codigo, str) or not producto_codigo.strip():
            raise ValueError("El código del producto no puede estar vacío.")
        
        try:
            cantidad_int = int(cantidad)
        except (TypeError, ValueError):
            raise ValueError("La cantidad vendida debe ser un número entero válido.")

        if cantidad_int <= 0:
            raise ValueError("La cantidad vendida debe ser mayor que cero.")

        self.usuario_id: str = usuario_id.strip()
        self.producto_codigo: str = producto_codigo.strip()
        self.cantidad: int = cantidad_int

    def a_diccionario(self) -> Dict[str, Any]:
        return {
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "cantidad": self.cantidad
        }

    @classmethod
    def desde_diccionario(cls, datos: Dict[str, Any]) -> "Venta":
        usuario_id: str = datos["usuario_id"]
        producto_codigo: str = datos["producto_codigo"]
        cantidad: int = datos["cantidad"]
        return cls(usuario_id, producto_codigo, cantidad)
