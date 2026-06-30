# -*- coding: utf-8 -*-
"""
Punto de arranque del programa restaurante_app.
Este script crea objetos, los agrega al servicio principal y muestra los resultados.
"""
import sys
import os

# Asegurar que el directorio raíz del proyecto esté en el path de búsqueda
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modelos.platillo import Platillo
from modelos.bebida import Bebida
from servicios.restaurante import Restaurante

def main():
    print("--- INICIANDO SISTEMA RESTAURANTE APP ---")
    
    # 1. Crear instancia del servicio Restaurante
    mi_restaurante = Restaurante("El Rincón del Sabor")
    print()
    
    # 2. Crear objetos de tipo Platillo (mínimo dos)
    platillo1 = Platillo(nombre="Lomo Saltado", precio=12.50, tiempo_preparacion=20)
    platillo2 = Platillo(nombre="Ceviche Clásico", precio=15.00, tiempo_preparacion=15)
    
    # 3. Crear objetos de tipo Bebida (mínimo dos)
    bebida1 = Bebida(nombre="Chicha Morada", precio=3.50, volumen_ml=500)
    bebida2 = Bebida(nombre="Pisco Sour", precio=8.00, volumen_ml=250)
    print()

    # 4. Agregar objetos a la lista del servicio Restaurante
    mi_restaurante.agregar_producto(platillo1)
    mi_restaurante.agregar_producto(platillo2)
    mi_restaurante.agregar_producto(bebida1)
    mi_restaurante.agregar_producto(bebida2)
    
    # 5. Mostrar la información registrada demostrando polimorfismo
    mi_restaurante.mostrar_menu()
    
    # 6. Demostrar encapsulación y validación de precios
    print("--- DEMOSTRACIÓN DE VALIDACIÓN Y ENCAPSULACIÓN ---")
    print(f"Precio actual de {platillo1.nombre}: ${platillo1.obtener_precio():.2f}")
    
    # Intento de modificación no válida (precio negativo)
    print(f"\nIntentando cambiar precio de {platillo1.nombre} a -$5.00...")
    platillo1.cambiar_precio(-5.00)
    print(f"Precio después del intento: ${platillo1.obtener_precio():.2f}")
    
    # Intento de modificación no válida (precio cero)
    print(f"\nIntentando cambiar precio de {platillo1.nombre} a $0.00...")
    platillo1.cambiar_precio(0.00)
    print(f"Precio después del intento: ${platillo1.obtener_precio():.2f}")
    
    # Modificación válida
    print(f"\nIntentando cambiar precio de {platillo1.nombre} a $13.99...")
    if platillo1.cambiar_precio(13.99):
        print("¡Precio actualizado con éxito!")
    print(f"Precio final: ${platillo1.obtener_precio():.2f}")
    
    # Volver a mostrar el menú con el precio actualizado
    print("\n--- MENÚ ACTUALIZADO ---")
    mi_restaurante.mostrar_menu()

if __name__ == "__main__":
    main()
