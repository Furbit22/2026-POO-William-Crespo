from dataclasses import dataclass

@dataclass
class Cliente:
    """
    Clase que representa un cliente del restaurante.
    Se implementa utilizando el decorador @dataclass.
    """
    nombre: str
    correo: str
    id_cliente: str
