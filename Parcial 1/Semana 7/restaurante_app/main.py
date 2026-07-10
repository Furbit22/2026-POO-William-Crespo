import sys
# Asegurar la correcta importación si se ejecuta directamente desde la raíz
# o desde la carpeta restaurante_app.
from modelos.producto import Producto
from modelos.cliente import Cliente
from servicios.restaurante import Restaurante

def mostrar_menu():
    """Imprime el menú de opciones en consola."""
    print("\n" + "=" * 40)
    print("        SISTEMA DE RESTAURANTE")
    print("=" * 40)
    print("1. Registrar producto")
    print("2. Listar productos")
    print("3. Buscar producto")
    print("-" * 40)
    print("4. Registrar cliente")
    print("5. Listar clientes")
    print("6. Buscar cliente")
    print("-" * 40)
    print("7. Salir")
    print("=" * 40)

def registrar_producto(servicio: Restaurante):
    """Solicita datos al usuario y registra un nuevo producto."""
    print("\n--- Registro de Producto ---")
    nombre = input("Ingrese el nombre del producto: ").strip()
    categoria = input("Ingrese la categoría del producto: ").strip()
    
    try:
        precio_input = input("Ingrese el precio del producto: ").strip()
        precio = float(precio_input)
    except ValueError:
        print("Error: El precio debe ser un valor numérico.")
        return

    opcion_disponible = input("¿Está disponible? (S/N, por defecto S): ").strip().upper()
    disponible = False if opcion_disponible == "N" else True

    try:
        # Se crea el objeto Producto; el constructor valida los datos mediante los setters
        nuevo_producto = Producto(nombre, categoria, precio, disponible)
        servicio.registrar_producto(nuevo_producto)
        print(f"\n¡Éxito! Producto '{nuevo_producto.nombre}' registrado correctamente.")
    except ValueError as e:
        print(f"\nError de validación: {e}")

def listar_productos(servicio: Restaurante):
    """Muestra todos los productos registrados en el sistema."""
    productos = servicio.listar_productos()
    print("\n--- Lista de Productos ---")
    if not productos:
        print("No hay productos registrados en el sistema.")
        return
    for i, producto in enumerate(productos, 1):
        print(f"{i}. {producto.mostrar_informacion()}")

def buscar_producto(servicio: Restaurante):
    """Busca productos por su nombre."""
    print("\n--- Buscar Producto ---")
    nombre_buscar = input("Ingrese el nombre del producto a buscar: ").strip()
    if not nombre_buscar:
        print("Error: Debe ingresar un criterio de búsqueda.")
        return
    
    resultados = servicio.buscar_producto(nombre_buscar)
    if not resultados:
        print(f"No se encontraron productos que coincidan con '{nombre_buscar}'.")
        return
    
    print(f"\nResultados de búsqueda para '{nombre_buscar}':")
    for producto in resultados:
        print(f"- {producto.mostrar_informacion()}")

def registrar_cliente(servicio: Restaurante):
    """Solicita datos al usuario y registra un nuevo cliente."""
    print("\n--- Registro de Cliente ---")
    nombre = input("Ingrese el nombre del cliente: ").strip()
    correo = input("Ingrese el correo del cliente: ").strip()
    id_cliente = input("Ingrese el identificador (ID) del cliente: ").strip()

    # Validaciones básicas antes de instanciar la dataclass
    if not nombre:
        print("Error: El nombre del cliente no puede estar vacío.")
        return
    if not correo:
        print("Error: El correo del cliente no puede estar vacío.")
        return
    if not id_cliente:
        print("Error: El identificador del cliente no puede estar vacío.")
        return

    # Creamos el objeto Cliente usando dataclass
    nuevo_cliente = Cliente(nombre, correo, id_cliente)
    servicio.registrar_cliente(nuevo_cliente)
    print(f"\n¡Éxito! Cliente '{nuevo_cliente.nombre}' con ID '{nuevo_cliente.id_cliente}' registrado correctamente.")

def listar_clientes(servicio: Restaurante):
    """Muestra todos los clientes registrados en el sistema."""
    clientes = servicio.listar_clientes()
    print("\n--- Lista de Clientes ---")
    if not clientes:
        print("No hay clientes registrados en el sistema.")
        return
    for i, cliente in enumerate(clientes, 1):
        print(f"{i}. ID: {cliente.id_cliente} | Nombre: {cliente.nombre} | Correo: {cliente.correo}")

def buscar_cliente(servicio: Restaurante):
    """Busca un cliente por su identificador único."""
    print("\n--- Buscar Cliente ---")
    id_buscar = input("Ingrese el ID del cliente a buscar: ").strip()
    if not id_buscar:
        print("Error: Debe ingresar el ID del cliente.")
        return
    
    cliente = servicio.buscar_cliente(id_buscar)
    if not cliente:
        print(f"No se encontró ningún cliente con el ID '{id_buscar}'.")
        return
    
    print("\nCliente encontrado:")
    print(f"ID: {cliente.id_cliente}")
    print(f"Nombre: {cliente.nombre}")
    print(f"Correo: {cliente.correo}")

def main():
    # Instanciamos el servicio principal del restaurante
    servicio_restaurante = Restaurante()
    
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-7): ").strip()
        
        if opcion == "1":
            registrar_producto(servicio_restaurante)
        elif opcion == "2":
            listar_productos(servicio_restaurante)
        elif opcion == "3":
            buscar_producto(servicio_restaurante)
        elif opcion == "4":
            registrar_cliente(servicio_restaurante)
        elif opcion == "5":
            listar_clientes(servicio_restaurante)
        elif opcion == "6":
            buscar_cliente(servicio_restaurante)
        elif opcion == "7":
            print("\n¡Gracias por utilizar el Sistema de Restaurante! Saliendo del programa...")
            break
        else:
            print("\nOpción no válida. Por favor, intente de nuevo con un número del 1 al 7.")

if __name__ == "__main__":
    main()
