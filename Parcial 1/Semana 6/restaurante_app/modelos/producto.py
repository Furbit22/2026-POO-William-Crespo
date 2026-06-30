# -*- coding: utf-8 -*-

class Producto:
    """
    Clase padre que representa un producto genérico del restaurante.
    Aplica encapsulación al atributo privado __precio.
    """
    def __init__(self, nombre: str, precio: float, disponible: bool = True):
        # Atributos públicos y protegidos
        self.nombre = nombre
        self._disponible = disponible
        # Atributo privado (encapsulado)
        self.__precio = 0.0
        
        # Asignar a través del método de modificación para aplicar la validación inicial
        self.cambiar_precio(precio)

    # Métodos de acceso (Getters)
    def obtener_precio(self) -> float:
        """Retorna el precio del producto."""
        return self.__precio

    def obtener_disponibilidad(self) -> bool:
        """Retorna el estado de disponibilidad del producto."""
        return self._disponible

    # Métodos de modificación (Setters)
    def cambiar_precio(self, nuevo_precio: float) -> bool:
        """
        Modifica el precio del producto aplicando validación.
        El precio debe ser un número positivo mayor que cero.
        """
        if nuevo_precio <= 0:
            print(f"Error de validación: El precio para '{self.nombre}' debe ser mayor a 0 (Intentado: {nuevo_precio})")
            return False
        self.__precio = nuevo_precio
        return True

    def cambiar_disponibilidad(self, disponible: bool):
        """Modifica la disponibilidad del producto."""
        self._disponible = disponible

    def mostrar_informacion(self) -> str:
        """Retorna una cadena con la información básica del producto."""
        estado = "Disponible" if self._disponible else "Agotado"
        return f"Producto: {self.nombre} | Precio: ${self.obtener_precio():.2f} | Estado: {estado}"
