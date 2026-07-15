import sys
from modelos.producto import Producto
from modelos.bebida import Bebida
from modelos.cliente import Cliente
from servicios.restaurante import Restaurante

def mostrar_menu() -> None:
    print("\n========================================")
    print("        SISTEMA DE RESTAURANTE")
    print("========================================")
    print("1. Registrar producto")
    print("2. Registrar bebida")
    print("3. Registrar cliente")
    print("----------------------------------------")
    print("4. Listar productos")
    print("5. Listar clientes")
    print("----------------------------------------")
    print("6. Salir")

def registrar_producto(servicio: Restaurante) -> None:
    print("\n--- Registrar Producto General ---")
    codigo = input("Ingrese el código del producto: ").strip()
    if not codigo:
        print("Error: El código no puede estar vacío.")
        return
    nombre = input("Ingrese el nombre del producto: ").strip()
    categoria = input("Ingrese la categoría: ").strip()
    try:
        precio = float(input("Ingrese el precio: ").strip())
        if precio < 0:
            print("Error: El precio no puede ser negativo.")
            return
    except ValueError:
        print("Error: El precio debe ser un número válido.")
        return

    producto = Producto(codigo, nombre, categoria, precio)
    if servicio.registrar_producto(producto):
        print("¡Producto registrado con éxito!")
    else:
        print(f"Error: Ya existe un producto con el código '{codigo}'.")

def registrar_bebida(servicio: Restaurante) -> None:
    print("\n--- Registrar Bebida ---")
    codigo = input("Ingrese el código de la bebida: ").strip()
    if not codigo:
        print("Error: El código no puede estar vacío.")
        return
    nombre = input("Ingrese el nombre de la bebida: ").strip()
    categoria = input("Ingrese la categoría (ej. Gaseosa, Jugo): ").strip()
    try:
        precio = float(input("Ingrese el precio: ").strip())
        if precio < 0:
            print("Error: El precio no puede ser negativo.")
            return
    except ValueError:
        print("Error: El precio debe ser un número válido.")
        return
    tamano = input("Ingrese el tamaño (ej. 500ml, 1.5L): ").strip()
    envase = input("Ingrese el tipo de envase (ej. Plástico, Vidrio, Lata): ").strip()

    bebida = Bebida(codigo, nombre, categoria, precio, tamano, envase)
    if servicio.registrar_producto(bebida):
        print("¡Bebida registrada con éxito!")
    else:
        print(f"Error: Ya existe un producto con el código '{codigo}'.")

def registrar_cliente(servicio: Restaurante) -> None:
    print("\n--- Registrar Cliente ---")
    identificacion = input("Ingrese la identificación (ID/Cédula): ").strip()
    if not identificacion:
        print("Error: La identificación no puede estar vacía.")
        return
    nombre = input("Ingrese el nombre del cliente: ").strip()
    correo = input("Ingrese el correo electrónico: ").strip()

    cliente = Cliente(identificacion, nombre, correo)
    if servicio.registrar_cliente(cliente):
        print("¡Cliente registrado con éxito!")
    else:
        print(f"Error: Ya existe un cliente con la identificación '{identificacion}'.")

def listar_productos(servicio: Restaurante) -> None:
    print("\n--- Listado de Productos ---")
    productos = servicio.obtener_productos()
    if not productos:
        print("No hay productos registrados en el sistema.")
        return
    for producto in productos:
        print(producto.mostrar_informacion())

def listar_clientes(servicio: Restaurante) -> None:
    print("\n--- Listado de Clientes ---")
    clientes = servicio.obtener_clientes()
    if not clientes:
        print("No hay clientes registrados en el sistema.")
        return
    for cliente in clientes:
        print(cliente.mostrar_informacion())

def main() -> None:
    servicio = Restaurante()
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            registrar_producto(servicio)
        elif opcion == "2":
            registrar_bebida(servicio)
        elif opcion == "3":
            registrar_cliente(servicio)
        elif opcion == "4":
            listar_productos(servicio)
        elif opcion == "5":
            listar_clientes(servicio)
        elif opcion == "6":
            print("Saliendo del sistema. ¡Hasta pronto!")
            sys.exit(0)
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
