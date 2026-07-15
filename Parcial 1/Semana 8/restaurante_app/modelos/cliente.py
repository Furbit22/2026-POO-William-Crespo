class Cliente:
    def __init__(self, identificacion: str, nombre: str, correo: str) -> None:
        self.identificacion: str = identificacion
        self.nombre: str = nombre
        self.correo: str = correo

    def mostrar_informacion(self) -> str:
        return f"Identificación: {self.identificacion} | Nombre: {self.nombre} | Correo: {self.correo}"
