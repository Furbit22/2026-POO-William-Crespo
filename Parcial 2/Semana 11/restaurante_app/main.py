import sys
import os
from typing import Dict, Callable, Tuple
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.restaurante import Restaurante
from servicios.archivo_servicio import ArchivoServicio

MENU_OPCIONES: Tuple[str, ...] = (
    "1. Registrar producto",
    "2. Buscar producto",
    "3. Actualizar producto",
    "4. Eliminar producto",
    "5. Listar productos",
    "6. Registrar usuario",
    "7. Listar usuarios",
    "8. Mostrar categorías",
    "9. Realizar venta",
    "10. Consultar ventas de un usuario",
    "11. Salir"
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
        elif "9." in opcion:
            print("----------------------------------------")
        print(opcion)
    print("========================================")

def registrar_producto(servicio: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    print("\n--- Registrar Producto ---")
    codigo = input("Ingrese el código del producto: ").strip()
    nombre = input("Ingrese el nombre del producto: ").strip()
    categoria = input("Ingrese la categoría: ").strip()
    precio_input = input("Ingrese el precio: ").strip()
    stock_input = input("Ingrese el stock inicial: ").strip()

    try:
        precio = float(precio_input)
    except ValueError:
        print("Error: El precio debe ser un número válido.")
        return

    try:
        stock = int(stock_input)
    except ValueError:
        print("Error: El stock debe ser un número entero válido.")
        return

    try:
        producto = Producto(codigo, nombre, categoria, precio, stock)
        if servicio.registrar_producto(producto):
            archivo_servicio.guardar_productos(servicio.obtener_productos())
            print("¡Producto registrado con éxito!")
        else:
            print(f"Error: Ya existe un producto con el código '{codigo}'.")
    except ValueError as e:
        print(f"Error de validación: {e}")

def buscar_producto(servicio: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    print("\n--- Buscar Producto ---")
    codigo = input("Ingrese el código del producto a buscar: ").strip()
    producto = servicio.buscar_producto(codigo)
    if producto:
        print("\nProducto encontrado:")
        print(producto.mostrar_informacion())
    else:
        print(f"No se encontró ningún producto con el código '{codigo}'.")

def actualizar_producto(servicio: Restaurante, archivo_servicio: ArchivoServicio) -> None:
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
    stock_input = input("Ingrese el nuevo stock (deje vacío para conservar el actual): ").strip()
    
    nuevo_nombre = nombre if nombre else producto.nombre
    nueva_categoria = categoria if categoria else producto.categoria
    
    if precio_input:
        try:
            nuevo_precio = float(precio_input)
        except ValueError:
            print("Error: El precio debe ser un número válido.")
            return
    else:
        nuevo_precio = producto.precio

    if stock_input:
        try:
            nuevo_stock = int(stock_input)
        except ValueError:
            print("Error: El stock debe ser un número entero válido.")
            return
    else:
        nuevo_stock = producto.stock

    try:
        if servicio.actualizar_producto(codigo, nuevo_nombre, nueva_categoria, nuevo_precio, nuevo_stock):
            archivo_servicio.guardar_productos(servicio.obtener_productos())
            print("¡Producto actualizado con éxito!")
        else:
            print("Error al actualizar el producto.")
    except ValueError as e:
        print(f"Error de validación al actualizar: {e}")

def eliminar_producto(servicio: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    print("\n--- Eliminar Producto ---")
    codigo = input("Ingrese el código del producto a eliminar: ").strip()
    if servicio.eliminar_producto(codigo):
        archivo_servicio.guardar_productos(servicio.obtener_productos())
        print(f"¡Producto con código '{codigo}' eliminado con éxito!")
    else:
        print(f"No se encontró ningún producto con el código '{codigo}'.")

def listar_productos(servicio: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    print("\n--- Listado de Productos ---")
    productos = servicio.obtener_productos()
    if not productos:
        print("No hay productos registrados en el sistema.")
        return
    for producto in productos:
        print(producto.mostrar_informacion())

def registrar_usuario(servicio: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    print("\n--- Registrar Usuario ---")
    identificacion = input("Ingrese la identificación: ").strip()
    nombre = input("Ingrese el nombre del usuario: ").strip()
    correo = input("Ingrese el correo electrónico: ").strip()

    try:
        usuario = Usuario(identificacion, nombre, correo)
        if servicio.registrar_usuario(usuario):
            archivo_servicio.guardar_usuarios(servicio.obtener_usuarios())
            print("¡Usuario registrado con éxito!")
        else:
            print(f"Error: Ya existe un usuario con la identificación '{identificacion}'.")
    except ValueError as e:
        print(f"Error de validación: {e}")

def listar_usuarios(servicio: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    print("\n--- Listado de Usuarios ---")
    usuarios = servicio.obtener_usuarios()
    if not usuarios:
        print("No hay usuarios registrados en el sistema.")
        return
    for usuario in usuarios:
        print(usuario.mostrar_informacion())

def mostrar_categorias(servicio: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    print("\n--- Categorías Únicas de Productos ---")
    categorias = servicio.obtener_categorias_unicas()
    if not categorias:
        print("No hay categorías registradas o no hay productos aún.")
        return
    print("Categorías disponibles:")
    for cat in categorias:
        print(f"- {cat}")

def realizar_venta(servicio: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    print("\n--- Realizar Venta ---")
    identificacion_usuario = input("Ingrese la identificación del usuario: ").strip()
    
    usuario = servicio.buscar_usuario(identificacion_usuario)
    if not usuario:
        print(f"Error: No existe el usuario con identificación '{identificacion_usuario}'.")
        return

    codigo_producto = input("Ingrese el código del producto: ").strip()
    producto = servicio.buscar_producto(codigo_producto)
    if not producto:
        print(f"Error: No existe el producto con código '{codigo_producto}'.")
        return

    cantidad_input = input("Ingrese la cantidad a vender: ").strip()
    try:
        cantidad = int(cantidad_input)
    except ValueError:
        print("Error: La cantidad debe ser un número entero válido.")
        return

    try:
        if servicio.vender_producto(codigo_producto, identificacion_usuario, cantidad):
            # Guardar tanto ventas.json como productos.json (porque se redujo el stock)
            archivo_servicio.guardar_ventas(servicio.obtener_ventas())
            archivo_servicio.guardar_productos(servicio.obtener_productos())
            print(f"¡Venta realizada con éxito! Se vendieron {cantidad} unidad(es) de '{producto.nombre}' al usuario '{usuario.nombre}'.")
        else:
            print("Error: No se pudo completar la venta.")
    except ValueError as e:
        print(f"Error al realizar venta: {e}")

def consultar_ventas_usuario(servicio: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    print("\n--- Consultar Ventas de un Usuario ---")
    identificacion_usuario = input("Ingrese la identificación del usuario: ").strip()
    
    usuario = servicio.buscar_usuario(identificacion_usuario)
    if not usuario:
        print(f"Error: No existe el usuario con identificación '{identificacion_usuario}'.")
        return

    ventas = servicio.consultar_ventas_usuario(identificacion_usuario)
    if not ventas:
        print(f"El usuario '{usuario.nombre}' no tiene ventas registradas.")
        return

    print(f"\nCompras de {usuario.nombre} (ID: {usuario.identificacion}):")
    for i, venta in enumerate(ventas, 1):
        producto = servicio.buscar_producto(venta.producto_codigo)
        nombre_prod = producto.nombre if producto else "Producto no encontrado (Código: " + venta.producto_codigo + ")"
        print(f"{i}. Producto: {nombre_prod} (Código: {venta.producto_codigo}) | Cantidad: {venta.cantidad}")

def main() -> None:
    # Determinar rutas relativas al archivo main.py
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_productos = os.path.join(base_dir, "datos", "productos.json")
    ruta_usuarios = os.path.join(base_dir, "datos", "usuarios.json")
    ruta_ventas = os.path.join(base_dir, "datos", "ventas.json")

    # Inicializar el servicio de archivos
    archivo_servicio = ArchivoServicio(ruta_productos, ruta_usuarios, ruta_ventas)
    
    # Cargar datos guardados previamente
    print("Cargando base de datos...")
    productos_cargados = archivo_servicio.cargar_productos()
    usuarios_cargados = archivo_servicio.cargar_usuarios()
    ventas_cargadas = archivo_servicio.cargar_ventas()
    
    # Inicializar el servicio principal Restaurante con las colecciones persistidas
    servicio = Restaurante(productos_cargados, usuarios_cargados, ventas_cargadas)
    
    acciones: Dict[str, Callable[[Restaurante, ArchivoServicio], None]] = {
        "1": registrar_producto,
        "2": buscar_producto,
        "3": actualizar_producto,
        "4": eliminar_producto,
        "5": listar_productos,
        "6": registrar_usuario,
        "7": listar_usuarios,
        "8": mostrar_categorias,
        "9": realizar_venta,
        "10": consultar_ventas_usuario
    }

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "11":
            print("Saliendo del sistema. ¡Hasta pronto!")
            sys.exit(0)
        elif opcion in acciones:
            try:
                acciones[opcion](servicio, archivo_servicio)
            except Exception as e:
                print(f"Ocurrió un error inesperado al procesar la opción: {e}")
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
