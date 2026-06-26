# Importar clases de los módelos
from modelos.producto import Producto
from modelos.cliente import Cliente


# Clase que gestiona el restaurante
class Restaurante:
    """Clase que administra productos y clientes del restaurante."""

    def __init__(self, nombre_restaurante: str) -> None:
        """
        Inicializa el restaurante con su nombre y listas vacías.

        Args:
            nombre_restaurante: Nombre del restaurante
        """
        # Atributo del restaurante
        self.nombre_restaurante: str = nombre_restaurante
        # Listas para almacenar productos y clientes
        self.lista_productos: list = []
        self.lista_clientes: list = []

    def agregar_producto(self, producto) -> None:
        """Agrega un producto a la lista del inventario."""
        self.lista_productos.append(producto)

    def registrar_cliente(self, cliente) -> None:
        """Registra un cliente en la base de datos del restaurante."""
        self.lista_clientes.append(cliente)

    def mostrar_informacion_sistema(self) -> None:
        """Muestra en consola toda la información de productos y clientes."""
        linea = "=" * 80
        print("\n" + linea)
        print(f"INFORMACION DEL RESTAURANTE: {self.nombre_restaurante}")
        print(linea)

        # Mostrar productos registrados
        print("\nPRODUCTOS REGISTRADOS:")
        print("-" * 80)
        if self.lista_productos:
            for i, producto in enumerate(self.lista_productos, 1):
                print(f"{i}. {producto}")
        else:
            print("No hay productos registrados.")

        # Mostrar clientes registrados
        print("\nCLIENTES REGISTRADOS:")
        print("-" * 80)
        if self.lista_clientes:
            for i, cliente in enumerate(self.lista_clientes, 1):
                print(f"{i}. {cliente}")
        else:
            print("No hay clientes registrados.")

        print("\n" + linea + "\n")
