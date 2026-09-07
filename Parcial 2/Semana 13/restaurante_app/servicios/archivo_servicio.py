import os
import json
from typing import List
from modelos.producto import Producto
from modelos.usuario import Usuario

class ArchivoServicio:
    """
    Servicio encargado de la persistencia de datos en archivos JSON.
    Gestiona la carga y almacenamiento de productos y usuarios,
    centralizando el manejo de excepciones de E/S y formato.
    """
    def __init__(self, ruta_productos: str, ruta_usuarios: str) -> None:
        self.ruta_productos: str = ruta_productos
        self.ruta_usuarios: str = ruta_usuarios

        # Asegurar la existencia de las carpetas contenedoras
        for ruta in [self.ruta_productos, self.ruta_usuarios]:
            directorio = os.path.dirname(ruta)
            if directorio:
                os.makedirs(directorio, exist_ok=True)

    def cargar_productos(self) -> List[Producto]:
        """
        Carga los productos desde el archivo JSON especificado.
        Controla excepciones y descarta registros mal formados sin interrumpir la ejecución.
        """
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
                    except (KeyError, ValueError) as e:
                        print(f"[ArchivoServicio] Registro de producto omitido por error: {e}")
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as e:
            print(f"[ArchivoServicio] Error de formato JSON en productos: {e}")
        except PermissionError as e:
            print(f"[ArchivoServicio] Permiso denegado al leer productos: {e}")
        except Exception as e:
            print(f"[ArchivoServicio] Error inesperado al cargar productos: {e}")

        return productos

    def guardar_productos(self, productos: List[Producto]) -> bool:
        """Guarda la lista de objetos Producto en el archivo JSON."""
        try:
            datos = [p.a_diccionario() for p in productos]
            with open(self.ruta_productos, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            return True
        except PermissionError as e:
            print(f"[ArchivoServicio] Permiso denegado al escribir productos: {e}")
            return False
        except Exception as e:
            print(f"[ArchivoServicio] Error al guardar productos: {e}")
            return False

    def cargar_usuarios(self) -> List[Usuario]:
        """
        Carga los usuarios desde el archivo JSON especificado.
        Controla excepciones y descarta registros mal formados sin interrumpir la ejecución.
        """
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
                    except (KeyError, ValueError) as e:
                        print(f"[ArchivoServicio] Registro de usuario omitido por error: {e}")
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as e:
            print(f"[ArchivoServicio] Error de formato JSON en usuarios: {e}")
        except PermissionError as e:
            print(f"[ArchivoServicio] Permiso denegado al leer usuarios: {e}")
        except Exception as e:
            print(f"[ArchivoServicio] Error inesperado al cargar usuarios: {e}")

        return usuarios

    def guardar_usuarios(self, usuarios: List[Usuario]) -> bool:
        """Guarda la lista de objetos Usuario en el archivo JSON."""
        try:
            datos = [u.a_diccionario() for u in usuarios]
            with open(self.ruta_usuarios, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            return True
        except PermissionError as e:
            print(f"[ArchivoServicio] Permiso denegado al escribir usuarios: {e}")
            return False
        except Exception as e:
            print(f"[ArchivoServicio] Error al guardar usuarios: {e}")
            return False
