# Clase que representa un producto del restaurante
class Producto:
    """Modelo de datos para productos disponibles en el restaurante."""
    
    def __init__(self, nombre: str, precio: float, stock: int, disponible: bool) -> None:
        """
        Inicializa un nuevo producto.
        
        Args:
            nombre: Nombre descriptivo del producto
            precio: Costo del producto en unidades monetarias
            stock: Cantidad disponible en inventario
            disponible: Estado de disponibilidad del producto
        """
        # Atributos del producto con tipado explícito
        self.nombre: str = nombre
        self.precio: float = precio
        self.stock: int = stock
        self.disponible: bool = disponible
    
    def __str__(self) -> str:
        """Retorna una representación legible del producto para el usuario."""
        estado: str = "Disponible" if self.disponible else "No disponible"
        return f"Producto: {self.nombre} | Precio: ${self.precio:.2f} | Stock: {self.stock} unidades | Estado: {estado}"
