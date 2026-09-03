from typing import Any, Dict

class Producto:
    """
    Representa un producto dentro del restaurante.
    Mantiene información sobre código, nombre, categoría, precio y stock disponible.
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
        except (TypeError, ValueError):
            raise ValueError("El precio debe ser un número válido.")
        
        if precio_float < 0:
            raise ValueError("El precio no puede ser negativo.")

        try:
            stock_int = int(stock)
        except (TypeError, ValueError):
            raise ValueError("El stock debe ser un número entero válido.")

        if stock_int < 0:
            raise ValueError("El stock no puede ser negativo.")

        self.codigo: str = codigo.strip()
        self.nombre: str = nombre.strip()
        self.categoria: str = categoria.strip()
        self.precio: float = precio_float
        self.stock: int = stock_int

    def vender(self, cantidad: int) -> None:
        """
        Reduce el stock del producto según la cantidad indicada.
        Valida que la cantidad sea un entero positivo y que exista suficiente disponibilidad.
        """
        try:
            cantidad_int = int(cantidad)
        except (TypeError, ValueError):
            raise ValueError("La cantidad solicitada debe ser un número entero válido.")

        if cantidad_int <= 0:
            raise ValueError("La cantidad a vender debe ser mayor que cero.")
        if self.stock < cantidad_int:
            raise ValueError(f"Stock insuficiente para {self.nombre}. Stock disponible: {self.stock}, solicitado: {cantidad_int}")
        
        self.stock -= cantidad_int

    def mostrar_informacion(self) -> str:
        """Retorna una cadena con la información detallada y formateada del producto."""
        return f"Código: {self.codigo} | Producto: {self.nombre} | Categoría: {self.categoria} | Precio: ${self.precio:.2f} | Stock: {self.stock}"

    def a_diccionario(self) -> Dict[str, Any]:
        """Serializa el objeto Producto a un diccionario compatible con JSON."""
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
        precio: float = datos["precio"]
        stock: int = datos.get("stock", 0)
        return cls(codigo, nombre, categoria, precio, stock)
