import os
import json
from typing import List
from modelos.producto import Producto
from modelos.usuario import Usuario

class ArchivoServicio:
    def __init__(self, ruta_productos: str, ruta_usuarios: str) -> None:
        self.ruta_productos: str = ruta_productos
        self.ruta_usuarios: str = ruta_usuarios
        
        # Asegurar que existan los directorios padre
        for ruta in [self.ruta_productos, self.ruta_usuarios]:
            directorio = os.path.dirname(ruta)
            if directorio:
                os.makedirs(directorio, exist_ok=True)

    def cargar_productos(self) -> List[Producto]:
        productos: List[Producto] = []
        if not os.path.exists(self.ruta_productos):
            # FileNotFoundError se maneja implícitamente al verificar existencia
            return productos

        try:
            with open(self.ruta_productos, "r", encoding="utf-8") as f:
                datos = json.load(f)
                
                # Soportar tanto formato de lista como diccionario (por compatibilidad)
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
            # Por si acaso ocurre una condición de carrera
            return []
        except json.JSONDecodeError as e:
            print(f"Error: El archivo de productos JSON no tiene un formato válido: {e}")
        except PermissionError as e:
            print(f"Error: Permiso denegado al leer el archivo de productos: {e}")
        except Exception as e:
            print(f"Error inesperado al cargar productos: {e}")

        return productos

    def guardar_productos(self, productos: List[Producto]) -> None:
        try:
            datos = [p.a_diccionario() for p in productos]
            with open(self.ruta_productos, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
        except PermissionError as e:
            print(f"Error: Permiso denegado al escribir el archivo de productos: {e}")
        except Exception as e:
            print(f"Error inesperado al guardar productos: {e}")

    def cargar_usuarios(self) -> List[Usuario]:
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
        try:
            datos = [u.a_diccionario() for u in usuarios]
            with open(self.ruta_usuarios, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
        except PermissionError as e:
            print(f"Error: Permiso denegado al escribir el archivo de usuarios: {e}")
        except Exception as e:
            print(f"Error inesperado al guardar usuarios: {e}")
