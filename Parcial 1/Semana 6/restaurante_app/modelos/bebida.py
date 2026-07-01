# -*- coding: utf-8 -*-
from modelos.producto import Producto

class Bebida(Producto):
    """
    Clase hija que representa una bebida disponible en el restaurante.
    Hereda de Producto y añade el atributo propio volumen_ml.
    """
    def __init__(self, nombre: str, precio: float, volumen_ml: int, disponible: bool = True):
        # Invocar constructor de la clase padre
        super().__init__(nombre, precio, disponible)
        # Atributo propio
        self.volumen_ml = volumen_ml  # Volumen en mililitros

    def mostrar_informacion(self) -> str:
        """
        Sobrescribe el método de la clase padre (Polimorfismo).
        Agrega información específica de la bebida.
        """
        info_base = super().mostrar_informacion()
        return f"[Bebida] {info_base} | Volumen: {self.volumen_ml} ml"

    def servir(self) -> str:
        """
        Implementa el método servir para Bebida (Polimorfismo).
        """
        return f"La bebida '{self.nombre}' ({self.volumen_ml} ml) se está sirviendo en la barra. ¡Se servirá fría con hielo!"

