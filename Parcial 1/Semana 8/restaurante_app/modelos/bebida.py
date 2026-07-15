from modelos.producto import Producto

class Bebida(Producto):
    def __init__(self, codigo: str, nombre: str, categoria: str, precio: float, tamano: str, envase: str) -> None:
        super().__init__(codigo, nombre, categoria, precio)
        self.tamano: str = tamano
        self.envase: str = envase

    def mostrar_informacion(self) -> str:
        info_base = super().mostrar_informacion()
        return f"{info_base} | Tamaño: {self.tamano} | Envase: {self.envase}"
