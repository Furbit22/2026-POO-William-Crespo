from typing import Any, Dict

class Usuario:
    """
    Representa a un comensal o usuario registrado en el sistema del restaurante.
    Contiene cédula/identificación, nombre completo y correo electrónico.
    """
    def __init__(self, identificacion: str, nombre: str, correo: str) -> None:
        if not isinstance(identificacion, str) or not identificacion.strip():
            raise ValueError("La identificación del usuario no puede estar vacía.")
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del usuario no puede estar vacío.")
        if not isinstance(correo, str) or "@" not in correo or not correo.strip():
            raise ValueError("El correo electrónico del usuario debe ser válido (contener '@').")

        self.identificacion: str = identificacion.strip()
        self.nombre: str = nombre.strip()
        self.correo: str = correo.strip()

    def mostrar_informacion(self) -> str:
        """Retorna una cadena con la información del usuario."""
        return f"ID: {self.identificacion} | Nombre: {self.nombre} | Correo: {self.correo}"

    def a_diccionario(self) -> Dict[str, Any]:
        """Serializa la entidad Usuario a un formato de diccionario."""
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
