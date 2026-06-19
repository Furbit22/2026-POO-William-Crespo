# -*- coding: utf-8 -*-
"""
Módulo de servicios para el Sistema de Restaurante
Define la clase Restaurante que gestiona productos y clientes
"""

from modelos.producto import Producto
from modelos.cliente import Cliente


class Restaurante:
    """
    Clase que representa un restaurante y administra su negocio.

    Maneja el almacenamiento de productos disponibles y clientes registrados.
    Proporciona métodos para agregar productos, registrar clientes y mostrar información.
    """

    def __init__(self, nombre_restaurante):
        """
        Constructor de la clase Restaurante.

        Args:
            nombre_restaurante (str): Nombre del restaurante
        """
        self.nombre_restaurante = nombre_restaurante
        self.productos = []  # Lista para almacenar objetos Producto
        self.clientes = []   # Lista para almacenar objetos Cliente

    def agregar_producto(self, nombre, precio, categoria):
        """
        Agrega un nuevo producto al restaurante.

        Args:
            nombre (str): Nombre del producto
            precio (float): Precio del producto
            categoria (str): Categoría del producto

        Returns:
            bool: True si se agregó correctamente, False si el producto ya existe
        """
        # Verifica que el producto no exista ya en el menú
        for producto in self.productos:
            if producto.nombre.lower() == nombre.lower():
                print(f"⚠️  El producto '{nombre}' ya existe en el menú.")
                return False

        # Crea un nuevo producto y lo agrega a la lista
        nuevo_producto = Producto(nombre, precio, categoria)
        self.productos.append(nuevo_producto)
        print(f"✅ Producto '{nombre}' agregado correctamente.")
        return True

    def registrar_cliente(self, nombre, id_cliente):
        """
        Registra un nuevo cliente en el restaurante.

        Args:
            nombre (str): Nombre del cliente
            id_cliente (int): ID único del cliente

        Returns:
            bool: True si se registró correctamente, False si el ID ya existe
        """
        # Verifica que el ID del cliente sea único
        for cliente in self.clientes:
            if cliente.id_cliente == id_cliente:
                print(f"⚠️  El cliente con ID {id_cliente} ya está registrado.")
                return False

        # Crea un nuevo cliente y lo agrega a la lista
        nuevo_cliente = Cliente(nombre, id_cliente)
        self.clientes.append(nuevo_cliente)
        print(f"✅ Cliente '{nombre}' registrado correctamente.")
        return True

    def mostrar_menu(self):
        """
        Muestra el menú de productos disponibles en el restaurante.
        Agrupa los productos por categoría para mejor presentación.
        """
        if not self.productos:
            print("\n📋 El menú está vacío.")
            return

        print(f"\n{'='*60}")
        print(f"{'MENÚ - ' + self.nombre_restaurante:^60}")
        print(f"{'='*60}")

        # Obtiene todas las categorías únicas
        categorias = set(producto.categoria for producto in self.productos)

        # Agrupa y muestra productos por categoría
        for categoria in sorted(categorias):
            print(f"\n🍽️  {categoria.upper()}")
            print("-" * 60)

            for producto in self.productos:
                if producto.categoria == categoria:
                    print(f"  • {producto.nombre:<30} ${producto.precio:>7.2f}")

        print(f"\n{'='*60}\n")

    def mostrar_clientes(self):
        """
        Muestra la lista de clientes registrados en el restaurante.
        """
        if not self.clientes:
            print("\n👥 No hay clientes registrados aún.")
            return

        print(f"\n{'='*60}")
        print(f"{'CLIENTES REGISTRADOS - ' + self.nombre_restaurante:^60}")
        print(f"{'='*60}\n")

        # Itera sobre la lista de clientes y los muestra
        for idx, cliente in enumerate(self.clientes, 1):
            print(f"{idx}. {cliente}")

        print(f"\n{'='*60}\n")

    def __str__(self):
        """
        Retorna una representación en texto del restaurante.

        Returns:
            str: Información del restaurante
        """
        return (f"Restaurante: {self.nombre_restaurante} | "
                f"Productos: {len(self.productos)} | Clientes: {len(self.clientes)}")

