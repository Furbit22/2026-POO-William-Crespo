from datetime import datetime
from typing import List, Optional, Tuple, Any, Dict
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio

class RestauranteServicio:
    """
    Servicio central de lógica de negocio para restaurante_app.
    Encapsula las reglas del dominio, la validación pedagógica de acceso,
    las operaciones CRUD sobre productos, la consulta de usuarios y la gestión
    transaccional de ventas (Semana 15), asegurando la persistencia mediante ArchivoServicio.
    """
    def __init__(
        self,
        archivo_servicio: Optional[ArchivoServicio] = None,
        productos: Optional[List[Producto]] = None,
        usuarios: Optional[List[Usuario]] = None,
        ventas: Optional[List[Venta]] = None
    ) -> None:
        self.archivo_servicio: Optional[ArchivoServicio] = archivo_servicio

        # 1. Cargar productos desde archivo o lista en memoria
        if productos is not None:
            self._productos: List[Producto] = list(productos)
        elif self.archivo_servicio is not None:
            self._productos: List[Producto] = self.archivo_servicio.cargar_productos()
        else:
            self._productos: List[Producto] = []

        # 2. Cargar usuarios desde archivo o lista en memoria
        if usuarios is not None:
            self._usuarios: List[Usuario] = list(usuarios)
        elif self.archivo_servicio is not None:
            self._usuarios: List[Usuario] = self.archivo_servicio.cargar_usuarios()
        else:
            self._usuarios: List[Usuario] = []

        # 3. Cargar ventas desde archivo o lista en memoria (Semana 15)
        if ventas is not None:
            self._ventas: List[Venta] = list(ventas)
        elif self.archivo_servicio is not None:
            self._ventas: List[Venta] = self.archivo_servicio.cargar_ventas()
        else:
            self._ventas: List[Venta] = []

    # -------------------------------------------------------------------------
    # Validación y Simulación de Acceso (Login)
    # -------------------------------------------------------------------------
    def validar_acceso(self, usuario_input: str, contrasenia_input: str) -> Tuple[bool, str, Optional[Usuario]]:
        """
        Valida las credenciales de acceso simuladas.
        Retorna (exito: bool, mensaje: str, usuario: Optional[Usuario]).
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
        """Busca y retorna un producto a partir de su código único."""
        if not codigo or not str(codigo).strip():
            return None

        cod_limpio = str(codigo).strip().upper()
        for p in self._productos:
            if p.codigo.upper() == cod_limpio:
                return p
        return None

    def buscar_producto_por_codigo(self, codigo: str) -> Optional[Producto]:
        """Alias de consultar_producto para consistencia histórica."""
        return self.consultar_producto(codigo)

    def actualizar_producto(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: Any,
        stock: Any
    ) -> Tuple[bool, str, Optional[Producto]]:
        """Actualiza los atributos de un producto existente identificado por su código."""
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
        """Elimina un producto del catálogo por su código."""
        if not codigo or not str(codigo).strip():
            return False, "Debe indicar el código del producto que desea eliminar."

        producto = self.consultar_producto(codigo)
        if producto is None:
            return False, f"No se encontró ningún producto con el código '{codigo.strip().upper()}'."

        self._productos.remove(producto)
        self._persistir_productos()
        return True, f"Producto '{producto.codigo}' ({producto.nombre}) eliminado exitosamente."

    def _persistir_productos(self) -> bool:
        """Persiste la colección actual de productos en productos.json."""
        if self.archivo_servicio is not None:
            return self.archivo_servicio.guardar_productos(self._productos)
        return True

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
        """Filtra productos cuyo código, nombre o categoría coincidan con el criterio dado."""
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
        """Filtra usuarios por coincidencia en identificación, nombre o correo."""
        if not criterio or not criterio.strip():
            return self.listar_usuarios()

        termino = criterio.strip().lower()
        return [
            u for u in self._usuarios
            if termino in u.identificacion.lower() or termino in u.nombre.lower() or termino in u.correo.lower()
        ]

    def buscar_usuario_por_id(self, identificacion: str) -> Optional[Usuario]:
        """Busca y retorna un usuario por su número de identificación."""
        if not identificacion:
            return None
        ident_limpia = str(identificacion).strip()
        for u in self._usuarios:
            if u.identificacion == ident_limpia:
                return u
        return None

    # -------------------------------------------------------------------------
    # Gestión de Ventas (Semana 15 - Conceptos de Eventos)
    # -------------------------------------------------------------------------
    def registrar_venta(
        self,
        usuario_id: str,
        producto_codigo: str
    ) -> Tuple[bool, str, Optional[Venta]]:
        """
        Registra una venta comercial en restaurante_app.
        Relaciona a un usuario registrado con un producto disponible en el menú.
        
        Validaciones de negocio:
        - usuario_id y producto_codigo no deben estar vacíos.
        - El usuario debe existir en el registro del restaurante.
        - El producto debe existir en el catálogo.
        - Debe haber existencias suficientes en stock (stock > 0).
        
        Efectos colaterales:
        - Descuenta 1 unidad de stock del producto.
        - Genera un código correlativo único (ej. V001, V002).
        - Estampa la fecha y hora de la operación.
        - Persiste de inmediato en caliente tanto 'productos.json' como 'ventas.json'.
        """
        if not usuario_id or not str(usuario_id).strip():
            return False, "Debe seleccionar un usuario válido para la venta.", None

        if not producto_codigo or not str(producto_codigo).strip():
            return False, "Debe seleccionar un producto válido para la venta.", None

        uid_limpio = str(usuario_id).strip()
        pcod_limpio = str(producto_codigo).strip().upper()

        # Validar existencia de usuario
        usuario = self.buscar_usuario_por_id(uid_limpio)
        if usuario is None:
            return False, f"El usuario con ID '{uid_limpio}' no está registrado en el sistema.", None

        # Validar existencia de producto
        producto = self.consultar_producto(pcod_limpio)
        if producto is None:
            return False, f"El producto con código '{pcod_limpio}' no existe en el catálogo.", None

        # Validar existencias en stock
        if producto.stock <= 0:
            return False, f"No hay existencias disponibles para '{producto.nombre}' (Stock: 0).", None

        # Descontar stock
        producto.stock -= 1

        # Generar identificador correlativo para la venta
        nuevo_id = self._generar_siguiente_id_venta()
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            nueva_venta = Venta(
                id_venta=nuevo_id,
                usuario_id=usuario.identificacion,
                producto_codigo=producto.codigo,
                fecha=fecha_actual,
                total=producto.precio
            )
        except ValueError as e:
            # Revertir stock si ocurre error de validación
            producto.stock += 1
            return False, str(e), None

        self._ventas.append(nueva_venta)

        # Persistencia en caliente de ambas colecciones
        self._persistir_productos()
        self._persistir_ventas()

        mensaje_exito = (
            f"Venta [{nueva_venta.id_venta}] registrada exitosamente: "
            f"'{producto.nombre}' para '{usuario.nombre}' (${nueva_venta.total:.2f})."
        )
        return True, mensaje_exito, nueva_venta

    def _generar_siguiente_id_venta(self) -> str:
        """Genera el siguiente identificador correlativo secuencial para una venta."""
        numeros = []
        for v in self._ventas:
            # Intentar extraer el número de V001, V002, etc.
            if v.id_venta.startswith("V"):
                try:
                    num = int(v.id_venta[1:])
                    numeros.append(num)
                except ValueError:
                    pass
        siguiente = max(numeros) + 1 if numeros else 1
        return f"V{siguiente:03d}"

    def _persistir_ventas(self) -> bool:
        """Persiste la colección actual de ventas en ventas.json."""
        if self.archivo_servicio is not None:
            return self.archivo_servicio.guardar_ventas(self._ventas)
        return True

    def listar_ventas(self) -> List[Venta]:
        """Retorna una copia de la lista de ventas registradas."""
        return list(self._ventas)

    def contar_ventas(self) -> int:
        """Retorna la cantidad total de transacciones de ventas efectuadas."""
        return len(self._ventas)

    def calcular_total_ventas(self) -> float:
        """Calcula el total económico acumulado por ventas ($)."""
        return sum(v.total for v in self._ventas)

    def obtener_detalle_venta(self, venta: Venta) -> Dict[str, Any]:
        """
        Retorna la información completa de una venta enriquecida con los nombres
        reales del usuario y del producto.
        """
        usuario = self.buscar_usuario_por_id(venta.usuario_id)
        producto = self.consultar_producto(venta.producto_codigo)

        nombre_usuario = usuario.nombre if usuario else f"Usuario ({venta.usuario_id})"
        nombre_producto = producto.nombre if producto else f"Producto ({venta.producto_codigo})"

        return {
            "id_venta": venta.id_venta,
            "fecha": venta.fecha,
            "usuario_id": venta.usuario_id,
            "usuario_nombre": nombre_usuario,
            "producto_codigo": venta.producto_codigo,
            "producto_nombre": nombre_producto,
            "total": venta.total
        }

    # -------------------------------------------------------------------------
    # Recarga Global de Datos
    # -------------------------------------------------------------------------
    def recargar_datos(self) -> None:
        """Recarga las colecciones en memoria desde el almacenamiento JSON."""
        if self.archivo_servicio:
            self._productos = self.archivo_servicio.cargar_productos()
            self._usuarios = self.archivo_servicio.cargar_usuarios()
            self._ventas = self.archivo_servicio.cargar_ventas()
