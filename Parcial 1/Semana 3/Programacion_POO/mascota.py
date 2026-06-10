"""
mascota.py

Definición de la clase Mascota para la solución orientada a objetos.

La clase implementa atributos básicos (nombre, especie, edad) y los
métodos `mostrar_informacion()` y `hacer_sonido()`.
"""

class Mascota:
    """Clase que representa una mascota simple.

    Atributos:
        nombre (str): nombre de la mascota
        especie (str): especie de la mascota (por ejemplo: Perro, Gato)
        edad (int): edad en años
    """

    def __init__(self, nombre: str, especie: str, edad: int):
        self.nombre = nombre
        self.especie = especie
        self.edad = edad

    def mostrar_informacion(self):
        """Muestra la información básica de la mascota de forma organizada."""
        print("\n--- Información de la mascota ---")
        print(f"Nombre : {self.nombre}")
        print(f"Especie: {self.especie}")
        print(f"Edad   : {self.edad} años")
        print("--------------------------------")

    def hacer_sonido(self):
        """Imprime un sonido representativo según la especie.

        Se utiliza una aproximación simple: se compara la especie en
        minúsculas y se elige un sonido representativo. Si no se reconoce
        la especie, se muestra un mensaje genérico.
        """
        especie_key = (self.especie or "").strip().lower()
        sonidos = {
            'perro': 'Guau!',
            'perra': 'Guau!',
            'gato': 'Miau!',
            'gata': 'Miau!',
            'pájaro': 'Pío!',
            'pajaro': 'Pío!',
            'ave': 'Pío!',
            'conejo': '...silbidos suaves...'
        }
        sonido = sonidos.get(especie_key, 'Sonido desconocido (la mascota hace su propio sonido)')
        print(f"{self.nombre} dice: {sonido}\n")

