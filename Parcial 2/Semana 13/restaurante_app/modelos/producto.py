from typing import Any, Dict

class Producto:
    """
    Representa un producto o platillo ofrecido en el restaurante.
    Contiene código identificador, nombre, categoría, precio unitario y stock disponible.
    """
    def __init__(self, codigo: str, nombre: str, categoria: str, precio: float, stock: int = 0) -> None:
        if not isinstance(codigo, str) or not codigo.strip():
            raise ValueError("El código del producto no puede estar vacío.")
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        if not isinstance(categoria, str) or not categoria.strip():
            raise ValueError("La categoría del producto no puede estar vacía.")
        
        try:
            precio_float = float(precio)
        except (ValueError, TypeError):
            raise ValueError("El precio del producto debe ser un valor numérico válido.")

        if precio_float < 0:
            raise ValueError("El precio del producto no puede ser negativo.")

        try:
            stock_int = int(stock)
        except (ValueError, TypeError):
            raise ValueError("El stock del producto debe ser un número entero.")

        if stock_int < 0:
            raise ValueError("El stock del producto no puede ser negativo.")

        self.codigo: str = codigo.strip()
        self.nombre: str = nombre.strip()
        self.categoria: str = categoria.strip()
        self.precio: float = precio_float
        self.stock: int = stock_int

    def mostrar_informacion(self) -> str:
        """Retorna una cadena descriptiva con los detalles del producto."""
        return (f"Código: {self.codigo} | Nombre: {self.nombre} | "
                f"Categoría: {self.categoria} | Precio: ${self.precio:.2f} | Stock: {self.stock}")

    def a_diccionario(self) -> Dict[str, Any]:
        """Serializa la entidad Producto a un diccionario compatible con formato JSON."""
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock
        }

    @classmethod
    def desde_diccionario(cls, datos: Dict[str, Any]) -> "Producto":
        """Reconstruye una instancia de Producto a partir de un diccionario."""
        codigo: str = datos["codigo"]
        nombre: str = datos["nombre"]
        categoria: str = datos["categoria"]
        precio: float = float(datos["precio"])
        stock: int = int(datos.get("stock", 0))
        return cls(codigo, nombre, categoria, precio, stock)
