from typing import Any, Dict

class Producto:
    def __init__(self, codigo: str, nombre: str, categoria: str, precio: float) -> None:
        if not isinstance(codigo, str) or not codigo.strip():
            raise ValueError("El código del producto no puede estar vacío.")
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        if not isinstance(categoria, str) or not categoria.strip():
            raise ValueError("La categoría del producto no puede estar vacía.")
        
        try:
            precio_float = float(precio)
        except (TypeError, ValueError):
            raise ValueError("El precio debe ser un número válido.")
        
        if precio_float < 0:
            raise ValueError("El precio no puede ser negativo.")

        self.codigo: str = codigo.strip()
        self.nombre: str = nombre.strip()
        self.categoria: str = categoria.strip()
        self.precio: float = precio_float

    def mostrar_informacion(self) -> str:
        return f"Código: {self.codigo} | Producto: {self.nombre} | Categoría: {self.categoria} | Precio: ${self.precio:.2f}"

    def a_diccionario(self) -> Dict[str, Any]:
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio
        }

    @classmethod
    def desde_diccionario(cls, datos: Dict[str, Any]) -> "Producto":
        # KeyError may happen if fields are missing in data
        codigo: str = datos["codigo"]
        nombre: str = datos["nombre"]
        categoria: str = datos["categoria"]
        precio: float = datos["precio"]
        return cls(codigo, nombre, categoria, precio)
