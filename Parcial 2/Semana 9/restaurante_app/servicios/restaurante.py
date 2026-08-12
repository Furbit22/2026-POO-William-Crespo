import os
import json
from typing import List, Optional, Set, Dict, Any
from modelos.producto import Producto
from modelos.usuario import Usuario

class Restaurante:
    def __init__(self) -> None:
        # Definir la ruta de la carpeta data
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.productos_path = os.path.join(self.data_dir, "productos.json")
        self.usuarios_path = os.path.join(self.data_dir, "usuarios.json")
        
        # Cargar los datos desde los archivos JSON correspondientes
        self._datos: Dict[str, List[Any]] = {
            "productos": self._cargar_productos(),
            "usuarios": self._cargar_usuarios()
        }

    def _cargar_productos(self) -> List[Producto]:
        if not os.path.exists(self.productos_path):
            return []
        try:
            with open(self.productos_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                productos = []
                for item in data.values():
                    productos.append(Producto(
                        codigo=item["codigo"],
                        nombre=item["nombre"],
                        categoria=item["categoria"],
                        precio=float(item["precio"])
                    ))
                return productos
        except Exception:
            return []

    def _cargar_usuarios(self) -> List[Usuario]:
        if not os.path.exists(self.usuarios_path):
            return []
        try:
            with open(self.usuarios_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                usuarios = []
                for item in data.values():
                    usuarios.append(Usuario(
                        identificacion=item["identificacion"],
                        nombre=item["nombre"],
                        correo=item["correo"]
                    ))
                return usuarios
        except Exception:
            return []

    def _guardar_productos(self) -> None:
        data = {}
        for prod in self._datos["productos"]:
            data[prod.codigo] = {
                "codigo": prod.codigo,
                "nombre": prod.nombre,
                "categoria": prod.categoria,
                "precio": prod.precio
            }
        with open(self.productos_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def _guardar_usuarios(self) -> None:
        data = {}
        for usr in self._datos["usuarios"]:
            data[usr.identificacion] = {
                "identificacion": usr.identificacion,
                "nombre": usr.nombre,
                "correo": usr.correo
            }
        with open(self.usuarios_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def registrar_producto(self, producto: Producto) -> bool:
        productos: List[Producto] = self._datos["productos"]
        for prod in productos:
            if prod.codigo == producto.codigo:
                return False
        productos.append(producto)
        self._guardar_productos()
        return True

    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        productos: List[Producto] = self._datos["productos"]
        for prod in productos:
            if prod.codigo == codigo:
                return prod
        return None

    def actualizar_producto(self, codigo: str, nombre: str, categoria: str, precio: float) -> bool:
        producto = self.buscar_producto(codigo)
        if producto:
            producto.nombre = nombre
            producto.categoria = categoria
            producto.precio = precio
            self._guardar_productos()
            return True
        return False

    def eliminar_producto(self, codigo: str) -> bool:
        producto = self.buscar_producto(codigo)
        if producto:
            self._datos["productos"].remove(producto)
            self._guardar_productos()
            return True
        return False

    def obtener_productos(self) -> List[Producto]:
        return self._datos["productos"]

    def registrar_usuario(self, usuario: Usuario) -> bool:
        usuarios: List[Usuario] = self._datos["usuarios"]
        for usr in usuarios:
            if usr.identificacion == usuario.identificacion:
                return False
        usuarios.append(usuario)
        self._guardar_usuarios()
        return True

    def obtener_usuarios(self) -> List[Usuario]:
        return self._datos["usuarios"]

    def obtener_categorias_unicas(self) -> Set[str]:
        productos: List[Producto] = self._datos["productos"]
        return {prod.categoria for prod in productos if prod.categoria}

