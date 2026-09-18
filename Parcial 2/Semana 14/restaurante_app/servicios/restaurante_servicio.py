from typing import List, Optional, Tuple, Any
from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio

class RestauranteServicio:
    """
    Servicio central de lógica de negocio para restaurante_app.
    Encapsula las reglas del dominio, la validación pedagógica de acceso,
    y las operaciones de gestión (CRUD) sobre las colecciones en memoria de
    productos y usuarios, asegurando la persistencia a través de ArchivoServicio.
    """
    def __init__(
        self,
        archivo_servicio: Optional[ArchivoServicio] = None,
        productos: Optional[List[Producto]] = None,
        usuarios: Optional[List[Usuario]] = None
    ) -> None:
        self.archivo_servicio: Optional[ArchivoServicio] = archivo_servicio

        # Cargar productos desde archivo o lista en memoria
        if productos is not None:
            self._productos: List[Producto] = list(productos)
        elif self.archivo_servicio is not None:
            self._productos: List[Producto] = self.archivo_servicio.cargar_productos()
        else:
            self._productos: List[Producto] = []

        # Cargar usuarios desde archivo o lista en memoria
        if usuarios is not None:
            self._usuarios: List[Usuario] = list(usuarios)
        elif self.archivo_servicio is not None:
            self._usuarios: List[Usuario] = self.archivo_servicio.cargar_usuarios()
        else:
            self._usuarios: List[Usuario] = []

    # -------------------------------------------------------------------------
    # Validación y Simulación de Acceso (Login)
    # -------------------------------------------------------------------------
    def validar_acceso(self, usuario_input: str, contrasenia_input: str) -> Tuple[bool, str, Optional[Usuario]]:
        """
        Valida las credenciales de acceso simuladas.
        Retorna (exito: bool, mensaje: str, usuario: Optional[Usuario]).
        
        Reglas pedagógicas:
        - Campos obligatorios no vacíos.
        - Acceso administrativo ('admin' con '1234').
        - Acceso para usuarios registrados en 'usuarios.json' (por cédula, nombre o correo, clave '1234' o ID).
        """
        user_clean = usuario_input.strip() if usuario_input else ""
        pass_clean = contrasenia_input.strip() if contrasenia_input else ""

        if not user_clean or not pass_clean:
            return False, "Por favor complete todos los campos requeridos.", None

        # 1. Acceso Administrador
        if user_clean.lower() in ("admin", "administrador"):
            if pass_clean == "1234":
                admin_user = Usuario("ADMIN", "Administrador del Sistema", "admin@restaurante.com")
                return True, "¡Acceso concedido como Administrador!", admin_user
            return False, "Contraseña incorrecta. La contraseña es 1234.", None

        # 2. Acceso para usuarios registrados
        usuario_encontrado: Optional[Usuario] = None
        for u in self._usuarios:
            if (u.identificacion == user_clean or 
                u.correo.lower() == user_clean.lower() or 
                u.nombre.lower() == user_clean.lower()):
                usuario_encontrado = u
                break

        if usuario_encontrado:
            if pass_clean in ("1234", usuario_encontrado.identificacion):
                return True, f"¡Bienvenido/a, {usuario_encontrado.nombre}!", usuario_encontrado
            return False, "Contraseña incorrecta. La contraseña es 1234.", None

        return False, "El usuario ingresado no existe en el registro.", None

    # -------------------------------------------------------------------------
    # Operaciones CRUD sobre Productos
    # -------------------------------------------------------------------------
    def registrar_producto(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: Any,
        stock: Any
    ) -> Tuple[bool, str, Optional[Producto]]:
        """
        Registra un nuevo producto en el restaurante.
        Valida unicidad de código e integridad de los datos numéricos y de texto.
        Persiste los cambios inmediatamente a través de ArchivoServicio.
        """
        if not codigo or not str(codigo).strip():
            return False, "El código del producto es obligatorio.", None

        cod_limpio = str(codigo).strip().upper()

        if self.consultar_producto(cod_limpio) is not None:
            return False, f"Ya existe un producto registrado con el código '{cod_limpio}'.", None

        try:
            nuevo_producto = Producto(
                codigo=cod_limpio,
                nombre=str(nombre),
                categoria=str(categoria),
                precio=precio,
                stock=stock
            )
        except ValueError as e:
            return False, str(e), None

        self._productos.append(nuevo_producto)
        self._persistir_productos()
        return True, f"Producto '{nuevo_producto.nombre}' ({nuevo_producto.codigo}) registrado con éxito.", nuevo_producto

    def consultar_producto(self, codigo: str) -> Optional[Producto]:
        """
        Busca y retorna un producto a partir de su código único.
        Retorna None si no existe.
        """
        if not codigo or not str(codigo).strip():
            return None

        cod_limpio = str(codigo).strip().upper()
        for p in self._productos:
            if p.codigo.upper() == cod_limpio:
                return p
        return None

    def buscar_producto_por_codigo(self, codigo: str) -> Optional[Producto]:
        """Alias para consultar_producto para interoperabilidad con semanas previas."""
        return self.consultar_producto(codigo)

    def actualizar_producto(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: Any,
        stock: Any
    ) -> Tuple[bool, str, Optional[Producto]]:
        """
        Actualiza los atributos de un producto existente identificado por su código.
        Valida que el producto exista y que los nuevos datos cumplan las reglas del dominio.
        Persiste los cambios inmediatamente.
        """
        if not codigo or not str(codigo).strip():
            return False, "Debe ingresar o seleccionar el código del producto a actualizar.", None

        producto = self.consultar_producto(codigo)
        if producto is None:
            return False, f"No se encontró ningún producto con el código '{codigo.strip().upper()}'.", None

        try:
            producto.actualizar_datos(nombre=str(nombre), categoria=str(categoria), precio=precio, stock=stock)
        except ValueError as e:
            return False, str(e), None

        self._persistir_productos()
        return True, f"Producto '{producto.codigo}' actualizado exitosamente.", producto

    def eliminar_producto(self, codigo: str) -> Tuple[bool, str]:
        """
        Elimina un producto del catálogo por su código.
        Actualiza la colección en memoria y persiste los cambios en disco.
        """
        if not codigo or not str(codigo).strip():
            return False, "Debe indicar el código del producto que desea eliminar."

        producto = self.consultar_producto(codigo)
        if producto is None:
            return False, f"No se encontró ningún producto con el código '{codigo.strip().upper()}'."

        self._productos.remove(producto)
        self._persistir_productos()
        return True, f"Producto '{producto.codigo}' ({producto.nombre}) eliminado exitosamente."

    def _persistir_productos(self) -> bool:
        """Helper interno para persistir la colección actual de productos en disco."""
        if self.archivo_servicio is not None:
            return self.archivo_servicio.guardar_productos(self._productos)
        return True

    # -------------------------------------------------------------------------
    # Consultas y Filtros de Productos
    # -------------------------------------------------------------------------
    def listar_productos(self) -> List[Producto]:
        """Retorna una copia de la lista de productos registrados."""
        return list(self._productos)

    def contar_productos(self) -> int:
        """Retorna la cantidad de tipos de productos disponibles."""
        return len(self._productos)

    def obtener_stock_total(self) -> int:
        """Calcula el número total de unidades de productos en existencias."""
        return sum(p.stock for p in self._productos)

    def buscar_productos(self, criterio: str) -> List[Producto]:
        """
        Filtra productos cuyo código, nombre o categoría coincidan con el criterio dado.
        """
        if not criterio or not criterio.strip():
            return self.listar_productos()

        termino = criterio.strip().lower()
        return [
            p for p in self._productos
            if termino in p.codigo.lower() or termino in p.nombre.lower() or termino in p.categoria.lower()
        ]

    # -------------------------------------------------------------------------
    # Operaciones de Consulta de Usuarios
    # -------------------------------------------------------------------------
    def listar_usuarios(self) -> List[Usuario]:
        """Retorna la lista de usuarios registrados."""
        return list(self._usuarios)

    def contar_usuarios(self) -> int:
        """Retorna la cantidad total de usuarios registrados."""
        return len(self._usuarios)

    def buscar_usuarios(self, criterio: str) -> List[Usuario]:
        """
        Filtra usuarios por coincidencia en identificación, nombre o correo.
        """
        if not criterio or not criterio.strip():
            return self.listar_usuarios()

        termino = criterio.strip().lower()
        return [
            u for u in self._usuarios
            if termino in u.identificacion.lower() or termino in u.nombre.lower() or termino in u.correo.lower()
        ]

    def buscar_usuario_por_id(self, identificacion: str) -> Optional[Usuario]:
        """Busca y retorna un usuario por su número de cédula/identificación."""
        if not identificacion:
            return None
        ident_limpia = str(identificacion).strip()
        for u in self._usuarios:
            if u.identificacion == ident_limpia:
                return u
        return None

    # -------------------------------------------------------------------------
    # Recarga de Datos
    # -------------------------------------------------------------------------
    def recargar_datos(self) -> None:
        """Recarga las colecciones en memoria desde el archivo de persistencia."""
        if self.archivo_servicio:
            self._productos = self.archivo_servicio.cargar_productos()
            self._usuarios = self.archivo_servicio.cargar_usuarios()
