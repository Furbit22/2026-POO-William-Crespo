"""
main.py

Programa principal para la versión orientada a objetos. Crea instancias
de `Mascota` y demuestra el uso de sus métodos.
"""

from mascota import Mascota


def main():
    print("=== Gestión de mascotas (Programación Orientada a Objetos) ===")

    # Crear al menos dos objetos Mascota
    mascota1 = Mascota('Firulais', 'Perro', 5)
    mascota2 = Mascota('Misu', 'Gato', 3)

    # También se puede crear otra con una especie menos conocida
    mascota3 = Mascota('Piquito', 'Pájaro', 1)

    mascotas = [mascota1, mascota2, mascota3]

    # Ejecutar los métodos definidos y mostrar la información
    for m in mascotas:
        m.mostrar_informacion()
        m.hacer_sonido()


if __name__ == '__main__':
    main()

