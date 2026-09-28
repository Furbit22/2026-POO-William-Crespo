import os
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, List, Optional
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.restaurante_servicio import RestauranteServicio

class MainView(tk.Frame):
    """
    Panel principal de la aplicación restaurante_app para la Semana 16.
    Implementa el manejo integral de eventos en Tkinter aplicado a la gestión de usuarios:
      INTERACCIÓN -> EVENTO -> bind() / command= -> CALLBACK -> SERVICIO -> PERSISTENCIA -> RESPUESTA VISUAL
    
    Eventos destacados:
      - <<TreeviewSelect>> : Selección en tabla y carga automática de usuario en el formulario.
      - <Return>           : Atajo de teclado para confirmar el registro (Enter).
      - <Escape>           : Atajo de teclado para limpiar formulario y cancelar selección (Esc).
      - <<ComboboxSelected>> : Respuesta inmediata al cambio de rol seleccionado.
      - command=           : Invocación directa de métodos desde botones principales.
      - Control de roles  : Acceso administrativo exclusivo para rol Administrador.
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

        self.logo_header_img: Optional[tk.PhotoImage] = None
        self._cargar_recursos_assets()

        self._configurar_estilos()
        self._crear_interfaz()

        # Carga inicial de datos en las tres secciones
        self._cargar_datos_productos()
        self._cargar_datos_usuarios()
        self._cargar_datos_ventas()
        self._actualizar_combos_ventas()

    def _cargar_recursos_assets(self) -> None:
        """Carga el logotipo del encabezado desde la carpeta assets/."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_logo = os.path.join(base_dir, "assets", "logo_header.png")

        if not os.path.exists(ruta_logo):
            ruta_logo = os.path.join(base_dir, "assets", "logo_restaurante.png")

        if os.path.exists(ruta_logo):
            try:
                self.logo_header_img = tk.PhotoImage(file=ruta_logo)
            except Exception as e:
                print(f"[MainView] No se pudo cargar el logo de cabecera: {e}")
                self.logo_header_img = None

    def _configurar_estilos(self) -> None:
        """Configura los estilos temáticos ttk para pestañas, agrupadores y tablas."""
        estilo = ttk.Style()
        estilo.theme_use("clam")

        # Pestañas (Notebook)
        estilo.configure("TNotebook", background="#f3f4f6", borderwidth=0)
        estilo.configure(
            "TNotebook.Tab",
            font=("Helvetica", 10, "bold"),
            padding=[18, 8],
            background="#e5e7eb",
            foreground="#374151"
        )
        estilo.map(
            "TNotebook.Tab",
            background=[("selected", "#2563eb")],
            foreground=[("selected", "#ffffff")]
        )

        # Agrupadores (LabelFrame)
        estilo.configure(
            "TLabelframe",
            background="#ffffff",
            relief="solid",
            borderwidth=1
        )
        estilo.configure(
            "TLabelframe.Label",
            font=("Helvetica", 10, "bold"),
            foreground="#1e3a8a",
            background="#ffffff",
            padding=[6, 2]
        )

        # Tablas (Treeview)
        estilo.configure(
            "Treeview",
            font=("Helvetica", 9),
            rowheight=26,
            background="#ffffff",
            fieldbackground="#ffffff",
            foreground="#1f2937"
        )
        estilo.configure(
            "Treeview.Heading",
            font=("Helvetica", 9, "bold"),
            background="#e2e8f0",
            foreground="#1f2937",
            relief="flat"
        )
        estilo.map("Treeview.Heading", background=[("active", "#cbd5e1")])

    def _crear_interfaz(self) -> None:
        """Construye la distribución de contenedores principales del sistema."""
        # 1. Barra Superior (Header)
        header = tk.Frame(self, bg="#1e293b", padx=20, pady=10)
        header.pack(fill="x", side="top")

        info_header = tk.Frame(header, bg="#1e293b")
        info_header.pack(side="left")

        # Si el logotipo está cargado desde assets/, se muestra en el header
        if self.logo_header_img is not None:
            lbl_logo = tk.Label(info_header, image=self.logo_header_img, bg="#1e293b")
            lbl_logo.pack(side="left", padx=(0, 15))
        else:
            lbl_app = tk.Label(
                info_header,
                text="🍽️ Restaurante App — Gestión & Eventos",
                font=("Helvetica", 14, "bold"),
                fg="#ffffff",
                bg="#1e293b"
            )
            lbl_app.pack(anchor="w")

        datos_sesion = tk.Frame(info_header, bg="#1e293b")
        datos_sesion.pack(side="left" if self.logo_header_img else "top", fill="x")

        lbl_sesion = tk.Label(
            datos_sesion,
            text=f"Sesión activa: {self.usuario_actual.nombre} ({self.usuario_actual.identificacion}) | Rol: {self.usuario_actual.rol}",
            font=("Helvetica", 9, "bold"),
            fg="#cbd5e1",
            bg="#1e293b"
        )
        lbl_sesion.pack(anchor="w")

        lbl_sub = tk.Label(
            datos_sesion,
            text="Semana 16 — Manejo de Eventos en Gestión de Usuarios (POO)",
            font=("Helvetica", 8),
            fg="#94a3b8",
            bg="#1e293b"
        )
        lbl_sub.pack(anchor="w")

        # Botón de Cierre de Sesión
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
            padx=14,
            pady=6,
            command=self.on_logout
        )
        btn_logout.pack(side="right")

        # 2. Navegación por Secciones (ttk.Notebook)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=10)

        # Secciones requeridas por la consigna
        self._crear_tab_productos()
        self._crear_tab_usuarios()
        self._crear_tab_ventas()

        # 3. Barra de Estado Inferior (Footer)
        self.footer = tk.Frame(self, bg="#e2e8f0", padx=15, pady=6)
        self.footer.pack(fill="x", side="bottom")

        self.lbl_footer_status = tk.Label(
            self.footer,
            text="Semana 16 — Eventos activos: <<TreeviewSelect>>, <Return>, <Escape>, <<ComboboxSelected>>.",
            font=("Helvetica", 8),
            fg="#475569",
            bg="#e2e8f0"
        )
        self.lbl_footer_status.pack(side="left")

    def _actualizar_estado_global(self, mensaje: str) -> None:
        """Actualiza el texto descriptivo de la barra de estado en el footer."""
        self.lbl_footer_status.config(text=mensaje)

    # =========================================================================
    # SECCIÓN 1: GESTIÓN DE PRODUCTOS (CRUD)
    # =========================================================================
    def _crear_tab_productos(self) -> None:
        """Construye la vista de gestión completa de productos."""
        tab = tk.Frame(self.notebook, bg="#ffffff", padx=14, pady=12)
        self.notebook.add(tab, text=" 📦 Gestión de Productos ")

        # Panel Superior: Métricas y Búsqueda
        panel_superior = tk.Frame(tab, bg="#ffffff")
        panel_superior.pack(fill="x", pady=(0, 10))

        stats_frame = tk.Frame(panel_superior, bg="#f8fafc", bd=1, relief="solid", padx=12, pady=6)
        stats_frame.pack(side="left")

        self.lbl_total_prod = tk.Label(
            stats_frame,
            text=f"Total Platillos: {self.servicio.contar_productos()}",
            font=("Helvetica", 9, "bold"),
            fg="#1e40af",
            bg="#f8fafc"
        )
        self.lbl_total_prod.pack(side="left", padx=(0, 15))

        self.lbl_stock_total = tk.Label(
            stats_frame,
            text=f"Existencias Totales: {self.servicio.obtener_stock_total()} u.",
            font=("Helvetica", 9, "bold"),
            fg="#047857",
            bg="#f8fafc"
        )
        self.lbl_stock_total.pack(side="left")

        # Búsqueda
        search_frame = tk.Frame(panel_superior, bg="#ffffff")
        search_frame.pack(side="right")

        tk.Label(search_frame, text="Filtrar:", font=("Helvetica", 9, "bold"), bg="#ffffff", fg="#374151").pack(side="left", padx=(0, 5))
        self.txt_buscar_prod = ttk.Entry(search_frame, width=18, font=("Helvetica", 9))
        self.txt_buscar_prod.pack(side="left", padx=(0, 5))
        self.txt_buscar_prod.bind("<KeyRelease>", lambda e: self._filtrar_productos())

        btn_limpiar_busq = tk.Button(
            search_frame,
            text="Restablecer",
            font=("Helvetica", 8),
            bg="#e5e7eb",
            relief="flat",
            cursor="hand2",
            command=self._restablecer_productos
        )
        btn_limpiar_busq.pack(side="left")

        # Contenedor Central Dividido
        panel_central = tk.Frame(tab, bg="#ffffff")
        panel_central.pack(fill="both", expand=True)

        # Formulario de Producto (LabelFrame)
        self.frame_formulario = ttk.LabelFrame(panel_central, text=" Formulario de Producto ", padding=[12, 10])
        self.frame_formulario.pack(side="left", fill="y", padx=(0, 12))

        # Fila 0: Código
        tk.Label(self.frame_formulario, text="Código del Producto *:", font=("Helvetica", 9, "bold"), bg="#ffffff", anchor="w").grid(row=0, column=0, sticky="w", pady=(2, 2))
        box_codigo = tk.Frame(self.frame_formulario, bg="#ffffff")
        box_codigo.grid(row=1, column=0, sticky="ew", pady=(0, 8))

        self.txt_codigo = ttk.Entry(box_codigo, width=14, font=("Helvetica", 9))
        self.txt_codigo.pack(side="left", fill="x", expand=True, padx=(0, 5))

        btn_consultar_codigo = tk.Button(
            box_codigo,
            text="🔍 Cargar",
            font=("Helvetica", 8, "bold"),
            bg="#3b82f6",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=6,
            pady=2,
            command=self._cargar_por_codigo
        )
        btn_consultar_codigo.pack(side="right")

        # Fila 2: Nombre
        tk.Label(self.frame_formulario, text="Nombre del Platillo / Producto *:", font=("Helvetica", 9, "bold"), bg="#ffffff", anchor="w").grid(row=2, column=0, sticky="w", pady=(2, 2))
        self.txt_nombre = ttk.Entry(self.frame_formulario, width=28, font=("Helvetica", 9))
        self.txt_nombre.grid(row=3, column=0, sticky="ew", pady=(0, 8))

        # Fila 4: Categoría
        tk.Label(self.frame_formulario, text="Categoría *:", font=("Helvetica", 9, "bold"), bg="#ffffff", anchor="w").grid(row=4, column=0, sticky="w", pady=(2, 2))
        self.combo_categoria = ttk.Combobox(
            self.frame_formulario,
            values=["Comida", "Bebida", "Acompañamiento", "Postre", "Cafetería"],
            state="readonly",
            font=("Helvetica", 9)
        )
        self.combo_categoria.current(0)
        self.combo_categoria.grid(row=5, column=0, sticky="ew", pady=(0, 8))

        # Fila 6: Precio y Stock en doble columna
        num_frame = tk.Frame(self.frame_formulario, bg="#ffffff")
        num_frame.grid(row=6, column=0, sticky="ew", pady=(0, 8))

        tk.Label(num_frame, text="Precio ($) *:", font=("Helvetica", 9, "bold"), bg="#ffffff").grid(row=0, column=0, sticky="w")
        self.txt_precio = ttk.Entry(num_frame, width=12, font=("Helvetica", 9))
        self.txt_precio.grid(row=1, column=0, sticky="w", padx=(0, 10))

        tk.Label(num_frame, text="Existencias *:", font=("Helvetica", 9, "bold"), bg="#ffffff").grid(row=0, column=1, sticky="w")
        self.spin_stock = ttk.Spinbox(num_frame, from_=0, to=9999, width=10, font=("Helvetica", 9))
        self.spin_stock.set(0)
        self.spin_stock.grid(row=1, column=1, sticky="w")

        # Banner de feedback del formulario
        self.lbl_feedback_prod = tk.Label(self.frame_formulario, text="", font=("Helvetica", 8), bg="#ffffff", wraplength=230)
        self.lbl_feedback_prod.grid(row=7, column=0, sticky="ew", pady=(4, 8))

        # Botones de Acción CRUD
        btn_frame = tk.Frame(self.frame_formulario, bg="#ffffff")
        btn_frame.grid(row=8, column=0, sticky="ew")

        btn_registrar = tk.Button(btn_frame, text="➕ Registrar", font=("Helvetica", 9, "bold"), bg="#16a34a", fg="#ffffff", relief="flat", cursor="hand2", padx=8, pady=5, command=self._registrar_producto)
        btn_registrar.pack(fill="x", pady=(0, 4))

        fila_btns = tk.Frame(btn_frame, bg="#ffffff")
        fila_btns.pack(fill="x", pady=(0, 4))

        btn_actualizar = tk.Button(fila_btns, text="✏️ Actualizar", font=("Helvetica", 8, "bold"), bg="#f59e0b", fg="#ffffff", relief="flat", cursor="hand2", padx=6, pady=4, command=self._actualizar_producto)
        btn_actualizar.pack(side="left", fill="x", expand=True, padx=(0, 2))

        btn_eliminar = tk.Button(fila_btns, text="🗑️ Eliminar", font=("Helvetica", 8, "bold"), bg="#ef4444", fg="#ffffff", relief="flat", cursor="hand2", padx=6, pady=4, command=self._eliminar_producto)
        btn_eliminar.pack(side="right", fill="x", expand=True, padx=(2, 0))

        btn_limpiar = tk.Button(btn_frame, text="🧹 Limpiar Formulario", font=("Helvetica", 8), bg="#6b7280", fg="#ffffff", relief="flat", cursor="hand2", pady=4, command=self._limpiar_formulario_producto)
        btn_limpiar.pack(fill="x")

        # Catálogo de Productos (LabelFrame + Treeview + Scrollbar)
        frame_catalogo = ttk.LabelFrame(panel_central, text=" Catálogo de Productos Registrados ", padding=[8, 8])
        frame_catalogo.pack(side="right", fill="both", expand=True)

        table_box = tk.Frame(frame_catalogo, bg="#ffffff")
        table_box.pack(fill="both", expand=True)

        cols = ("codigo", "nombre", "categoria", "precio", "stock")
        self.tree_prod = ttk.Treeview(table_box, columns=cols, show="headings", selectmode="browse")

        self.tree_prod.heading("codigo", text="Código")
        self.tree_prod.heading("nombre", text="Nombre del Platillo")
        self.tree_prod.heading("categoria", text="Categoría")
        self.tree_prod.heading("precio", text="Precio ($)")
        self.tree_prod.heading("stock", text="Stock")

        self.tree_prod.column("codigo", width=75, anchor="center")
        self.tree_prod.column("nombre", width=190, anchor="w")
        self.tree_prod.column("categoria", width=110, anchor="center")
        self.tree_prod.column("precio", width=85, anchor="e")
        self.tree_prod.column("stock", width=70, anchor="center")

        scroll_prod_y = ttk.Scrollbar(table_box, orient="vertical", command=self.tree_prod.yview)
        self.tree_prod.configure(yscrollcommand=scroll_prod_y.set)

        self.tree_prod.pack(side="left", fill="both", expand=True)
        scroll_prod_y.pack(side="right", fill="y")

        # Acciones de catálogo
        acciones_box = tk.Frame(frame_catalogo, bg="#ffffff", pady=4)
        acciones_box.pack(fill="x")

        tk.Button(
            acciones_box,
            text="📥 Cargar Fila Seleccionada al Formulario",
            font=("Helvetica", 8, "bold"),
            bg="#2563eb",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=3,
            command=self._cargar_seleccion_tabla_producto
        ).pack(side="left")

        tk.Button(
            acciones_box,
            text="🗑️ Eliminar Fila",
            font=("Helvetica", 8),
            bg="#fee2e2",
            fg="#b91c1c",
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=3,
            command=self._eliminar_seleccion_tabla_producto
        ).pack(side="right")

    def _cargar_datos_productos(self, lista: Optional[List[Producto]] = None) -> None:
        """Carga o refresca los productos en el Treeview."""
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

        self.lbl_total_prod.config(text=f"Total Platillos: {self.servicio.contar_productos()}")
        self.lbl_stock_total.config(text=f"Existencias Totales: {self.servicio.obtener_stock_total()} u.")

    def _mostrar_feedback_producto(self, mensaje: str, es_error: bool = False) -> None:
        """Muestra retroalimentación visual en el formulario de productos."""
        color = "#dc2626" if es_error else "#16a34a"
        self.lbl_feedback_prod.config(text=mensaje, fg=color)

    def _limpiar_formulario_producto(self) -> None:
        """Vacia las cajas de texto del formulario de productos."""
        self.txt_codigo.delete(0, tk.END)
        self.txt_nombre.delete(0, tk.END)
        self.combo_categoria.current(0)
        self.txt_precio.delete(0, tk.END)
        self.spin_stock.set(0)
        self.lbl_feedback_prod.config(text="")
        self.txt_codigo.focus_set()

    def _registrar_producto(self) -> None:
        """Callback para registrar producto."""
        cod = self.txt_codigo.get()
        nom = self.txt_nombre.get()
        cat = self.combo_categoria.get()
        prec = self.txt_precio.get()
        stk = self.spin_stock.get()

        exito, mensaje, nuevo_prod = self.servicio.registrar_producto(cod, nom, cat, prec, stk)
        if not exito:
            self._mostrar_feedback_producto(mensaje, es_error=True)
            messagebox.showwarning("Atención", mensaje, parent=self)
            return

        self._mostrar_feedback_producto(mensaje, es_error=False)
        self._actualizar_estado_global(f"➕ {mensaje}")
        self._cargar_datos_productos()
        self._actualizar_combos_ventas()
        self._limpiar_formulario_producto()
        messagebox.showinfo("Registro Exitoso", mensaje, parent=self)

    def _cargar_por_codigo(self) -> None:
        """Consulta un producto por su código y llena el formulario."""
        codigo = self.txt_codigo.get()
        if not codigo.strip():
            self._mostrar_feedback_producto("Ingrese un código para buscar.", es_error=True)
            return

        producto = self.servicio.consultar_producto(codigo)
        if producto is None:
            self._mostrar_feedback_producto(f"No existe el código '{codigo.upper()}'.", es_error=True)
            return

        self._poblar_formulario_producto(producto)
        self._mostrar_feedback_producto(f"Producto '{producto.codigo}' cargado.", es_error=False)

    def _poblar_formulario_producto(self, producto: Producto) -> None:
        """Llena los campos del formulario con los atributos del producto."""
        self.txt_codigo.delete(0, tk.END)
        self.txt_codigo.insert(0, producto.codigo)

        self.txt_nombre.delete(0, tk.END)
        self.txt_nombre.insert(0, producto.nombre)

        if producto.categoria in self.combo_categoria["values"]:
            self.combo_categoria.set(producto.categoria)

        self.txt_precio.delete(0, tk.END)
        self.txt_precio.insert(0, str(producto.precio))

        self.spin_stock.set(producto.stock)

    def _actualizar_producto(self) -> None:
        """Callback para actualizar un producto existente."""
        cod = self.txt_codigo.get()
        nom = self.txt_nombre.get()
        cat = self.combo_categoria.get()
        prec = self.txt_precio.get()
        stk = self.spin_stock.get()

        exito, mensaje, prod_actualizado = self.servicio.actualizar_producto(cod, nom, cat, prec, stk)
        if not exito:
            self._mostrar_feedback_producto(mensaje, es_error=True)
            messagebox.showwarning("Atención", mensaje, parent=self)
            return

        self._mostrar_feedback_producto(mensaje, es_error=False)
        self._actualizar_estado_global(f"✏️ {mensaje}")
        self._cargar_datos_productos()
        self._actualizar_combos_ventas()
        messagebox.showinfo("Actualización Exitosa", mensaje, parent=self)

    def _eliminar_producto(self) -> None:
        """Callback para eliminar un producto."""
        codigo = self.txt_codigo.get()
        if not codigo.strip():
            self._mostrar_feedback_producto("Indique el código del producto a eliminar.", es_error=True)
            return

        producto = self.servicio.consultar_producto(codigo)
        if producto is None:
            self._mostrar_feedback_producto("El producto no existe.", es_error=True)
            return

        if not messagebox.askyesno("Confirmar", f"¿Eliminar '{producto.nombre}'?", parent=self):
            return

        exito, mensaje = self.servicio.eliminar_producto(codigo)
        if exito:
            self._mostrar_feedback_producto(mensaje, es_error=False)
            self._actualizar_estado_global(f"🗑️ {mensaje}")
            self._cargar_datos_productos()
            self._actualizar_combos_ventas()
            self._limpiar_formulario_producto()
            messagebox.showinfo("Eliminado", mensaje, parent=self)
        else:
            self._mostrar_feedback_producto(mensaje, es_error=True)

    def _cargar_seleccion_tabla_producto(self) -> None:
        """Carga la fila seleccionada del Treeview al formulario."""
        sel = self.tree_prod.selection()
        if not sel:
            messagebox.showinfo("Información", "Seleccione una fila del catálogo.", parent=self)
            return
        cod = self.tree_prod.item(sel[0], "values")[0]
        p = self.servicio.consultar_producto(cod)
        if p:
            self._poblar_formulario_producto(p)

    def _eliminar_seleccion_tabla_producto(self) -> None:
        """Elimina la fila seleccionada del Treeview."""
        sel = self.tree_prod.selection()
        if not sel:
            messagebox.showinfo("Información", "Seleccione una fila a eliminar.", parent=self)
            return
        cod = self.tree_prod.item(sel[0], "values")[0]
        self.txt_codigo.delete(0, tk.END)
        self.txt_codigo.insert(0, cod)
        self._eliminar_producto()

    def _filtrar_productos(self) -> None:
        """Filtra productos según el criterio de búsqueda."""
        crit = self.txt_buscar_prod.get()
        self._cargar_datos_productos(self.servicio.buscar_productos(crit))

    def _restablecer_productos(self) -> None:
        """Limpia el filtro de productos."""
        self.txt_buscar_prod.delete(0, tk.END)
        self._cargar_datos_productos()

    # =========================================================================
    # SECCIÓN 2: GESTIÓN DE USUARIOS Y ROLES (SEMANA 16 - MANEJO DE EVENTOS)
    # =========================================================================
    def _crear_tab_usuarios(self) -> None:
        """
        Construye la sección de usuarios según los privilegios del rol autenticado.
        - Administrador: Dispone del panel completo de gestión (CRUD, eventos, atajos, Treeview).
        - Empleado / Cliente: Dispone de vista informativa restringida sin privilegios administrativos.
        """
        if self.usuario_actual.es_administrador:
            self._crear_tab_usuarios_admin()
        else:
            self._crear_tab_usuarios_restringido()

    def _crear_tab_usuarios_admin(self) -> None:
        """Construye la vista de gestión completa de usuarios para el Administrador."""
        tab = tk.Frame(self.notebook, bg="#ffffff", padx=14, pady=12)
        self.notebook.add(tab, text=" 👥 Gestión de Usuarios ")

        # Panel Superior: Métricas de Usuarios y Búsqueda
        panel_superior = tk.Frame(tab, bg="#ffffff")
        panel_superior.pack(fill="x", pady=(0, 10))

        stats_frame = tk.Frame(panel_superior, bg="#f8fafc", bd=1, relief="solid", padx=12, pady=6)
        stats_frame.pack(side="left")

        self.lbl_total_user = tk.Label(
            stats_frame,
            text=f"Total Usuarios: {self.servicio.contar_usuarios()}",
            font=("Helvetica", 9, "bold"),
            fg="#1e40af",
            bg="#f8fafc"
        )
        self.lbl_total_user.pack(side="left", padx=(0, 15))

        self.lbl_resumen_roles = tk.Label(
            stats_frame,
            text=self._obtener_resumen_roles_texto(),
            font=("Helvetica", 9),
            fg="#047857",
            bg="#f8fafc"
        )
        self.lbl_resumen_roles.pack(side="left")

        # Búsqueda con evento <KeyRelease>
        search_frame = tk.Frame(panel_superior, bg="#ffffff")
        search_frame.pack(side="right")

        tk.Label(search_frame, text="Filtrar:", font=("Helvetica", 9, "bold"), bg="#ffffff", fg="#374151").pack(side="left", padx=(0, 5))
        self.txt_buscar_user = ttk.Entry(search_frame, width=18, font=("Helvetica", 9))
        self.txt_buscar_user.pack(side="left", padx=(0, 5))
        self.txt_buscar_user.bind("<KeyRelease>", lambda e: self._filtrar_usuarios())

        btn_limpiar_busq_user = tk.Button(
            search_frame,
            text="Restablecer",
            font=("Helvetica", 8),
            bg="#e5e7eb",
            relief="flat",
            cursor="hand2",
            command=self._restablecer_usuarios
        )
        btn_limpiar_busq_user.pack(side="left")

        # Contenedor Central Dividido (Formulario a la Izq y Treeview a la Der)
        panel_central = tk.Frame(tab, bg="#ffffff")
        panel_central.pack(fill="both", expand=True)

        # ----------------- PANEL IZQUIERDO: Formulario de Usuario -----------------
        self.frame_form_usuario = ttk.LabelFrame(
            panel_central,
            text=" Formulario de Usuario (Manejo de Eventos) ",
            padding=[12, 10]
        )
        self.frame_form_usuario.pack(side="left", fill="y", padx=(0, 12))

        # Campo: Identificación
        tk.Label(
            self.frame_form_usuario,
            text="Identificación / Cédula *:",
            font=("Helvetica", 9, "bold"),
            bg="#ffffff",
            anchor="w"
        ).grid(row=0, column=0, sticky="w", pady=(2, 2))

        self.txt_user_id = ttk.Entry(self.frame_form_usuario, width=28, font=("Helvetica", 9))
        self.txt_user_id.grid(row=1, column=0, sticky="ew", pady=(0, 6))

        # Campo: Nombre Completo
        tk.Label(
            self.frame_form_usuario,
            text="Nombre Completo *:",
            font=("Helvetica", 9, "bold"),
            bg="#ffffff",
            anchor="w"
        ).grid(row=2, column=0, sticky="w", pady=(2, 2))

        self.txt_user_nombre = ttk.Entry(self.frame_form_usuario, width=28, font=("Helvetica", 9))
        self.txt_user_nombre.grid(row=3, column=0, sticky="ew", pady=(0, 6))

        # Campo: Correo Electrónico
        tk.Label(
            self.frame_form_usuario,
            text="Correo Electrónico *:",
            font=("Helvetica", 9, "bold"),
            bg="#ffffff",
            anchor="w"
        ).grid(row=4, column=0, sticky="w", pady=(2, 2))

        self.txt_user_correo = ttk.Entry(self.frame_form_usuario, width=28, font=("Helvetica", 9))
        self.txt_user_correo.grid(row=5, column=0, sticky="ew", pady=(0, 6))

        # Campo: Rol (Combobox con evento <<ComboboxSelected>>)
        tk.Label(
            self.frame_form_usuario,
            text="Rol del Sistema *:",
            font=("Helvetica", 9, "bold"),
            bg="#ffffff",
            anchor="w"
        ).grid(row=6, column=0, sticky="w", pady=(2, 2))

        self.combo_user_rol = ttk.Combobox(
            self.frame_form_usuario,
            values=["Administrador", "Empleado", "Cliente"],
            state="readonly",
            font=("Helvetica", 9)
        )
        self.combo_user_rol.current(2)  # Por defecto 'Cliente'
        self.combo_user_rol.grid(row=7, column=0, sticky="ew", pady=(0, 4))

        # EVENTO VIRTUAL: <<ComboboxSelected>> asociado mediante bind()
        self.combo_user_rol.bind("<<ComboboxSelected>>", self._al_cambiar_rol_combobox)

        # Micro-tarjeta descriptiva dinámica del rol seleccionado
        self.lbl_info_rol = tk.Label(
            self.frame_form_usuario,
            text="Rol Cliente: Comensal registrado en el restaurante.",
            font=("Helvetica", 8, "italic"),
            fg="#4b5563",
            bg="#f1f5f9",
            bd=1,
            relief="solid",
            padx=6,
            pady=3,
            anchor="w"
        )
        self.lbl_info_rol.grid(row=8, column=0, sticky="ew", pady=(2, 8))

        # Atajos de teclado en el formulario:
        # <Return> -> Atajo para registrar usuario (reutiliza _registrar_usuario)
        # <Escape> -> Atajo para limpiar formulario y deseleccionar tabla
        for widget in (self.txt_user_id, self.txt_user_nombre, self.txt_user_correo, self.combo_user_rol):
            widget.bind("<Return>", self._al_presionar_enter_usuario)
            widget.bind("<Escape>", self._al_presionar_escape_usuario)

        # Etiqueta de retroalimentación visual del formulario
        self.lbl_feedback_user = tk.Label(
            self.frame_form_usuario,
            text="",
            font=("Helvetica", 8),
            bg="#ffffff",
            wraplength=230
        )
        self.lbl_feedback_user.grid(row=9, column=0, sticky="ew", pady=(0, 6))

        # Botones de Acción CRUD (asociados mediante command=)
        btn_user_frame = tk.Frame(self.frame_form_usuario, bg="#ffffff")
        btn_user_frame.grid(row=10, column=0, sticky="ew")

        # Botón Registrar
        btn_registrar_user = tk.Button(
            btn_user_frame,
            text="➕ Registrar Usuario (Enter)",
            font=("Helvetica", 9, "bold"),
            bg="#16a34a",
            fg="#ffffff",
            activebackground="#15803d",
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=5,
            command=self._registrar_usuario
        )
        btn_registrar_user.pack(fill="x", pady=(0, 4))

        # Fila de Actualizar y Eliminar
        fila_btns_user = tk.Frame(btn_user_frame, bg="#ffffff")
        fila_btns_user.pack(fill="x", pady=(0, 4))

        btn_actualizar_user = tk.Button(
            fila_btns_user,
            text="✏️ Actualizar",
            font=("Helvetica", 8, "bold"),
            bg="#f59e0b",
            fg="#ffffff",
            activebackground="#d97706",
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=6,
            pady=4,
            command=self._actualizar_usuario
        )
        btn_actualizar_user.pack(side="left", fill="x", expand=True, padx=(0, 2))

        btn_eliminar_user = tk.Button(
            fila_btns_user,
            text="🗑️ Eliminar",
            font=("Helvetica", 8, "bold"),
            bg="#ef4444",
            fg="#ffffff",
            activebackground="#dc2626",
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=6,
            pady=4,
            command=self._eliminar_usuario
        )
        btn_eliminar_user.pack(side="right", fill="x", expand=True, padx=(2, 0))

        # Botón Limpiar
        btn_limpiar_user = tk.Button(
            btn_user_frame,
            text="🧹 Limpiar Formulario (Esc)",
            font=("Helvetica", 8),
            bg="#6b7280",
            fg="#ffffff",
            activebackground="#4b5563",
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            pady=4,
            command=self._limpiar_formulario_usuario
        )
        btn_limpiar_user.pack(fill="x", pady=(0, 8))

        # Tarjeta pedagógica de referencia de eventos
        tarjeta_eventos = tk.Frame(self.frame_form_usuario, bg="#f8fafc", bd=1, relief="solid", padx=8, pady=6)
        tarjeta_eventos.grid(row=11, column=0, sticky="ew")

        tk.Label(
            tarjeta_eventos,
            text="📌 Eventos Tkinter Semana 16:",
            font=("Helvetica", 8, "bold"),
            fg="#1e40af",
            bg="#f8fafc"
        ).pack(anchor="w")

        info_ev = (
            "• <<TreeviewSelect>> : Carga fila al formulario.\n"
            "• <Return> : Atajo Enter para registrar.\n"
            "• <Escape> : Atajo Esc para limpiar / cancelar.\n"
            "• <<ComboboxSelected>> : Cambio de rol.\n"
            "• command= : Callbacks en botones."
        )
        tk.Label(
            tarjeta_eventos,
            text=info_ev,
            font=("Helvetica", 7),
            fg="#475569",
            bg="#f8fafc",
            justify="left"
        ).pack(anchor="w")

        # ----------------- PANEL DERECHO: Catálogo de Usuarios -----------------
        frame_directorio = ttk.LabelFrame(
            panel_central,
            text=" Catálogo de Usuarios Registrados (Treeview) ",
            padding=[8, 8]
        )
        frame_directorio.pack(side="right", fill="both", expand=True)

        table_user_box = tk.Frame(frame_directorio, bg="#ffffff")
        table_user_box.pack(fill="both", expand=True)

        cols_u = ("identificacion", "nombre", "correo", "rol")
        self.tree_user = ttk.Treeview(
            table_user_box,
            columns=cols_u,
            show="headings",
            selectmode="browse"
        )

        self.tree_user.heading("identificacion", text="ID / Cédula")
        self.tree_user.heading("nombre", text="Nombre Completo")
        self.tree_user.heading("correo", text="Correo Electrónico")
        self.tree_user.heading("rol", text="Rol del Sistema")

        self.tree_user.column("identificacion", width=95, anchor="center")
        self.tree_user.column("nombre", width=180, anchor="w")
        self.tree_user.column("correo", width=190, anchor="w")
        self.tree_user.column("rol", width=110, anchor="center")

        scroll_user_y = ttk.Scrollbar(table_user_box, orient="vertical", command=self.tree_user.yview)
        self.tree_user.configure(yscrollcommand=scroll_user_y.set)

        self.tree_user.pack(side="left", fill="both", expand=True)
        scroll_user_y.pack(side="right", fill="y")

        # EVENTO VIRTUAL: <<TreeviewSelect>> asociado mediante bind()
        self.tree_user.bind("<<TreeviewSelect>>", self._al_seleccionar_usuario_treeview)
        # Atajo <Escape> en la tabla para deseleccionar
        self.tree_user.bind("<Escape>", self._al_presionar_escape_usuario)

        # Acciones auxiliares de la tabla
        acciones_user_box = tk.Frame(frame_directorio, bg="#ffffff", pady=4)
        acciones_user_box.pack(fill="x")

        tk.Label(
            acciones_user_box,
            text="💡 Haga clic en cualquier fila para cargar automáticamente sus datos mediante <<TreeviewSelect>>.",
            font=("Helvetica", 8, "italic"),
            fg="#64748b",
            bg="#ffffff"
        ).pack(side="left")

        tk.Button(
            acciones_user_box,
            text="🗑️ Eliminar Fila",
            font=("Helvetica", 8),
            bg="#fee2e2",
            fg="#b91c1c",
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=2,
            command=self._eliminar_usuario
        ).pack(side="right")

    def _crear_tab_usuarios_restringido(self) -> None:
        """
        Construye la vista de usuarios en modo restringido para Empleado o Cliente.
        Evita el acceso a la gestión administrativa de cuentas conforme a la consigna.
        """
        tab = tk.Frame(self.notebook, bg="#ffffff", padx=15, pady=12)
        self.notebook.add(tab, text=" 👥 Usuarios (Acceso Restringido) ")

        # Tarjeta de Alerta de Seguridad
        banner_aviso = tk.Frame(tab, bg="#fef2f2", bd=1, relief="solid", padx=14, pady=10)
        banner_aviso.pack(fill="x", pady=(0, 12))

        tk.Label(
            banner_aviso,
            text="🔒 Acceso Administrativo Restringido",
            font=("Helvetica", 10, "bold"),
            fg="#991b1b",
            bg="#fef2f2"
        ).pack(anchor="w")

        texto_restringido = (
            f"Ha iniciado sesión como '{self.usuario_actual.nombre}' con el rol '{self.usuario_actual.rol}'.\n"
            "La gestión administrativa (crear, modificar o eliminar cuentas de usuarios) está reservada "
            "exclusivamente para el Administrador del sistema.\n"
            "Su perfil dispone únicamente de consulta de directorio en modo lectura."
        )
        tk.Label(
            banner_aviso,
            text=texto_restringido,
            font=("Helvetica", 8),
            fg="#7f1d1d",
            bg="#fef2f2",
            justify="left"
        ).pack(anchor="w", pady=(4, 0))

        # Panel de Búsqueda
        top_panel = tk.Frame(tab, bg="#ffffff")
        top_panel.pack(fill="x", pady=(0, 10))

        self.lbl_total_user = tk.Label(
            top_panel,
            text=f"Total Usuarios Registrados: {self.servicio.contar_usuarios()}",
            font=("Helvetica", 9, "bold"),
            fg="#1e40af",
            bg="#ffffff"
        )
        self.lbl_total_user.pack(side="left")

        search_frame = tk.Frame(top_panel, bg="#ffffff")
        search_frame.pack(side="right")

        tk.Label(search_frame, text="Filtrar:", font=("Helvetica", 9, "bold"), bg="#ffffff", fg="#374151").pack(side="left", padx=(0, 5))
        self.txt_buscar_user = ttk.Entry(search_frame, width=20, font=("Helvetica", 9))
        self.txt_buscar_user.pack(side="left", padx=(0, 5))
        self.txt_buscar_user.bind("<KeyRelease>", lambda e: self._filtrar_usuarios())

        tk.Button(
            search_frame,
            text="Restablecer",
            font=("Helvetica", 8),
            bg="#e5e7eb",
            relief="flat",
            cursor="hand2",
            command=self._restablecer_usuarios
        ).pack(side="left")

        # Tabla de Solo Lectura
        table_container = tk.Frame(tab, bg="#ffffff")
        table_container.pack(fill="both", expand=True)

        cols_u = ("identificacion", "nombre", "correo", "rol")
        self.tree_user = ttk.Treeview(table_container, columns=cols_u, show="headings", selectmode="browse")

        self.tree_user.heading("identificacion", text="ID / Cédula")
        self.tree_user.heading("nombre", text="Nombre Completo")
        self.tree_user.heading("correo", text="Correo Electrónico")
        self.tree_user.heading("rol", text="Rol del Sistema")

        self.tree_user.column("identificacion", width=120, anchor="center")
        self.tree_user.column("nombre", width=240, anchor="w")
        self.tree_user.column("correo", width=240, anchor="w")
        self.tree_user.column("rol", width=140, anchor="center")

        scroll_y = ttk.Scrollbar(table_container, orient="vertical", command=self.tree_user.yview)
        self.tree_user.configure(yscrollcommand=scroll_y.set)

        self.tree_user.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

    # -------------------------------------------------------------------------
    # Métodos y Callbacks para Gestión de Usuarios (Semana 16)
    # -------------------------------------------------------------------------
    def _obtener_resumen_roles_texto(self) -> str:
        """Calcula y retorna un resumen resumido de usuarios por cada rol."""
        usuarios = self.servicio.listar_usuarios()
        admins = sum(1 for u in usuarios if u.es_administrador)
        empleados = sum(1 for u in usuarios if u.es_empleado)
        clientes = sum(1 for u in usuarios if u.es_cliente)
        return f"Admins: {admins} | Empleados: {empleados} | Clientes: {clientes}"

    def _actualizar_descripcion_rol(self, rol: str) -> None:
        """Actualiza la micro-tarjeta informativa según el rol seleccionado."""
        if not hasattr(self, "lbl_info_rol"):
            return

        descripciones = {
            "Administrador": "Rol Administrador: Acceso total al sistema y gestión de usuarios.",
            "Empleado": "Rol Empleado: Gestión de catálogo y registro de ventas.",
            "Cliente": "Rol Cliente: Comensal registrado en el restaurante."
        }
        texto = descripciones.get(rol, f"Rol seleccionado: {rol}")
        self.lbl_info_rol.config(text=texto)

    def _al_cambiar_rol_combobox(self, event: Optional[tk.Event] = None) -> None:
        """
        CALLBACK EVENTO VIRTUAL <<ComboboxSelected>>:
        Se dispara cuando el usuario cambia la opción del rol en el Combobox.
        Actualiza dinámicamente la descripción visual y la retroalimentación.
        """
        rol_seleccionado = self.combo_user_rol.get()
        self._actualizar_descripcion_rol(rol_seleccionado)
        self._mostrar_feedback_usuario(f"Rol seleccionado: {rol_seleccionado}", es_error=False)
        self._actualizar_estado_global(f"<<ComboboxSelected>>: Rol configurado a '{rol_seleccionado}'.")

    def _al_seleccionar_usuario_treeview(self, event: Optional[tk.Event] = None) -> None:
        """
        CALLBACK EVENTO VIRTUAL <<TreeviewSelect>>:
        Se dispara automáticamente cuando el usuario selecciona una fila en la tabla.
        
        Flujo de trabajo:
        1. Captura el identificador de la fila seleccionada.
        2. Consulta el objeto Usuario a través de RestauranteServicio (no lee contraseñas de la tabla).
        3. Carga automáticamente los datos en el formulario para edición o consulta.
        """
        sel = self.tree_user.selection()
        if not sel:
            return

        valores = self.tree_user.item(sel[0], "values")
        if not valores:
            return

        user_id = str(valores[0]).strip()

        # REQUISITO CLAVE: Consultar el objeto Usuario mediante el servicio
        usuario = self.servicio.buscar_usuario_por_id(user_id)
        if usuario is None:
            return

        # Cargar los datos en el formulario si el panel administrativo está presente
        if hasattr(self, "txt_user_id"):
            self.txt_user_id.delete(0, tk.END)
            self.txt_user_id.insert(0, usuario.identificacion)

            self.txt_user_nombre.delete(0, tk.END)
            self.txt_user_nombre.insert(0, usuario.nombre)

            self.txt_user_correo.delete(0, tk.END)
            self.txt_user_correo.insert(0, usuario.correo)

            if usuario.rol in self.combo_user_rol["values"]:
                self.combo_user_rol.set(usuario.rol)

            self._actualizar_descripcion_rol(usuario.rol)
            self._mostrar_feedback_usuario(
                f"Usuario '{usuario.nombre}' ({usuario.rol}) cargado al formulario.",
                es_error=False
            )
            self._actualizar_estado_global(
                f"<<TreeviewSelect>>: Datos de '{usuario.nombre}' (ID: {usuario.identificacion}) cargados."
            )

    def _al_presionar_enter_usuario(self, event: Optional[tk.Event] = None) -> str:
        """
        CALLBACK EVENTO DE TECLADO <Return>:
        Atajo para confirmar el registro de un usuario desde cualquier campo del formulario.
        REUTILIZA el método existente self._registrar_usuario() para evitar duplicar lógica.
        """
        self._registrar_usuario()
        return "break"  # Evita propagación de salto de línea en Tkinter

    def _al_presionar_escape_usuario(self, event: Optional[tk.Event] = None) -> str:
        """
        CALLBACK EVENTO DE TECLADO <Escape>:
        Atajo para limpiar el formulario, cancelar la selección en la tabla
        y devolver la interfaz a su estado inicial.
        REUTILIZA el método existente self._limpiar_formulario_usuario().
        """
        self._limpiar_formulario_usuario()
        return "break"

    def _mostrar_feedback_usuario(self, mensaje: str, es_error: bool = False) -> None:
        """Muestra retroalimentación visual en el formulario de usuarios."""
        if hasattr(self, "lbl_feedback_user"):
            color = "#dc2626" if es_error else "#16a34a"
            self.lbl_feedback_user.config(text=mensaje, fg=color)

    def _limpiar_formulario_usuario(self) -> None:
        """
        Limpia los campos del formulario, restablece el Combobox al rol Cliente,
        cancela la selección activa en el Treeview y devuelve el foco a la identificación.
        """
        if hasattr(self, "txt_user_id"):
            self.txt_user_id.delete(0, tk.END)
            self.txt_user_nombre.delete(0, tk.END)
            self.txt_user_correo.delete(0, tk.END)
            self.combo_user_rol.current(2)  # 'Cliente'
            self._actualizar_descripcion_rol("Cliente")
            self._mostrar_feedback_usuario("")
            self.txt_user_id.focus_set()

        # Deseleccionar fila activa en la tabla
        sel = self.tree_user.selection()
        if sel:
            self.tree_user.selection_remove(sel)

        self._actualizar_estado_global("<Escape>: Formulario de usuario restablecido y selección cancelada.")

    def _registrar_usuario(self) -> None:
        """
        Callback de registro de usuario asociado mediante command= al botón
        y reutilizado por el evento de teclado <Return>.
        Delega la validación de negocio y persistencia a RestauranteServicio.
        """
        if not hasattr(self, "txt_user_id"):
            return

        id_val = self.txt_user_id.get()
        nom_val = self.txt_user_nombre.get()
        cor_val = self.txt_user_correo.get()
        rol_val = self.combo_user_rol.get()

        exito, mensaje, nuevo_user = self.servicio.registrar_usuario(id_val, nom_val, cor_val, rol_val)
        if not exito:
            self._mostrar_feedback_usuario(mensaje, es_error=True)
            messagebox.showwarning("Atención al Registrar", mensaje, parent=self)
            return

        self._mostrar_feedback_usuario(mensaje, es_error=False)
        self._actualizar_estado_global(f"➕ {mensaje}")
        self._cargar_datos_usuarios()
        self._actualizar_combos_ventas()
        self._limpiar_formulario_usuario()
        messagebox.showinfo("Registro Exitoso", mensaje, parent=self)

    def _actualizar_usuario(self) -> None:
        """
        Callback de actualización de usuario asociado mediante command= al botón.
        Delega la actualización y persistencia a RestauranteServicio.
        """
        if not hasattr(self, "txt_user_id"):
            return

        id_val = self.txt_user_id.get()
        nom_val = self.txt_user_nombre.get()
        cor_val = self.txt_user_correo.get()
        rol_val = self.combo_user_rol.get()

        exito, mensaje, user_act = self.servicio.actualizar_usuario(id_val, nom_val, cor_val, rol_val)
        if not exito:
            self._mostrar_feedback_usuario(mensaje, es_error=True)
            messagebox.showwarning("Atención al Actualizar", mensaje, parent=self)
            return

        self._mostrar_feedback_usuario(mensaje, es_error=False)
        self._actualizar_estado_global(f"✏️ {mensaje}")
        self._cargar_datos_usuarios()
        self._actualizar_combos_ventas()
        messagebox.showinfo("Actualización Exitosa", mensaje, parent=self)

    def _eliminar_usuario(self) -> None:
        """
        Callback de eliminación de usuario asociado mediante command= al botón.
        Comprueba que la cuenta administrativa autenticada no sea eliminada por accidente,
        solicita confirmación y delega la operación a RestauranteServicio.
        """
        id_val = ""
        if hasattr(self, "txt_user_id"):
            id_val = self.txt_user_id.get().strip()

        # Si el campo está vacío, intentar obtener el ID de la fila seleccionada
        if not id_val:
            sel = self.tree_user.selection()
            if sel:
                valores = self.tree_user.item(sel[0], "values")
                if valores:
                    id_val = str(valores[0]).strip()

        if not id_val:
            self._mostrar_feedback_usuario("Indique o seleccione la identificación del usuario a eliminar.", es_error=True)
            messagebox.showinfo("Selección Requerida", "Seleccione un usuario de la tabla o ingrese su identificación.", parent=self)
            return

        # VERIFICACIÓN DE SEGURIDAD: Evitar eliminar la cuenta administrativa actualmente autenticada
        if id_val.upper() == self.usuario_actual.identificacion.upper():
            msg_bloqueo = "No es posible eliminar la cuenta administrativa con la que se encuentra actualmente autenticado."
            self._mostrar_feedback_usuario(msg_bloqueo, es_error=True)
            messagebox.showerror("Operación Bloqueada", msg_bloqueo, parent=self)
            return

        # Confirmación previa obligatoria antes de eliminar
        confirmacion = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar al usuario con identificación '{id_val}'?\n"
            "Esta operación eliminará permanentemente el registro de usuarios.json.",
            parent=self
        )
        if not confirmacion:
            return

        exito, mensaje = self.servicio.eliminar_usuario(
            id_val,
            id_usuario_autenticado=self.usuario_actual.identificacion
        )

        if not exito:
            self._mostrar_feedback_usuario(mensaje, es_error=True)
            messagebox.showerror("Error al Eliminar", mensaje, parent=self)
            return

        self._mostrar_feedback_usuario(mensaje, es_error=False)
        self._actualizar_estado_global(f"🗑️ {mensaje}")
        self._cargar_datos_usuarios()
        self._actualizar_combos_ventas()
        self._limpiar_formulario_usuario()
        messagebox.showinfo("Usuario Eliminado", mensaje, parent=self)

    def _cargar_datos_usuarios(self, lista: Optional[List[Usuario]] = None) -> None:
        """
        Carga o refresca los usuarios en el Treeview con formato estilizado
        y actualiza los indicadores numéricos del sistema.
        """
        for item in self.tree_user.get_children():
            self.tree_user.delete(item)

        usuarios = lista if lista is not None else self.servicio.listar_usuarios()
        for idx, u in enumerate(usuarios):
            tag_fila = "par" if idx % 2 == 0 else "impar"
            self.tree_user.insert(
                "",
                "end",
                values=(u.identificacion, u.nombre, u.correo, u.rol),
                tags=(tag_fila,)
            )

        self.tree_user.tag_configure("par", background="#ffffff")
        self.tree_user.tag_configure("impar", background="#f8fafc")

        if hasattr(self, "lbl_total_user"):
            self.lbl_total_user.config(text=f"Total Usuarios: {self.servicio.contar_usuarios()}")
        if hasattr(self, "lbl_resumen_roles"):
            self.lbl_resumen_roles.config(text=self._obtener_resumen_roles_texto())

    def _filtrar_usuarios(self) -> None:
        """Filtra usuarios según el texto ingresado en el buscador."""
        crit = self.txt_buscar_user.get()
        self._cargar_datos_usuarios(self.servicio.buscar_usuarios(crit))

    def _restablecer_usuarios(self) -> None:
        """Limpia el filtro de usuarios y recarga la lista completa."""
        self.txt_buscar_user.delete(0, tk.END)
        self._cargar_datos_usuarios()

    # =========================================================================
    # SECCIÓN 3: GESTIÓN DE VENTAS (SEMANA 15 - FUNDAMENTOS DE EVENTOS)
    # =========================================================================
    def _crear_tab_ventas(self) -> None:
        """
        Construye la sección funcional de Registro de Ventas.
        Demuestra el flujo fundamental de eventos:
          USUARIO -> ACCIÓN -> BOTÓN -> command= -> CALLBACK -> SERVICIO -> PERSISTENCIA -> UI
        """
        tab = tk.Frame(self.notebook, bg="#ffffff", padx=14, pady=12)
        self.notebook.add(tab, text=" 🛒 Registro de Ventas ")

        # --- A. Panel Superior: KPIs de Ventas y Recaudación ---
        panel_superior = tk.Frame(tab, bg="#ffffff")
        panel_superior.pack(fill="x", pady=(0, 10))

        stats_frame = tk.Frame(panel_superior, bg="#f8fafc", bd=1, relief="solid", padx=12, pady=6)
        stats_frame.pack(side="left")

        self.lbl_total_ventas = tk.Label(
            stats_frame,
            text=f"Total Ventas Registradas: {self.servicio.contar_ventas()}",
            font=("Helvetica", 9, "bold"),
            fg="#1e40af",
            bg="#f8fafc"
        )
        self.lbl_total_ventas.pack(side="left", padx=(0, 15))

        self.lbl_recaudacion_total = tk.Label(
            stats_frame,
            text=f"Recaudación en Caja: ${self.servicio.calcular_total_ventas():.2f}",
            font=("Helvetica", 9, "bold"),
            fg="#047857",
            bg="#f8fafc"
        )
        self.lbl_recaudacion_total.pack(side="left", padx=(0, 15))

        self.lbl_ventas_stock_info = tk.Label(
            stats_frame,
            text=f"Menú Activo: {self.servicio.contar_productos()} platillos",
            font=("Helvetica", 9),
            fg="#475569",
            bg="#f8fafc"
        )
        self.lbl_ventas_stock_info.pack(side="left")

        # Botón para refrescar selectores y catálogo
        tk.Button(
            panel_superior,
            text="🔄 Sincronizar",
            font=("Helvetica", 8),
            bg="#e5e7eb",
            relief="flat",
            cursor="hand2",
            command=self._sincronizar_todo
        ).pack(side="right")

        # --- B. Contenedor Central Dividido: Formulario (Izq) y Catálogo de Ventas (Der) ---
        panel_central = tk.Frame(tab, bg="#ffffff")
        panel_central.pack(fill="both", expand=True)

        # --- PANEL IZQUIERDO: Formulario de Registro de Venta ---
        self.frame_form_venta = ttk.LabelFrame(
            panel_central,
            text=" Registrar Nueva Venta ",
            padding=[14, 12]
        )
        self.frame_form_venta.pack(side="left", fill="y", padx=(0, 12))

        # 1. Selector de Usuario / Cliente
        tk.Label(
            self.frame_form_venta,
            text="Seleccionar Cliente / Usuario *:",
            font=("Helvetica", 9, "bold"),
            bg="#ffffff",
            anchor="w"
        ).pack(fill="x", pady=(2, 4))

        self.combo_venta_usuario = ttk.Combobox(
            self.frame_form_venta,
            state="readonly",
            width=34,
            font=("Helvetica", 9)
        )
        self.combo_venta_usuario.pack(fill="x", pady=(0, 12))

        # 2. Selector de Producto / Platillo
        tk.Label(
            self.frame_form_venta,
            text="Seleccionar Platillo / Producto *:",
            font=("Helvetica", 9, "bold"),
            bg="#ffffff",
            anchor="w"
        ).pack(fill="x", pady=(2, 4))

        self.combo_venta_producto = ttk.Combobox(
            self.frame_form_venta,
            state="readonly",
            width=34,
            font=("Helvetica", 9)
        )
        self.combo_venta_producto.pack(fill="x", pady=(0, 8))

        # Tarjeta explicativa pedagógica sobre el evento
        info_evento = tk.Frame(self.frame_form_venta, bg="#f1f5f9", bd=1, relief="solid", padx=8, pady=6)
        info_evento.pack(fill="x", pady=(4, 10))

        tk.Label(
            info_evento,
            text="📌 Fundamento de Eventos (Semana 15):",
            font=("Helvetica", 8, "bold"),
            fg="#1e3a8a",
            bg="#f1f5f9"
        ).pack(anchor="w")

        tk.Label(
            info_evento,
            text="Al pulsar 'Registrar Venta', command= dispara un callback que consulta RestauranteServicio, descuenta stock y persiste en ventas.json.",
            font=("Helvetica", 8),
            fg="#475569",
            bg="#f1f5f9",
            justify="left",
            wraplength=230
        ).pack(anchor="w")

        # Mensaje dinámico de retroalimentación
        self.lbl_feedback_venta = tk.Label(
            self.frame_form_venta,
            text="",
            font=("Helvetica", 8),
            bg="#ffffff",
            wraplength=240
        )
        self.lbl_feedback_venta.pack(fill="x", pady=(0, 8))

        # Botón de Acción Principal: REGISTRAR VENTA con command=
        # NOTA VITAL: Se pasa la referencia del callback 'self._al_registrar_venta' SIN paréntesis
        self.btn_registrar_venta = tk.Button(
            self.frame_form_venta,
            text="🛒 Registrar Venta",
            font=("Helvetica", 10, "bold"),
            bg="#2563eb",
            fg="#ffffff",
            activebackground="#1d4ed8",
            activeforeground="#ffffff",
            cursor="hand2",
            relief="flat",
            pady=8,
            command=self._al_registrar_venta
        )
        self.btn_registrar_venta.pack(fill="x", pady=(0, 6))

        # Botón para limpiar formulario de venta
        btn_limpiar_venta = tk.Button(
            self.frame_form_venta,
            text="🧹 Limpiar Selección",
            font=("Helvetica", 8),
            bg="#6b7280",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            pady=4,
            command=self._limpiar_formulario_venta
        )
        btn_limpiar_venta.pack(fill="x")

        # --- PANEL DERECHO: Catálogo Histórico de Ventas Registradas ---
        frame_historial = ttk.LabelFrame(
            panel_central,
            text=" Historial de Ventas Registradas ",
            padding=[8, 8]
        )
        frame_historial.pack(side="right", fill="both", expand=True)

        table_ventas_box = tk.Frame(frame_historial, bg="#ffffff")
        table_ventas_box.pack(fill="both", expand=True)

        cols_v = ("id", "fecha", "usuario", "producto", "total")
        self.tree_ventas = ttk.Treeview(
            table_ventas_box,
            columns=cols_v,
            show="headings",
            selectmode="browse"
        )

        self.tree_ventas.heading("id", text="ID Venta")
        self.tree_ventas.heading("fecha", text="Fecha y Hora")
        self.tree_ventas.heading("usuario", text="Cliente / Usuario")
        self.tree_ventas.heading("producto", text="Platillo Adquirido")
        self.tree_ventas.heading("total", text="Total ($)")

        self.tree_ventas.column("id", width=75, anchor="center")
        self.tree_ventas.column("fecha", width=145, anchor="center")
        self.tree_ventas.column("usuario", width=180, anchor="w")
        self.tree_ventas.column("producto", width=180, anchor="w")
        self.tree_ventas.column("total", width=85, anchor="e")

        scroll_ventas_y = ttk.Scrollbar(table_ventas_box, orient="vertical", command=self.tree_ventas.yview)
        self.tree_ventas.configure(yscrollcommand=scroll_ventas_y.set)

        self.tree_ventas.pack(side="left", fill="both", expand=True)
        scroll_ventas_y.pack(side="right", fill="y")

    # -------------------------------------------------------------------------
    # Métodos y Callbacks para Ventas (Semana 15)
    # -------------------------------------------------------------------------
    def _actualizar_combos_ventas(self) -> None:
        """
        Puebla los Combobox de usuarios y productos con datos formateados y legibles.
        Se ejecuta al inicializar y tras cada venta o registro de producto.
        """
        # 1. Usuarios: "{identificacion} - {nombre} ({rol})"
        usuarios = self.servicio.listar_usuarios()
        valores_usuarios = [f"{u.identificacion} - {u.nombre} ({u.rol})" for u in usuarios]
        self.combo_venta_usuario["values"] = valores_usuarios
        if valores_usuarios and not self.combo_venta_usuario.get():
            self.combo_venta_usuario.current(0)

        # 2. Productos: "{codigo} - {nombre} (${precio:.2f} | Stock: {stock})"
        productos = self.servicio.listar_productos()
        valores_productos = [
            f"{p.codigo} - {p.nombre} (${p.precio:.2f} | Stock: {p.stock})"
            for p in productos
        ]
        self.combo_venta_producto["values"] = valores_productos
        if valores_productos and not self.combo_venta_producto.get():
            self.combo_venta_producto.current(0)

    def _cargar_datos_ventas(self) -> None:
        """
        Carga y presenta la colección de ventas registradas en el Treeview.
        Actualiza además las métricas de recaudación y cantidad de ventas.
        """
        for item in self.tree_ventas.get_children():
            self.tree_ventas.delete(item)

        ventas = self.servicio.listar_ventas()
        for idx, venta in enumerate(ventas):
            detalle = self.servicio.obtener_detalle_venta(venta)
            tag = "par" if idx % 2 == 0 else "impar"

            self.tree_ventas.insert(
                "",
                "end",
                values=(
                    detalle["id_venta"],
                    detalle["fecha"],
                    f"{detalle['usuario_nombre']} ({detalle['usuario_id']})",
                    f"{detalle['producto_nombre']} ({detalle['producto_codigo']})",
                    f"${detalle['total']:.2f}"
                ),
                tags=(tag,)
            )

        self.tree_ventas.tag_configure("par", background="#ffffff")
        self.tree_ventas.tag_configure("impar", background="#f8fafc")

        # Actualizar indicadores KPI
        self.lbl_total_ventas.config(text=f"Total Ventas Registradas: {self.servicio.contar_ventas()}")
        self.lbl_recaudacion_total.config(text=f"Recaudación en Caja: ${self.servicio.calcular_total_ventas():.2f}")
        self.lbl_ventas_stock_info.config(text=f"Menú Activo: {self.servicio.contar_productos()} platillos")

    def _al_registrar_venta(self) -> None:
        """
        CALLBACK FUNDAMENTAL DE LA SEMANA 15:
        Asociado al botón mediante: command=self._al_registrar_venta
        
        Flujo de ejecución:
        1. Obtiene las selecciones del usuario desde la interfaz (Combobox).
        2. Valida la presencia de datos en la vista.
        3. Extrae los identificadores limpios (usuario_id, producto_codigo).
        4. Delega la validación de negocio, stock y persistencia a RestauranteServicio.
        5. Procesa la respuesta del servicio:
           - Si error: muestra alerta y feedback en rojo.
           - Si éxito: actualiza Treeview de ventas, refresca existencias en combos y catálogo,
             comunica el éxito en pantalla y en messagebox.
        """
        sel_usuario = self.combo_venta_usuario.get()
        sel_producto = self.combo_venta_producto.get()

        # Validación en la interfaz: comprobar selecciones
        if not sel_usuario or not sel_producto:
            msg_aviso = "Debe seleccionar un usuario y un producto para registrar la venta."
            self._mostrar_feedback_venta(msg_aviso, es_error=True)
            messagebox.showwarning("Selección Incompleta", msg_aviso, parent=self)
            return

        # Extracción de identificadores
        # Formato esperado: "1001 - Carlos Mendoza" -> "1001"
        usuario_id = sel_usuario.split(" - ")[0].strip()
        # Formato esperado: "P001 - Hamburguesa ... " -> "P001"
        producto_codigo = sel_producto.split(" - ")[0].strip()

        # Delegación exclusiva de la operación de venta al servicio de negocio
        exito, mensaje, nueva_venta = self.servicio.registrar_venta(usuario_id, producto_codigo)

        if not exito:
            # Respuesta visual ante fallo (ej. sin stock disponible)
            self._mostrar_feedback_venta(mensaje, es_error=True)
            messagebox.showerror("Error en Venta", mensaje, parent=self)
            return

        # Respuesta visual exitosa
        self._mostrar_feedback_venta(mensaje, es_error=False)
        self._actualizar_estado_global(f"🛒 {mensaje}")

        # Sincronización inmediata de la interfaz
        self._cargar_datos_ventas()
        self._actualizar_combos_ventas()
        self._cargar_datos_productos()  # Reflejar disminución de existencias en catálogo

        messagebox.showinfo("Venta Exitosa", mensaje, parent=self)

    def _mostrar_feedback_venta(self, mensaje: str, es_error: bool = False) -> None:
        """Presenta retroalimentación visual en la tarjeta de venta."""
        color = "#dc2626" if es_error else "#16a34a"
        self.lbl_feedback_venta.config(text=mensaje, fg=color)

    def _limpiar_formulario_venta(self) -> None:
        """Restablece los selectores del formulario de ventas."""
        self._actualizar_combos_ventas()
        self.lbl_feedback_venta.config(text="")

    def _sincronizar_todo(self) -> None:
        """Sincroniza y recarga todas las pestañas desde los datos en memoria."""
        self._cargar_datos_productos()
        self._cargar_datos_usuarios()
        self._cargar_datos_ventas()
        self._actualizar_combos_ventas()
        self._actualizar_estado_global("🔄 Datos sincronizados correctamente.")
