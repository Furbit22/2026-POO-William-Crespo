class Producto:
    def __init__(self, codigo: str, nombre: str, categoria: str, precio: float) -> None:
        self.codigo: str = codigo
        self.nombre: str = nombre
        self.categoria: str = categoria
        self.precio: float = precio

    def mostrar_informacion(self) -> str:
        return f"Código: {self.codigo} | Producto: {self.nombre} | Categoría: {self.categoria} | Precio: ${self.precio:.2f}"
