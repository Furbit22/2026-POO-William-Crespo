from typing import Any, Dict

class Usuario:
    """
    Representa un usuario del sistema del restaurante (cliente, personal o comensal).
    Se utiliza como información base para la simulación pedagógica de acceso en la UI.
    """
    def __init__(self, identificacion: str, nombre: str, correo: str) -> None:
        if not isinstance(identificacion, str) or not identificacion.strip():
            raise ValueError("La identificación del usuario no puede estar vacía.")
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del usuario no puede estar vacío.")
        if not isinstance(correo, str) or not correo.strip() or "@" not in correo:
            raise ValueError("El correo del usuario debe ser válido (debe contener '@').")

        self.identificacion: str = identificacion.strip()
        self.nombre: str = nombre.strip()
        self.correo: str = correo.strip()

    def mostrar_informacion(self) -> str:
        """Retorna una cadena descriptiva con los detalles del usuario."""
        return f"Identificación: {self.identificacion} | Nombre: {self.nombre} | Correo: {self.correo}"

    def a_diccionario(self) -> Dict[str, Any]:
        """Serializa la entidad Usuario a un diccionario compatible con formato JSON."""
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo
        }

    @classmethod
    def desde_diccionario(cls, datos: Dict[str, Any]) -> "Usuario":
        """Reconstruye una instancia de Usuario a partir de un diccionario."""
        identificacion: str = datos["identificacion"]
        nombre: str = datos["nombre"]
        correo: str = datos["correo"]
        return cls(identificacion, nombre, correo)
