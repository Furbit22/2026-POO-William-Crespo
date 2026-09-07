from typing import List, Optional, Tuple
from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio

class RestauranteServicio:
    """
    Servicio central de lógica de negocio para el restaurante.
    Gestiona las colecciones en memoria de productos y usuarios,
    provee métodos para la consulta e inspección de datos por parte de la UI,
    y encapsula la validación de acceso simulada según las directrices pedagógicas.
    """
    def __init__(
        self,
        archivo_servicio: Optional[ArchivoServicio] = None,
        productos: Optional[List[Producto]] = None,
        usuarios: Optional[List[Usuario]] = None
    ) -> None:
        self.archivo_servicio: Optional[ArchivoServicio] = archivo_servicio

        # Cargar productos desde archivo o lista provista
        if productos is not None:
            self._productos: List[Producto] = list(productos)
        elif self.archivo_servicio is not None:
            self._productos: List[Producto] = self.archivo_servicio.cargar_productos()
        else:
            self._productos: List[Producto] = []

        # Cargar usuarios desde archivo o lista provista
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
        Retorna una tupla: (exito: bool, mensaje: str, usuario: Optional[Usuario]).
        
        Reglas pedagógicas:
        - Los campos no deben estar vacíos.
        - Soporta acceso administrativo ('admin' con contraseñas comunes).
        - Soporta acceso para cualquier usuario registrado en 'usuarios.json'
          (usando identificación, correo o nombre, y contraseñas pedagógicas como '1234' o su ID).
        """
        user_clean = usuario_input.strip()
        pass_clean = contrasenia_input.strip()

        if not user_clean or not pass_clean:
            return False, "Por favor complete todos los campos requeridos.", None

        # 1. Acceso de Administrador: admin / 1234
        if user_clean.lower() in ("admin", "administrador"):
            if pass_clean == "1234":
                admin_user = Usuario("ADMIN", "Administrador del Sistema", "admin@restaurante.com")
                return True, "¡Acceso concedido como Administrador!", admin_user
            return False, "Contraseña incorrecta. La contraseña es 1234.", None

        # 2. Búsqueda entre usuarios registrados (con contraseña 1234)
        usuario_encontrado: Optional[Usuario] = None
        for u in self._usuarios:
            if (u.identificacion == user_clean or 
                u.correo.lower() == user_clean.lower() or 
                u.nombre.lower() == user_clean.lower()):
                usuario_encontrado = u
                break

        if usuario_encontrado:
            if pass_clean == "1234":
                return True, f"¡Bienvenido/a, {usuario_encontrado.nombre}!", usuario_encontrado
            return False, "Contraseña incorrecta. La contraseña es 1234.", None

        return False, "El usuario ingresado no existe. Use 'admin' o un ID registrado.", None

    # -------------------------------------------------------------------------
    # Operaciones de Consulta de Productos
    # -------------------------------------------------------------------------
    def listar_productos(self) -> List[Producto]:
        """Retorna la lista completa de productos registrados."""
        return list(self._productos)

    def contar_productos(self) -> int:
        """Retorna la cantidad total de tipos de productos."""
        return len(self._productos)

    def obtener_stock_total(self) -> int:
        """Calcula el total acumulado de unidades en stock."""
        return sum(p.stock for p in self._productos)

    def buscar_productos(self, criterio: str) -> List[Producto]:
        """
        Filtra productos cuyo código, nombre o categoría coincida con el criterio.
        """
        if not criterio or not criterio.strip():
            return self.listar_productos()

        termino = criterio.strip().lower()
        return [
            p for p in self._productos
            if termino in p.codigo.lower() or termino in p.nombre.lower() or termino in p.categoria.lower()
        ]

    def buscar_producto_por_codigo(self, codigo: str) -> Optional[Producto]:
        """Busca y retorna un producto específico por su código único."""
        codigo_limpio = codigo.strip().upper()
        for p in self._productos:
            if p.codigo.upper() == codigo_limpio:
                return p
        return None

    # -------------------------------------------------------------------------
    # Operaciones de Consulta de Usuarios
    # -------------------------------------------------------------------------
    def listar_usuarios(self) -> List[Usuario]:
        """Retorna la lista completa de usuarios registrados."""
        return list(self._usuarios)

    def contar_usuarios(self) -> int:
        """Retorna la cantidad total de usuarios registrados."""
        return len(self._usuarios)

    def buscar_usuarios(self, criterio: str) -> List[Usuario]:
        """
        Filtra usuarios cuya identificación, nombre o correo coincida con el criterio.
        """
        if not criterio or not criterio.strip():
            return self.listar_usuarios()

        termino = criterio.strip().lower()
        return [
            u for u in self._usuarios
            if termino in u.identificacion.lower() or termino in u.nombre.lower() or termino in u.correo.lower()
        ]

    def buscar_usuario_por_id(self, identificacion: str) -> Optional[Usuario]:
        """Busca y retorna un usuario por su número de identificación."""
        ident_limpia = identificacion.strip()
        for u in self._usuarios:
            if u.identificacion == ident_limpia:
                return u
        return None

    # -------------------------------------------------------------------------
    # Sincronización y Recarga
    # -------------------------------------------------------------------------
    def recargar_datos(self) -> None:
        """Recarga los datos desde los archivos JSON si el servicio está configurado."""
        if self.archivo_servicio:
            self._productos = self.archivo_servicio.cargar_productos()
            self._usuarios = self.archivo_servicio.cargar_usuarios()
