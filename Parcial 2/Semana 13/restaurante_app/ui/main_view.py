import tkinter as tk
from tkinter import ttk
from typing import Callable, List
from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.restaurante_servicio import RestauranteServicio

class MainView(tk.Frame):
    """
    Panel principal de la aplicación gráfica restaurante_app.
    Permite visualizar los productos y usuarios registrados en el sistema,
    solicitando toda la información a RestauranteServicio (sin tocar archivos JSON),
    y manteniendo identificadas las funcionalidades futuras (como Ventas).
    """
    def __init__(
        self,
        parent: tk.Widget,
        servicio: RestauranteServicio,
        usuario_actual: Usuario,
        on_logout: Callable[[], None]
    ) -> None:
        super().__init__(parent, bg="#f3f4f6")
        self.servicio: RestauranteServicio = servicio
        self.usuario_actual: Usuario = usuario_actual
        self.on_logout: Callable[[], None] = on_logout

        self._configurar_estilos()
        self._crear_interfaz()
        self._cargar_datos_productos()
        self._cargar_datos_usuarios()

    def _configurar_estilos(self) -> None:
        """Configura estilos ttk para las tablas y pestañas."""
        estilo = ttk.Style()
        estilo.theme_use("clam")

        # Configuración del Notebook (pestañas)
        estilo.configure("TNotebook", background="#f3f4f6", borderwidth=0)
        estilo.configure(
            "TNotebook.Tab",
            font=("Helvetica", 10, "bold"),
            padding=[16, 8],
            background="#e5e7eb",
            foreground="#374151"
        )
        estilo.map(
            "TNotebook.Tab",
            background=[("selected", "#2563eb")],
            foreground=[("selected", "#ffffff")]
        )

        # Configuración del Treeview (tablas)
        estilo.configure(
            "Treeview",
            font=("Helvetica", 10),
            rowheight=26,
            background="#ffffff",
            fieldbackground="#ffffff",
            foreground="#1f2937"
        )
        estilo.configure(
            "Treeview.Heading",
            font=("Helvetica", 10, "bold"),
            background="#e5e7eb",
            foreground="#1f2937",
            relief="flat"
        )
        estilo.map("Treeview.Heading", background=[("active", "#d1d5db")])

    def _crear_interfaz(self) -> None:
        """Construye la distribución completa del panel principal."""
        # 1. Barra Superior (Header)
        header = tk.Frame(self, bg="#1e293b", padx=20, pady=12)
        header.pack(fill="x", side="top")

        # Título y logotipo
        info_header = tk.Frame(header, bg="#1e293b")
        info_header.pack(side="left")

        lbl_app = tk.Label(
            info_header,
            text="🍽️ Restaurante App",
            font=("Helvetica", 14, "bold"),
            fg="#ffffff",
            bg="#1e293b"
        )
        lbl_app.pack(anchor="w")

        lbl_sesion = tk.Label(
            info_header,
            text=f"Sesión iniciada: {self.usuario_actual.nombre} ({self.usuario_actual.identificacion})",
            font=("Helvetica", 9),
            fg="#94a3b8",
            bg="#1e293b"
        )
        lbl_sesion.pack(anchor="w")

        # Botón Cerrar Sesión
        btn_logout = tk.Button(
            header,
            text="🚪 Cerrar Sesión",
            font=("Helvetica", 9, "bold"),
            bg="#ef4444",
            fg="#ffffff",
            activebackground="#dc2626",
            activeforeground="#ffffff",
            cursor="hand2",
            relief="flat",
            padx=12,
            pady=6,
            command=self.on_logout
        )
        btn_logout.pack(side="right")

        # 2. Contenedor de Pestañas (Notebook)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=15)

        # Crear las tres pestañas solicitadas
        self._crear_tab_productos()
        self._crear_tab_usuarios()
        self._crear_tab_ventas_pendiente()

        # 3. Barra de Estado Inferior
        footer = tk.Frame(self, bg="#e2e8f0", padx=15, pady=6)
        footer.pack(fill="x", side="bottom")

        lbl_footer = tk.Label(
            footer,
            text="Semana 13 — Conceptos Fundamentales de Interfaces Gráficas | Vista desacoplada conectada a RestauranteServicio",
            font=("Helvetica", 8),
            fg="#64748b",
            bg="#e2e8f0"
        )
        lbl_footer.pack(side="left")

    # =========================================================================
    # PESTAÑA: PRODUCTOS REGISTRADOS
    # =========================================================================
    def _crear_tab_productos(self) -> None:
        """Construye la vista de productos cargados mediante el servicio."""
        tab = tk.Frame(self.notebook, bg="#ffffff", padx=15, pady=15)
        self.notebook.add(tab, text=" 📦 Productos Registrados ")

        # Panel de Resumen y Búsqueda
        top_panel = tk.Frame(tab, bg="#ffffff")
        top_panel.pack(fill="x", pady=(0, 10))

        # Tarjetas de estadísticas
        stats_frame = tk.Frame(top_panel, bg="#f8fafc", bd=1, relief="solid", padx=10, pady=6)
        stats_frame.pack(side="left")

        self.lbl_total_prod = tk.Label(
            stats_frame,
            text=f"Total Productos: {self.servicio.contar_productos()}",
            font=("Helvetica", 9, "bold"),
            fg="#1e40af",
            bg="#f8fafc"
        )
        self.lbl_total_prod.pack(side="left", padx=(0, 15))

        self.lbl_stock_total = tk.Label(
            stats_frame,
            text=f"Stock Total Disponible: {self.servicio.obtener_stock_total()} u.",
            font=("Helvetica", 9, "bold"),
            fg="#047857",
            bg="#f8fafc"
        )
        self.lbl_stock_total.pack(side="left")

        # Barra de búsqueda de productos
        search_frame = tk.Frame(top_panel, bg="#ffffff")
        search_frame.pack(side="right")

        lbl_buscar = tk.Label(search_frame, text="Buscar:", font=("Helvetica", 9, "bold"), bg="#ffffff", fg="#374151")
        lbl_buscar.pack(side="left", padx=(0, 5))

        self.txt_buscar_prod = ttk.Entry(search_frame, width=20, font=("Helvetica", 9))
        self.txt_buscar_prod.pack(side="left", padx=(0, 5))
        self.txt_buscar_prod.bind("<KeyRelease>", lambda e: self._filtrar_productos())

        btn_limpiar = tk.Button(
            search_frame,
            text="Restablecer",
            font=("Helvetica", 8),
            bg="#e5e7eb",
            relief="flat",
            cursor="hand2",
            command=self._restablecer_productos
        )
        btn_limpiar.pack(side="left")

        # Tabla (Treeview) de Productos con Scrollbar
        table_container = tk.Frame(tab, bg="#ffffff")
        table_container.pack(fill="both", expand=True)

        columnas = ("codigo", "nombre", "categoria", "precio", "stock")
        self.tree_prod = ttk.Treeview(table_container, columns=columnas, show="headings", selectmode="browse")

        self.tree_prod.heading("codigo", text="Código")
        self.tree_prod.heading("nombre", text="Nombre del Platillo / Producto")
        self.tree_prod.heading("categoria", text="Categoría")
        self.tree_prod.heading("precio", text="Precio Unitario ($)")
        self.tree_prod.heading("stock", text="Stock Disponible")

        self.tree_prod.column("codigo", width=90, anchor="center")
        self.tree_prod.column("nombre", width=260, anchor="w")
        self.tree_prod.column("categoria", width=140, anchor="center")
        self.tree_prod.column("precio", width=120, anchor="e")
        self.tree_prod.column("stock", width=120, anchor="center")

        scroll_y = ttk.Scrollbar(table_container, orient="vertical", command=self.tree_prod.yview)
        self.tree_prod.configure(yscrollcommand=scroll_y.set)

        self.tree_prod.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

    def _cargar_datos_productos(self, lista: List[Producto] = None) -> None:
        """Puebla el Treeview solicitando la información a RestauranteServicio."""
        for item in self.tree_prod.get_children():
            self.tree_prod.delete(item)

        productos = lista if lista is not None else self.servicio.listar_productos()

        for idx, p in enumerate(productos):
            tag = "par" if idx % 2 == 0 else "impar"
            self.tree_prod.insert(
                "",
                "end",
                values=(p.codigo, p.nombre, p.categoria, f"${p.precio:.2f}", p.stock),
                tags=(tag,)
            )

        self.tree_prod.tag_configure("par", background="#ffffff")
        self.tree_prod.tag_configure("impar", background="#f8fafc")

        self.lbl_total_prod.config(text=f"Total Productos: {self.servicio.contar_productos()}")
        self.lbl_stock_total.config(text=f"Stock Total Disponible: {self.servicio.obtener_stock_total()} u.")

    def _filtrar_productos(self) -> None:
        """Filtra productos en memoria a través del servicio."""
        termino = self.txt_buscar_prod.get()
        filtrados = self.servicio.buscar_productos(termino)
        self._cargar_datos_productos(filtrados)

    def _restablecer_productos(self) -> None:
        """Limpia el campo de búsqueda y recarga todos los productos."""
        self.txt_buscar_prod.delete(0, tk.END)
        self._cargar_datos_productos()

    # =========================================================================
    # PESTAÑA: USUARIOS REGISTRADOS
    # =========================================================================
    def _crear_tab_usuarios(self) -> None:
        """Construye la vista de usuarios cargados mediante el servicio."""
        tab = tk.Frame(self.notebook, bg="#ffffff", padx=15, pady=15)
        self.notebook.add(tab, text=" 👥 Usuarios Registrados ")

        # Panel de Resumen y Búsqueda
        top_panel = tk.Frame(tab, bg="#ffffff")
        top_panel.pack(fill="x", pady=(0, 10))

        stats_frame = tk.Frame(top_panel, bg="#f8fafc", bd=1, relief="solid", padx=10, pady=6)
        stats_frame.pack(side="left")

        self.lbl_total_user = tk.Label(
            stats_frame,
            text=f"Total Usuarios: {self.servicio.contar_usuarios()}",
            font=("Helvetica", 9, "bold"),
            fg="#1e40af",
            bg="#f8fafc"
        )
        self.lbl_total_user.pack(side="left")

        # Búsqueda de usuarios
        search_frame = tk.Frame(top_panel, bg="#ffffff")
        search_frame.pack(side="right")

        lbl_buscar = tk.Label(search_frame, text="Buscar:", font=("Helvetica", 9, "bold"), bg="#ffffff", fg="#374151")
        lbl_buscar.pack(side="left", padx=(0, 5))

        self.txt_buscar_user = ttk.Entry(search_frame, width=20, font=("Helvetica", 9))
        self.txt_buscar_user.pack(side="left", padx=(0, 5))
        self.txt_buscar_user.bind("<KeyRelease>", lambda e: self._filtrar_usuarios())

        btn_limpiar = tk.Button(
            search_frame,
            text="Restablecer",
            font=("Helvetica", 8),
            bg="#e5e7eb",
            relief="flat",
            cursor="hand2",
            command=self._restablecer_usuarios
        )
        btn_limpiar.pack(side="left")

        # Tabla (Treeview) de Usuarios con Scrollbar
        table_container = tk.Frame(tab, bg="#ffffff")
        table_container.pack(fill="both", expand=True)

        columnas = ("identificacion", "nombre", "correo")
        self.tree_user = ttk.Treeview(table_container, columns=columnas, show="headings", selectmode="browse")

        self.tree_user.heading("identificacion", text="Identificación / Cédula")
        self.tree_user.heading("nombre", text="Nombre Completo")
        self.tree_user.heading("correo", text="Correo Electrónico")

        self.tree_user.column("identificacion", width=140, anchor="center")
        self.tree_user.column("nombre", width=250, anchor="w")
        self.tree_user.column("correo", width=250, anchor="w")

        scroll_y = ttk.Scrollbar(table_container, orient="vertical", command=self.tree_user.yview)
        self.tree_user.configure(yscrollcommand=scroll_y.set)

        self.tree_user.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

    def _cargar_datos_usuarios(self, lista: List[Usuario] = None) -> None:
        """Puebla el Treeview de usuarios mediante el servicio."""
        for item in self.tree_user.get_children():
            self.tree_user.delete(item)

        usuarios = lista if lista is not None else self.servicio.listar_usuarios()

        for idx, u in enumerate(usuarios):
            tag = "par" if idx % 2 == 0 else "impar"
            self.tree_user.insert(
                "",
                "end",
                values=(u.identificacion, u.nombre, u.correo),
                tags=(tag,)
            )

        self.tree_user.tag_configure("par", background="#ffffff")
        self.tree_user.tag_configure("impar", background="#f8fafc")

        self.lbl_total_user.config(text=f"Total Usuarios: {self.servicio.contar_usuarios()}")

    def _filtrar_usuarios(self) -> None:
        """Filtra usuarios en memoria a través del servicio."""
        termino = self.txt_buscar_user.get()
        filtrados = self.servicio.buscar_usuarios(termino)
        self._cargar_datos_usuarios(filtrados)

    def _restablecer_usuarios(self) -> None:
        """Limpia la búsqueda y muestra todos los usuarios."""
        self.txt_buscar_user.delete(0, tk.END)
        self._cargar_datos_usuarios()

    # =========================================================================
    # PESTAÑA: VENTAS (FUNCIONALIDAD FUTURA / PENDIENTE)
    # =========================================================================
    def _crear_tab_ventas_pendiente(self) -> None:
        """
        Construye la sección informativa de Ventas, cumpliendo con la directriz
        de mantener identificadas las funcionalidades futuras sin desarrollarlas prematuramente.
        """
        tab = tk.Frame(self.notebook, bg="#ffffff", padx=20, pady=30)
        self.notebook.add(tab, text=" 🛒 Ventas (Próximamente) ")

        card = tk.Frame(tab, bg="#f8fafc", bd=1, relief="solid", padx=25, pady=25)
        card.place(relx=0.5, rely=0.5, anchor="center")

        lbl_icono = tk.Label(card, text="🛒", font=("Segoe UI Emoji", 40), bg="#f8fafc")
        lbl_icono.pack(pady=(0, 5))

        lbl_titulo = tk.Label(
            card,
            text="Módulo de Ventas y Facturación",
            font=("Helvetica", 15, "bold"),
            fg="#1f2937",
            bg="#f8fafc"
        )
        lbl_titulo.pack()

        badge = tk.Label(
            card,
            text="ESTADO: FUNCIONALIDAD PENDIENTE",
            font=("Helvetica", 8, "bold"),
            bg="#fef3c7",
            fg="#92400e",
            padx=8,
            pady=3
        )
        badge.pack(pady=(6, 15))

        texto_explicativo = (
            "En cumplimiento con la rúbrica y alcance pedagógico de la Semana 13, esta versión base "
            "se enfoca en los fundamentos de Tkinter, la ventana principal y la separación en capas.\n\n"
            "En las próximas semanas de la asignatura se integrará este módulo para permitir:\n"
            "• Registro interactivo de ventas (Usuario - Producto).\n"
            "• Descuento automático de existencias en el inventario.\n"
            "• Historial transaccional y reportes de consumo."
        )

        lbl_desc = tk.Label(
            card,
            text=texto_explicativo,
            font=("Helvetica", 9),
            fg="#4b5563",
            bg="#f8fafc",
            justify="center",
            wraplength=480
        )
        lbl_desc.pack()
