import os
import json
from typing import List, Optional
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta

class ArchivoServicio:
    """
    Servicio de persistencia en archivos JSON para restaurante_app.
    Centraliza la lectura y escritura exclusiva de productos, usuarios y ventas,
    controlando excepciones de E/S y formato para garantizar la integridad de los datos.
    """
    def __init__(
        self,
        ruta_productos: str,
        ruta_usuarios: str,
        ruta_ventas: Optional[str] = None
    ) -> None:
        self.ruta_productos: str = ruta_productos
        self.ruta_usuarios: str = ruta_usuarios
        self.ruta_ventas: Optional[str] = ruta_ventas

        # Asegurar existencia de directorios de persistencia
        rutas_a_verificar = [self.ruta_productos, self.ruta_usuarios]
        if self.ruta_ventas:
            rutas_a_verificar.append(self.ruta_ventas)

        for ruta in rutas_a_verificar:
            directorio = os.path.dirname(ruta)
            if directorio:
                os.makedirs(directorio, exist_ok=True)

    # -------------------------------------------------------------------------
    # Persistencia de Productos
    # -------------------------------------------------------------------------
    def cargar_productos(self) -> List[Producto]:
        """Carga y deserializa los productos desde productos.json."""
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
                        print(f"[ArchivoServicio] Registro de producto omitido por formato inválido: {e}")
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
        """Serializa y persiste la colección de productos en productos.json."""
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

    # -------------------------------------------------------------------------
    # Persistencia de Usuarios
    # -------------------------------------------------------------------------
    def cargar_usuarios(self) -> List[Usuario]:
        """Carga y deserializa los usuarios desde usuarios.json."""
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
                        print(f"[ArchivoServicio] Registro de usuario omitido: {e}")
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
        """Serializa y persiste la colección de usuarios en usuarios.json."""
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

    # -------------------------------------------------------------------------
    # Persistencia de Ventas (Semana 15)
    # -------------------------------------------------------------------------
    def cargar_ventas(self) -> List[Venta]:
        """
        Carga y deserializa las ventas desde ventas.json.
        Controla excepciones y descarta registros corruptos.
        """
        ventas: List[Venta] = []
        if not self.ruta_ventas or not os.path.exists(self.ruta_ventas):
            return ventas

        try:
            with open(self.ruta_ventas, "r", encoding="utf-8") as f:
                datos = json.load(f)
                items = datos if isinstance(datos, list) else list(datos.values())

                for item in items:
                    try:
                        venta = Venta.desde_diccionario(item)
                        ventas.append(venta)
                    except (KeyError, ValueError) as e:
                        print(f"[ArchivoServicio] Registro de venta omitido: {e}")
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as e:
            print(f"[ArchivoServicio] Error de formato JSON en ventas: {e}")
        except PermissionError as e:
            print(f"[ArchivoServicio] Permiso denegado al leer ventas: {e}")
        except Exception as e:
            print(f"[ArchivoServicio] Error inesperado al cargar ventas: {e}")

        return ventas

    def guardar_ventas(self, ventas: List[Venta]) -> bool:
        """
        Serializa y persiste la colección de transacciones en ventas.json.
        Retorna True si la persistencia fue exitosa.
        """
        if not self.ruta_ventas:
            return False

        try:
            datos = [v.a_diccionario() for v in ventas]
            with open(self.ruta_ventas, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            return True
        except PermissionError as e:
            print(f"[ArchivoServicio] Permiso denegado al escribir ventas: {e}")
            return False
        except Exception as e:
            print(f"[ArchivoServicio] Error al guardar ventas: {e}")
            return False
