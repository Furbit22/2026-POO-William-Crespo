import os
import json
from typing import List
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta

class ArchivoServicio:
    """
    Servicio encargado de la persistencia de datos en archivos JSON.
    Gestiona la carga y almacenamiento de productos, usuarios y ventas,
    controlando excepciones de archivos y formato de manera centralizada.
    """
    def __init__(self, ruta_productos: str, ruta_usuarios: str, ruta_ventas: str) -> None:
        self.ruta_productos: str = ruta_productos
        self.ruta_usuarios: str = ruta_usuarios
        self.ruta_ventas: str = ruta_ventas
        
        # Asegurar que existan los directorios padre
        for ruta in [self.ruta_productos, self.ruta_usuarios, self.ruta_ventas]:
            directorio = os.path.dirname(ruta)
            if directorio:
                os.makedirs(directorio, exist_ok=True)

    def cargar_productos(self) -> List[Producto]:
        """Carga los productos desde el archivo JSON correspondiente."""
        productos: List[Producto] = []
        if not os.path.exists(self.ruta_productos):
            return productos

        try:
            with open(self.ruta_productos, "r", encoding="utf-8") as f:
                datos = json.load(f)
                items = datos if isinstance(datos, list) else list(datos.values())
                
                for item in items:
                    try:
                        producto = Producto.desde_diccionario(item)
                        productos.append(producto)
                    except KeyError as e:
                        print(f"Advertencia: Se omitió un producto por falta del campo obligatorio {e}: {item}")
                    except ValueError as e:
                        print(f"Advertencia: Se omitió un producto por datos inválidos ({e}): {item}")
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as e:
            print(f"Error: El archivo de productos JSON no tiene un formato válido: {e}")
        except PermissionError as e:
            print(f"Error: Permiso denegado al leer el archivo de productos: {e}")
        except Exception as e:
            print(f"Error inesperado al cargar productos: {e}")

        return productos

    def guardar_productos(self, productos: List[Producto]) -> None:
        """Guarda la lista de productos en el archivo JSON."""
        try:
            datos = [p.a_diccionario() for p in productos]
            with open(self.ruta_productos, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
        except PermissionError as e:
            print(f"Error: Permiso denegado al escribir el archivo de productos: {e}")
        except Exception as e:
            print(f"Error inesperado al guardar productos: {e}")

    def cargar_usuarios(self) -> List[Usuario]:
        """Carga los usuarios desde el archivo JSON correspondiente."""
        usuarios: List[Usuario] = []
        if not os.path.exists(self.ruta_usuarios):
            return usuarios

        try:
            with open(self.ruta_usuarios, "r", encoding="utf-8") as f:
                datos = json.load(f)
                items = datos if isinstance(datos, list) else list(datos.values())
                
                for item in items:
                    try:
                        usuario = Usuario.desde_diccionario(item)
                        usuarios.append(usuario)
                    except KeyError as e:
                        print(f"Advertencia: Se omitió un usuario por falta del campo obligatorio {e}: {item}")
                    except ValueError as e:
                        print(f"Advertencia: Se omitió un usuario por datos inválidos ({e}): {item}")
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as e:
            print(f"Error: El archivo de usuarios JSON no tiene un formato válido: {e}")
        except PermissionError as e:
            print(f"Error: Permiso denegado al leer el archivo de usuarios: {e}")
        except Exception as e:
            print(f"Error inesperado al cargar usuarios: {e}")

        return usuarios

    def guardar_usuarios(self, usuarios: List[Usuario]) -> None:
        """Guarda la lista de usuarios en el archivo JSON."""
        try:
            datos = [u.a_diccionario() for u in usuarios]
            with open(self.ruta_usuarios, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
        except PermissionError as e:
            print(f"Error: Permiso denegado al escribir el archivo de usuarios: {e}")
        except Exception as e:
            print(f"Error inesperado al guardar usuarios: {e}")

    def cargar_ventas(self) -> List[Venta]:
        """Carga las ventas desde el archivo JSON correspondiente."""
        ventas: List[Venta] = []
        if not os.path.exists(self.ruta_ventas):
            return ventas

        try:
            with open(self.ruta_ventas, "r", encoding="utf-8") as f:
                datos = json.load(f)
                items = datos if isinstance(datos, list) else list(datos.values())
                
                for item in items:
                    try:
                        venta = Venta.desde_diccionario(item)
                        ventas.append(venta)
                    except KeyError as e:
                        print(f"Advertencia: Se omitió una venta por falta del campo obligatorio {e}: {item}")
                    except ValueError as e:
                        print(f"Advertencia: Se omitió una venta por datos inválidos ({e}): {item}")
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as e:
            print(f"Error: El archivo de ventas JSON no tiene un formato válido: {e}")
        except PermissionError as e:
            print(f"Error: Permiso denegado al leer el archivo de ventas: {e}")
        except Exception as e:
            print(f"Error inesperado al cargar ventas: {e}")

        return ventas

    def guardar_ventas(self, ventas: List[Venta]) -> None:
        """Guarda la lista de transacciones de venta en el archivo JSON."""
        try:
            datos = [v.a_diccionario() for v in ventas]
            with open(self.ruta_ventas, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
        except PermissionError as e:
            print(f"Error: Permiso denegado al escribir el archivo de ventas: {e}")
        except Exception as e:
            print(f"Error inesperado al guardar ventas: {e}")
