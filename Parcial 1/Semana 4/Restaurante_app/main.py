# -*- coding: utf-8 -*-
"""
Archivo de demostración del Sistema de Restaurante
Ejemplo de uso de las clases Producto, Cliente y Restaurante
"""

from servicios.restaurante import Restaurante


def main():
    """Función principal que demuestra el uso de las clases"""

    # Crear una instancia del restaurante
    restaurante = Restaurante("La Buena Mesa")
    print(f"🏪 {restaurante}\n")

    # ========== AGREGAR PRODUCTOS ==========
    print("📦 AGREGANDO PRODUCTOS AL MENÚ:")
    print("-" * 60)
    restaurante.agregar_producto("Hamburguesa", 8.99, "Plato Principal")
    restaurante.agregar_producto("Pizza Margarita", 12.50, "Plato Principal")
    restaurante.agregar_producto("Ensalada César", 7.50, "Entrada")
    restaurante.agregar_producto("Coca Cola", 2.50, "Bebida")
    restaurante.agregar_producto("Cerveza", 3.00, "Bebida")
    restaurante.agregar_producto("Flan", 3.75, "Postre")
    restaurante.agregar_producto("Helado de Vainilla", 2.99, "Postre")

    # Intentar agregar un producto duplicado
    restaurante.agregar_producto("Hamburguesa", 9.99, "Plato Principal")

    # ========== MOSTRAR MENÚ ==========
    restaurante.mostrar_menu()

    # ========== REGISTRAR CLIENTES ==========
    print("👥 REGISTRANDO CLIENTES:")
    print("-" * 60)
    restaurante.registrar_cliente("Juan Pérez", 1001)
    restaurante.registrar_cliente("María García", 1002)
    restaurante.registrar_cliente("Carlos López", 1003)
    restaurante.registrar_cliente("Ana Martínez", 1004)

    # Intentar registrar un cliente con ID duplicado
    restaurante.registrar_cliente("Luis González", 1001)

    # ========== MOSTRAR CLIENTES ==========
    restaurante.mostrar_clientes()

    # ========== INFORMACIÓN FINAL ==========
    print(f"📊 INFORMACIÓN FINAL: {restaurante}\n")


if __name__ == "__main__":
    main()

