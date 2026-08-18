from typing import Any, Dict

class Usuario:
    def __init__(self, identificacion: str, nombre: str, correo: str) -> None:
        if not isinstance(identificacion, str) or not identificacion.strip():
            raise ValueError("La identificación del usuario no puede estar vacía.")
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del usuario no puede estar vacío.")
        if not isinstance(correo, str) or not correo.strip() or "@" not in correo:
            raise ValueError("El correo del usuario debe ser un correo válido.")

        self.identificacion: str = identificacion.strip()
        self.nombre: str = nombre.strip()
        self.correo: str = correo.strip()

    def mostrar_informacion(self) -> str:
        return f"Identificación: {self.identificacion} | Nombre: {self.nombre} | Correo: {self.correo}"

    def a_diccionario(self) -> Dict[str, Any]:
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo
        }

    @classmethod
    def desde_diccionario(cls, datos: Dict[str, Any]) -> "Usuario":
        identificacion: str = datos["identificacion"]
        nombre: str = datos["nombre"]
        correo: str = datos["correo"]
        return cls(identificacion, nombre, correo)
