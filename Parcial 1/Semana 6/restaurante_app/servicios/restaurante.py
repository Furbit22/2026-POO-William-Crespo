# -*- coding: utf-8 -*-
from typing import List
from modelos.producto import Producto

class Restaurante:
    """
    Clase de servicio encargada de administrar una lista de productos registrados
    y mostrar la información de forma organizada.
    """
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.__productos: List[Producto] = []  # Lista privada para almacenar los productos

    def agregar_producto(self, producto: Producto):
        """Agrega un producto al menú del restaurante."""
        self.__productos.append(producto)
        print(f"Producto '{producto.nombre}' registrado con éxito en el restaurante '{self.nombre}'.")

    def mostrar_menu(self):
        """
        Muestra la información de todos los productos.
        Demuestra polimorfismo al ejecutar mostrar_informacion() sobre
        los elementos de la lista sin importar si son Platillo o Bebida.
        """
        print("\n" + "=" * 60)
        print(f"MENÚ DEL RESTAURANTE: {self.nombre.upper()}")
        print("=" * 60)
        
        if not self.__productos:
            print("No hay productos registrados en el menú.")
            return

        for index, producto in enumerate(self.__productos, start=1):
            # Aquí ocurre el polimorfismo: se ejecuta mostrar_informacion() 
            # de acuerdo al tipo dinámico del objeto (Platillo o Bebida)
            print(f"{index}. {producto.mostrar_informacion()}")
            
        print("=" * 60 + "\n")

    def preparar_y_servir_todo(self):
        """
        Itera sobre todos los productos y ejecuta el método servir().
        Esto demuestra polimorfismo dinámico al ejecutar diferentes comportamientos
        específicos según si el objeto es un Platillo o una Bebida.
        """
        print("\n" + "=" * 60)
        print(f"PREPARACIÓN Y SERVICIO EN: {self.nombre.upper()}")
        print("=" * 60)
        
        if not self.__productos:
            print("No hay productos para servir.")
            return

        for index, producto in enumerate(self.__productos, start=1):
            print(f"{index}. {producto.servir()}")
            
        print("=" * 60 + "\n")

