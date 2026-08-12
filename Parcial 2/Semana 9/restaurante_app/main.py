import sys
from typing import Dict, Callable, Tuple
from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.restaurante import Restaurante

MENU_OPCIONES: Tuple[str, ...] = (
    "1. Registrar producto",
    "2. Buscar producto",
    "3. Actualizar producto",
    "4. Eliminar producto",
    "5. Listar productos",
    "6. Registrar usuario",
    "7. Listar usuarios",
    "8. Mostrar categorías",
    "9. Salir"
)

def mostrar_menu() -> None:
    print("\n========================================")
    print("        SISTEMA DE RESTAURANTE")
    print("========================================")
    for opcion in MENU_OPCIONES:
        if "6." in opcion:
            print("----------------------------------------")
        elif "8." in opcion:
            print("----------------------------------------")
        print(opcion)
    print("========================================")

def registrar_producto(servicio: Restaurante) -> None:
    print("\n--- Registrar Producto ---")
    codigo = input("Ingrese el código del producto: ").strip()
    if not codigo:
        print("Error: El código no puede estar vacío.")
        return
    nombre = input("Ingrese el nombre del producto: ").strip()
    if not nombre:
        print("Error: El nombre no puede estar vacío.")
        return
    categoria = input("Ingrese la categoría: ").strip()
    if not categoria:
        print("Error: La categoría no puede estar vacía.")
        return
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

def buscar_producto(servicio: Restaurante) -> None:
    print("\n--- Buscar Producto ---")
    codigo = input("Ingrese el código del producto a buscar: ").strip()
    producto = servicio.buscar_producto(codigo)
    if producto:
        print("\nProducto encontrado:")
        print(producto.mostrar_informacion())
    else:
        print(f"No se encontró ningún producto con el código '{codigo}'.")

def actualizar_producto(servicio: Restaurante) -> None:
    print("\n--- Actualizar Producto ---")
    codigo = input("Ingrese el código del producto a actualizar: ").strip()
    producto = servicio.buscar_producto(codigo)
    if not producto:
        print(f"No se encontró ningún producto con el código '{codigo}'.")
        return

    print(f"Datos actuales: {producto.mostrar_informacion()}")
    nombre = input("Ingrese el nuevo nombre (deje vacío para conservar el actual): ").strip()
    categoria = input("Ingrese la nueva categoría (deje vacío para conservar el actual): ").strip()
    precio_input = input("Ingrese el nuevo precio (deje vacío para conservar el actual): ").strip()
    
    nuevo_nombre = nombre if nombre else producto.nombre
    nueva_categoria = categoria if categoria else producto.categoria
    
    if precio_input:
        try:
            nuevo_precio = float(precio_input)
            if nuevo_precio < 0:
                print("Error: El precio no puede ser negativo.")
                return
        except ValueError:
            print("Error: El precio debe ser un número válido.")
            return
    else:
        nuevo_precio = producto.precio

    if servicio.actualizar_producto(codigo, nuevo_nombre, nueva_categoria, nuevo_precio):
        print("¡Producto actualizado con éxito!")
    else:
        print("Error al actualizar el producto.")

def eliminar_producto(servicio: Restaurante) -> None:
    print("\n--- Eliminar Producto ---")
    codigo = input("Ingrese el código del producto a eliminar: ").strip()
    if servicio.eliminar_producto(codigo):
        print(f"¡Producto con código '{codigo}' eliminado con éxito!")
    else:
        print(f"No se encontró ningún producto con el código '{codigo}'.")

def listar_productos(servicio: Restaurante) -> None:
    print("\n--- Listado de Productos ---")
    productos = servicio.obtener_productos()
    if not productos:
        print("No hay productos registrados en el sistema.")
        return
    for producto in productos:
        print(producto.mostrar_informacion())

def registrar_usuario(servicio: Restaurante) -> None:
    print("\n--- Registrar Usuario ---")
    identificacion = input("Ingrese la identificación: ").strip()
    if not identificacion:
        print("Error: La identificación no puede estar vacía.")
        return
    nombre = input("Ingrese el nombre del usuario: ").strip()
    if not nombre:
        print("Error: El nombre no puede estar vacío.")
        return
    correo = input("Ingrese el correo electrónico: ").strip()
    if not correo:
        print("Error: El correo no puede estar vacío.")
        return

    usuario = Usuario(identificacion, nombre, correo)
    if servicio.registrar_usuario(usuario):
        print("¡Usuario registrado con éxito!")
    else:
        print(f"Error: Ya existe un usuario con la identificación '{identificacion}'.")

def listar_usuarios(servicio: Restaurante) -> None:
    print("\n--- Listado de Usuarios ---")
    usuarios = servicio.obtener_usuarios()
    if not usuarios:
        print("No hay usuarios registrados en el sistema.")
        return
    for usuario in usuarios:
        print(usuario.mostrar_informacion())

def mostrar_categorias(servicio: Restaurante) -> None:
    print("\n--- Categorías Únicas de Productos ---")
    categorias = servicio.obtener_categorias_unicas()
    if not categorias:
        print("No hay categorías registradas o no hay productos aún.")
        return
    print("Categorías disponibles:")
    for cat in categorias:
        print(f"- {cat}")

def main() -> None:
    servicio = Restaurante()
    
    acciones: Dict[str, Callable[[Restaurante], None]] = {
        "1": registrar_producto,
        "2": buscar_producto,
        "3": actualizar_producto,
        "4": eliminar_producto,
        "5": listar_productos,
        "6": registrar_usuario,
        "7": listar_usuarios,
        "8": mostrar_categorias
    }

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "9":
            print("Saliendo del sistema. ¡Hasta pronto!")
            sys.exit(0)
        elif opcion in acciones:
            try:
                acciones[opcion](servicio)
            except Exception as e:
                print(f"Ocurrió un error inesperado al procesar la opción: {e}")
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
