from modelos.producto import Producto
from modelos.cliente import Cliente

class Restaurante:
    """
    Clase de servicio encargada de administrar las listas de productos y clientes del restaurante.
    """
    def __init__(self):
        self._productos: list[Producto] = []
        self._clientes: list[Cliente] = []

    # Métodos para productos
    def registrar_producto(self, producto: Producto) -> None:
        """Registra un nuevo producto en el restaurante."""
        self._productos.append(producto)

    def listar_productos(self) -> list[Producto]:
        """Retorna la lista de todos los productos registrados."""
        return self._productos

    def buscar_producto(self, nombre: str) -> list[Producto]:
        """
        Busca productos por coincidencia en el nombre (insensible a mayúsculas/minúsculas).
        Retorna una lista de productos coincidentes.
        """
        nombre_buscado = nombre.strip().lower()
        return [p for p in self._productos if nombre_buscado in p.nombre.lower()]

    # Métodos para clientes
    def registrar_cliente(self, cliente: Cliente) -> None:
        """Registra un nuevo cliente en el restaurante."""
        self._clientes.append(cliente)

    def listar_clientes(self) -> list[Cliente]:
        """Retorna la lista de todos los clientes registrados."""
        return self._clientes

    def buscar_cliente(self, id_cliente: str) -> Cliente | None:
        """
        Busca un cliente por su id_cliente.
        Retorna el objeto Cliente si existe, o None si no es encontrado.
        """
        id_buscado = id_cliente.strip()
        for c in self._clientes:
            if c.id_cliente == id_buscado:
                return c
        return None
