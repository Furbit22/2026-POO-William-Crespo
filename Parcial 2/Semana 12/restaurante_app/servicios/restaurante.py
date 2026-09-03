from typing import List, Optional, Set, Dict
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta

class Restaurante:
    """
    Servicio principal que gestiona la lógica de negocio del restaurante.
    
    Evolución Semana 12 - Optimización de Colecciones:
    - Conserva las listas principales (_productos, _usuarios, _ventas) para mantener
      el orden de registro, iteraciones secuenciales y serialización JSON.
    - Incorpora índices en memoria mediante diccionarios (dict) para permitir búsquedas
      y validaciones en tiempo constante O(1) por clave primaria.
    - Implementa un índice de ventas agrupadas por usuario para evitar recorrer toda la
      colección de ventas O(m) al consultar el historial de un usuario específico.
    - Emplea conjuntos (set) para optimizar validaciones de unicidad y pertenencia de
      categorías y correos electrónicos.
    - Provee sincronización continua en todas las operaciones de modificación y
      reconstrucción de índices tras la carga de datos persistidos.
    """

    def __init__(
        self,
        productos_iniciales: Optional[List[Producto]] = None,
        usuarios_iniciales: Optional[List[Usuario]] = None,
        ventas_iniciales: Optional[List[Venta]] = None
    ) -> None:
        # Colecciones principales (Listas: para orden y persistencia)
        self._productos: List[Producto] = productos_iniciales if productos_iniciales is not None else []
        self._usuarios: List[Usuario] = usuarios_iniciales if usuarios_iniciales is not None else []
        self._ventas: List[Venta] = ventas_iniciales if ventas_iniciales is not None else []

        # Estructuras auxiliares e índices en memoria (dict y set)
        self._indice_productos: Dict[str, Producto] = {}
        self._indice_usuarios: Dict[str, Usuario] = {}
        self._indice_ventas_por_usuario: Dict[str, List[Venta]] = {}
        self._categorias_unicas: Set[str] = set()
        self._correos_registrados: Set[str] = set()

        # Reconstruir los índices a partir de los datos iniciales recuperados desde JSON
        self._reconstruir_indices()

    def _reconstruir_indices(self) -> None:
        """
        Reconstruye todos los índices y conjuntos auxiliares en memoria
        a partir de las listas principales.
        Garantiza la coherencia de datos al iniciar la aplicación.
        """
        self._indice_productos.clear()
        self._categorias_unicas.clear()
        for prod in self._productos:
            self._indice_productos[prod.codigo] = prod
            if prod.categoria:
                self._categorias_unicas.add(prod.categoria)

        self._indice_usuarios.clear()
        self._correos_registrados.clear()
        self._indice_ventas_por_usuario.clear()

        for usr in self._usuarios:
            self._indice_usuarios[usr.identificacion] = usr
            if usr.correo:
                self._correos_registrados.add(usr.correo.strip().lower())
            self._indice_ventas_por_usuario[usr.identificacion] = []

        for vnt in self._ventas:
            # Agrupar las ventas directamente en la lista del usuario correspondiente
            if vnt.usuario_id in self._indice_ventas_por_usuario:
                self._indice_ventas_por_usuario[vnt.usuario_id].append(vnt)
            else:
                self._indice_ventas_por_usuario[vnt.usuario_id] = [vnt]

    def _sincronizar_categorias(self) -> None:
        """Actualiza el conjunto de categorías únicas a partir de los productos actuales."""
        self._categorias_unicas = {prod.categoria for prod in self._productos if prod.categoria}

    # =========================================================================
    # GESTIÓN DE PRODUCTOS (Optimizada con _indice_productos y _categorias_unicas)
    # =========================================================================

    def registrar_producto(self, producto: Producto) -> bool:
        """
        Registra un nuevo producto en el sistema.
        Optimización: Verificación de duplicados en O(1) usando el índice de productos.
        """
        if producto.codigo in self._indice_productos:
            return False

        # Inserción en lista principal (para persistencia) y sincronización de estructuras auxiliares
        self._productos.append(producto)
        self._indice_productos[producto.codigo] = producto
        if producto.categoria:
            self._categorias_unicas.add(producto.categoria)
        return True

    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        """
        Busca un producto por su código único.
        Optimización: Acceso directo en O(1) a través del índice hash en lugar de recorrido lineal O(n).
        """
        return self._indice_productos.get(codigo.strip())

    def actualizar_producto(self, codigo: str, nombre: str, categoria: str, precio: float, stock: int) -> bool:
        """
        Actualiza los datos de un producto existente.
        Optimización: Localización del producto en O(1) mediante el índice.
        """
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False

        # Validar antes de asignar para cumplir con las reglas del modelo
        temp = Producto(codigo, nombre, categoria, precio, stock)
        
        categoria_previa = producto.categoria
        producto.nombre = temp.nombre
        producto.categoria = temp.categoria
        producto.precio = temp.precio
        producto.stock = temp.stock

        # Si la categoría fue modificada, sincronizar el conjunto de categorías únicas
        if categoria_previa != producto.categoria:
            self._sincronizar_categorias()

        return True

    def eliminar_producto(self, codigo: str) -> bool:
        """
        Elimina un producto del sistema.
        Optimización: Búsqueda previa en O(1) y sincronización de lista, índice y categorías.
        """
        codigo_limpio = codigo.strip()
        producto = self.buscar_producto(codigo_limpio)
        if producto is None:
            return False

        self._productos.remove(producto)
        del self._indice_productos[codigo_limpio]
        self._sincronizar_categorias()
        return True

    def obtener_productos(self) -> List[Producto]:
        """Retorna la lista principal de productos (utilizada para listar y persistir en JSON)."""
        return self._productos

    def obtener_categorias_unicas(self) -> Set[str]:
        """
        Retorna el conjunto de categorías de productos registradas.
        Optimización: Retorno directo en O(1) del conjunto auxiliar en lugar de reconstruir en O(n).
        """
        return set(self._categorias_unicas)

    # =========================================================================
    # GESTIÓN DE USUARIOS (Optimizada con _indice_usuarios y _correos_registrados)
    # =========================================================================

    def registrar_usuario(self, usuario: Usuario) -> bool:
        """
        Registra un nuevo usuario en el sistema.
        Optimización: Validación de ID y unicidad de correo en O(1) usando dict y set.
        """
        id_limpia = usuario.identificacion.strip()
        correo_normalizado = usuario.correo.strip().lower()

        if id_limpia in self._indice_usuarios or correo_normalizado in self._correos_registrados:
            return False

        self._usuarios.append(usuario)
        self._indice_usuarios[id_limpia] = usuario
        self._correos_registrados.add(correo_normalizado)
        if id_limpia not in self._indice_ventas_por_usuario:
            self._indice_ventas_por_usuario[id_limpia] = []
        return True

    def buscar_usuario(self, identificacion: str) -> Optional[Usuario]:
        """
        Busca un usuario por su identificación.
        Optimización: Búsqueda directa en O(1) usando el diccionario auxiliar.
        """
        return self._indice_usuarios.get(identificacion.strip())

    def obtener_usuarios(self) -> List[Usuario]:
        """Retorna la lista principal de usuarios (utilizada para listar y persistir en JSON)."""
        return self._usuarios

    def existe_correo(self, correo: str) -> bool:
        """
        Verifica en O(1) si un correo electrónico ya está registrado.
        Utiliza el conjunto _correos_registrados.
        """
        return correo.strip().lower() in self._correos_registrados

    # =========================================================================
    # GESTIÓN DE VENTAS (Optimizada con _indice_ventas_por_usuario)
    # =========================================================================

    def vender_producto(self, codigo_producto: str, identificacion_usuario: str, cantidad: int) -> bool:
        """
        Registra una venta y actualiza el stock del producto.
        Optimización:
        - Búsqueda de usuario y producto en O(1) usando sus respectivos índices.
        - Inserción y sincronización en O(1) tanto en la lista principal como en el índice por usuario.
        """
        usuario = self.buscar_usuario(identificacion_usuario)
        producto = self.buscar_producto(codigo_producto)

        if usuario is None or producto is None:
            return False

        try:
            cantidad_int = int(cantidad)
        except (TypeError, ValueError):
            raise ValueError("La cantidad solicitada debe ser un número entero válido.")

        if cantidad_int <= 0:
            raise ValueError("La cantidad a vender debe ser mayor que cero.")

        if producto.stock < cantidad_int:
            raise ValueError(f"Stock insuficiente para {producto.nombre}. Stock disponible: {producto.stock}, solicitado: {cantidad_int}")

        # Crear y registrar la venta
        venta = Venta(usuario.identificacion, producto.codigo, cantidad_int)
        
        # Descontar stock del objeto Producto
        producto.vender(cantidad_int)

        # Sincronizar lista principal de ventas (para persistencia)
        self._ventas.append(venta)

        # Sincronizar índice auxiliar de ventas por usuario en O(1)
        if usuario.identificacion not in self._indice_ventas_por_usuario:
            self._indice_ventas_por_usuario[usuario.identificacion] = []
        self._indice_ventas_por_usuario[usuario.identificacion].append(venta)

        return True

    def consultar_ventas_usuario(self, identificacion_usuario: str) -> List[Venta]:
        """
        Consulta las ventas realizadas por un usuario específico.
        Optimización: Retorna directamente la sublista indexada en O(1) tiempo de búsqueda,
        evitando recorrer toda la lista de ventas del restaurante (O(m)).
        """
        id_limpia = identificacion_usuario.strip()
        # Retornar una copia superficial de la lista para preservar encapsulación
        return list(self._indice_ventas_por_usuario.get(id_limpia, []))

    def obtener_ventas(self) -> List[Venta]:
        """Retorna la lista principal de ventas (historial general y persistencia)."""
        return self._ventas
