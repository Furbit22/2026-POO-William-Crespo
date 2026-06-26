# Clase que representa un cliente del restaurante
class Cliente:
    """Modelo de datos para clientes del restaurante."""

    def __init__(self, cedula: str, nombre_completo: str, edad: int, es_frecuente: bool) -> None:
        """
        Inicializa un nuevo cliente.

        Args:
            cedula: Número de identificación única del cliente
            nombre_completo: Nombre y apellido del cliente
            edad: Edad en años del cliente
            es_frecuente: Indica si el cliente es frecuente o nuevo
        """
        # Atributos del cliente con tipado explícito
        self.cedula: str = cedula
        self.nombre_completo: str = nombre_completo
        self.edad: int = edad
        self.es_frecuente: bool = es_frecuente

    def __str__(self) -> str:
        """Retorna una representación legible del cliente para visualización."""
        tipo_cliente: str = "Frecuente" if self.es_frecuente else "Nuevo"
        return f"Cliente: {self.nombre_completo} | Cédula: {self.cedula} | Edad: {self.edad} años | Tipo: {tipo_cliente}"
