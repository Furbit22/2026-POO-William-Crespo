# -*- coding: utf-8 -*-
"""
Módulo de Producto para el Sistema de Restaurante
Define la clase Producto con sus atributos y métodos
"""


class Producto:
    """
    Clase que representa un producto disponible en el restaurante.

    Atributos:
        nombre (str): Nombre del producto
        precio (float): Precio del producto en unidades monetarias
        categoria (str): Categoría a la que pertenece el producto (ej: bebida, plato, postre)
    """

    def __init__(self, nombre, precio, categoria):
        """
        Constructor de la clase Producto.

        Args:
            nombre (str): Nombre del producto
            precio (float): Precio del producto
            categoria (str): Categoría del producto
        """
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria

    def __str__(self):
        """
        Retorna una representación en texto del producto.

        Returns:
            str: Representación legible del producto
        """
        return f"Producto: {self.nombre} | Precio: ${self.precio:.2f} | Categoría: {self.categoria}"

