# Importar clases del sistema
from servicios.restaurante import Restaurante
from modelos.producto import Producto
from modelos.cliente import Cliente

# Punto de entrada del programa
if __name__ == '__main__':
    # Crear instancia del restaurante con nombre descriptivo
    restaurante_principal: Restaurante = Restaurante('El Buen Sabor')

    # Crear primer producto - Comida tradicional
    producto_1: Producto = Producto(
        nombre='Ceviche Peruano',
        precio=18.50,
        stock=25,
        disponible=True
    )

    # Crear segundo producto - Bebida tradicional
    producto_2: Producto = Producto(
        nombre='Chicha Morada',
        precio=5.00,
        stock=40,
        disponible=True
    )

    # Crear primer cliente
    cliente_1: Cliente = Cliente(
        cedula='1023456789',
        nombre_completo='Carlos Mendoza García',
        edad=35,
        es_frecuente=True
    )

    # Crear segundo cliente
    cliente_2: Cliente = Cliente(
        cedula='1087654321',
        nombre_completo='María López Rodríguez',
        edad=28,
        es_frecuente=False
    )

    # Agregar productos al restaurante
    restaurante_principal.agregar_producto(producto_1)
    restaurante_principal.agregar_producto(producto_2)

    # Registrar clientes en el restaurante
    restaurante_principal.registrar_cliente(cliente_1)
    restaurante_principal.registrar_cliente(cliente_2)

    # Mostrar toda la información del sistema
    restaurante_principal.mostrar_informacion_sistema()
