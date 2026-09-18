from typing import Any, Dict

class Producto:
    """
    Representa un producto o platillo ofrecido en el restaurante.
    Contiene código identificador, nombre, categoría, precio unitario y stock disponible.
    Asegura la integridad de los datos mediante validaciones en su inicialización y actualización.
    """
    def __init__(self, codigo: str, nombre: str, categoria: str, precio: float, stock: int = 0) -> None:
        self._validar_cadena(codigo, "El código del producto no puede estar vacío.")
        self._validar_cadena(nombre, "El nombre del producto no puede estar vacío.")
        self._validar_cadena(categoria, "La categoría del producto no puede estar vacía.")
        
        precio_float = self._validar_precio(precio)
        stock_int = self._validar_stock(stock)

        self.codigo: str = codigo.strip()
        self.nombre: str = nombre.strip()
        self.categoria: str = categoria.strip()
        self.precio: float = precio_float
        self.stock: int = stock_int

    @staticmethod
    def _validar_cadena(valor: Any, mensaje_error: str) -> None:
        """Valida que una cadena no sea nula ni esté compuesta únicamente por espacios en blanco."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(mensaje_error)

    @staticmethod
    def _validar_precio(precio: Any) -> float:
        """Valida que el precio sea numérico y no negativo."""
        try:
            precio_float = float(precio)
        except (ValueError, TypeError):
            raise ValueError("El precio del producto debe ser un valor numérico válido.")

        if precio_float < 0:
            raise ValueError("El precio del producto no puede ser negativo.")
        return precio_float

    @staticmethod
    def _validar_stock(stock: Any) -> int:
        """Valida que el stock sea un número entero y no negativo."""
        try:
            stock_int = int(stock)
        except (ValueError, TypeError):
            raise ValueError("El stock del producto debe ser un número entero.")

        if stock_int < 0:
            raise ValueError("El stock del producto no puede ser negativo.")
        return stock_int

    def actualizar_datos(self, nombre: str, categoria: str, precio: float, stock: int) -> None:
        """
        Actualiza los datos modificables del producto con validación previa de integridad.
        El código identificador se mantiene inmutable por consistencia referencial.
        """
        self._validar_cadena(nombre, "El nombre del producto no puede estar vacío.")
        self._validar_cadena(categoria, "La categoría del producto no puede estar vacía.")
        precio_float = self._validar_precio(precio)
        stock_int = self._validar_stock(stock)

        self.nombre = nombre.strip()
        self.categoria = categoria.strip()
        self.precio = precio_float
        self.stock = stock_int

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
