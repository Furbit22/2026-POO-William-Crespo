# -*- coding: utf-8 -*-
from modelos.producto import Producto

class Platillo(Producto):
    """
    Clase hija que representa una comida o platillo del restaurante.
    Hereda de Producto y añade el atributo propio tiempo_preparacion.
    """
    def __init__(self, nombre: str, precio: float, tiempo_preparacion: int, disponible: bool = True):
        # Invocar constructor de la clase padre
        super().__init__(nombre, precio, disponible)
        # Atributo propio
        self.tiempo_preparacion = tiempo_preparacion  # Tiempo estimado en minutos

    def mostrar_informacion(self) -> str:
        """
        Sobrescribe el método de la clase padre (Polimorfismo).
        Agrega información específica del platillo.
        """
        info_base = super().mostrar_informacion()
        return f"[Platillo] {info_base} | Prep: {self.tiempo_preparacion} min"

    def servir(self) -> str:
        """
        Implementa el método servir para Platillo (Polimorfismo).
        """
        return f"El platillo '{self.nombre}' se está cocinando en cocina. Tiempo de espera: {self.tiempo_preparacion} min. ¡Se servirá caliente!"

