# -*- coding: utf-8 -*-
"""
Módulo de Cliente para el Sistema de Restaurante
Define la clase Cliente con sus atributos y métodos
"""


class Cliente:
    """
    Clase que representa un cliente del restaurante.

    Atributos:
        nombre (str): Nombre completo del cliente
        id_cliente (int): Identificador único del cliente
    """

    def __init__(self, nombre, id_cliente):
        """
        Constructor de la clase Cliente.

        Args:
            nombre (str): Nombre completo del cliente
            id_cliente (int): Identificador único asignado al cliente
        """
        self.nombre = nombre
        self.id_cliente = id_cliente

    def __str__(self):
        """
        Retorna una representación en texto del cliente.

        Returns:
            str: Representación legible del cliente
        """
        return f"Cliente: {self.nombre} | ID: {self.id_cliente}"

