class Celular:
    def __init__(self, marca, modelo, espacio, camara):
        self.marca = marca
        self.modelo = modelo
        self.espacio = espacio
        self.camara = camara

    def aumentar_almacenamiento(self):
        self.espacio = self.espacio + 256

    def mejorar_camara(self):
        self.camara = self.camara + 50

mi_telefono = Celular("iPhone", "16 Pro Max", 256, 48)
tu_telefono = Celular("Samsung", "Galaxy S24", 512, 200)

mi_telefono.aumentar_almacenamiento()
tu_telefono.mejorar_camara()

print(mi_telefono.espacio)
print(tu_telefono.camara)