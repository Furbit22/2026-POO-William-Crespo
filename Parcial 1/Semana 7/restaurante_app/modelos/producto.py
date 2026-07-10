class Producto:
    """
    Clase que representa un producto del restaurante.
    Aplica constructor tradicional, getters y setters para validar y encapsular la información.
    """
    def __init__(self, nombre: str, categoria: str, precio: float, disponible: bool = True):
        # Usamos los setters para asegurar la validación desde el momento de la creación
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.disponible = disponible

    @property
    def nombre(self) -> str:
        """Obtiene el nombre del producto."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Establece el nombre del producto validando que no esté vacío."""
        if not valor or not valor.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def categoria(self) -> str:
        """Obtiene la categoría del producto."""
        return self._categoria

    @categoria.setter
    def categoria(self, valor: str) -> None:
        """Establece la categoría del producto validando que no esté vacía."""
        if not valor or not valor.strip():
            raise ValueError("La categoría del producto no puede estar vacía.")
        self._categoria = valor.strip()

    @property
    def precio(self) -> float:
        """Obtiene el precio del producto."""
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        """Establece el precio del producto validando que sea mayor a cero."""
        try:
            precio_float = float(valor)
        except (TypeError, ValueError):
            raise ValueError("El precio debe ser un valor numérico.")
        
        if precio_float <= 0:
            raise ValueError("El precio del producto debe ser mayor que cero.")
        self._precio = precio_float

    @property
    def disponible(self) -> bool:
        """Obtiene la disponibilidad del producto."""
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        """Establece la disponibilidad del producto."""
        self._disponible = bool(valor)

    def mostrar_informacion(self) -> str:
        """Retorna una cadena con la información legible del producto."""
        estado = "Disponible" if self._disponible else "No disponible"
        return f"Producto: {self._nombre} | Categoría: {self._categoria} | Precio: ${self._precio:.2f} | Estado: {estado}"
