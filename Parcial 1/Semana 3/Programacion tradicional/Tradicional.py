"""
tradicional.py

Programa de gestión de mascotas — Enfoque: Programación Tradicional

Este programa registra y muestra la información básica de una mascota
sin utilizar clases ni objetos. Utiliza funciones y validación simple de
entrada por teclado.

Datos manejados por mascota:
- Nombre
- Especie
- Edad

Uso: ejecutar el script y seguir las indicaciones por teclado.
"""

def solicitar_texto(prompt):
    """Pide una cadena no vacía al usuario."""
    while True:
        valor = input(prompt).strip()
        if valor:
            return valor
        print("Entrada no válida. Por favor ingrese un valor no vacío.")


def solicitar_edad(prompt):
    """Pide un entero no negativo representando la edad (años)."""
    while True:
        valor = input(prompt).strip()
        try:
            edad = int(valor)
            if edad >= 0:
                return edad
            print("La edad debe ser un número entero no negativo.")
        except ValueError:
            print("Entrada inválida. Ingrese un número entero (por ejemplo: 3).")


def registrar_mascota():
    """Solicita los datos de la mascota y los devuelve en un diccionario."""
    print("=== Registro de mascota (Programación tradicional) ===")
    nombre = solicitar_texto("Nombre: ")
    especie = solicitar_texto("Especie: ")
    edad = solicitar_edad("Edad (en años): ")
    return {
        'nombre': nombre,
        'especie': especie,
        'edad': edad,
    }


def mostrar_mascota(mascota):
    """Muestra la información de la mascota de forma organizada."""
    print("\n--- Información registrada de la mascota ---")
    print(f"Nombre : {mascota['nombre']}")
    print(f"Especie: {mascota['especie']}")
    print(f"Edad   : {mascota['edad']} años")
    print("-------------------------------------------\n")


def main():
    mascota = registrar_mascota()
    mostrar_mascota(mascota)


if __name__ == '__main__':
    main()

