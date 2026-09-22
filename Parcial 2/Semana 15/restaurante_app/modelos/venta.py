from typing import Any, Dict

class Venta:
    """
    Representa una transacción de venta en restaurante_app.
    Modela la relación fundamental entre un usuario (cliente), un producto adquirido
    y la fecha/hora en que se realizó la operación comercial.
    """
    def __init__(
        self,
        id_venta: str,
        usuario_id: str,
        producto_codigo: str,
        fecha: str,
        total: float
    ) -> None:
        self._validar_cadena(id_venta, "El identificador de la venta no puede estar vacío.")
        self._validar_cadena(usuario_id, "El identificador del usuario no puede estar vacío.")
        self._validar_cadena(producto_codigo, "El código del producto no puede estar vacío.")
        self._validar_cadena(fecha, "La fecha de la venta no puede estar vacía.")

        total_float = self._validar_total(total)

        self.id_venta: str = id_venta.strip()
        self.usuario_id: str = usuario_id.strip()
        self.producto_codigo: str = producto_codigo.strip()
        self.fecha: str = fecha.strip()
        self.total: float = total_float

    @staticmethod
    def _validar_cadena(valor: Any, mensaje_error: str) -> None:
        """Valida que un campo de texto no sea nulo ni esté compuesto solo de espacios."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(mensaje_error)

    @staticmethod
    def _validar_total(total: Any) -> float:
        """Valida que el monto total de la venta sea numérico y no negativo."""
        try:
            total_float = float(total)
        except (ValueError, TypeError):
            raise ValueError("El total de la venta debe ser un número válido.")

        if total_float < 0:
            raise ValueError("El total de la venta no puede ser negativo.")
        return total_float

    def mostrar_informacion(self) -> str:
        """Retorna una cadena descriptiva con los detalles de la venta."""
        return (
            f"Venta [{self.id_venta}] | Fecha: {self.fecha} | "
            f"Usuario ID: {self.usuario_id} | Producto: {self.producto_codigo} | Total: ${self.total:.2f}"
        )

    def a_diccionario(self) -> Dict[str, Any]:
        """Serializa la transacción de venta a un diccionario para su persistencia en JSON."""
        return {
            "id_venta": self.id_venta,
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "fecha": self.fecha,
            "total": self.total
        }

    @classmethod
    def desde_diccionario(cls, datos: Dict[str, Any]) -> "Venta":
        """Reconstruye una instancia de Venta a partir de un diccionario."""
        id_venta: str = str(datos.get("id_venta", "")).strip()
        usuario_id: str = str(datos.get("usuario_id", "")).strip()
        producto_codigo: str = str(datos.get("producto_codigo", "")).strip()
        fecha: str = str(datos.get("fecha", "")).strip()
        total: float = float(datos.get("total", 0.0))

        return cls(
            id_venta=id_venta,
            usuario_id=usuario_id,
            producto_codigo=producto_codigo,
            fecha=fecha,
            total=total
        )
