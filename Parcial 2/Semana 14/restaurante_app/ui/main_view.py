import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, List, Optional
from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.restaurante_servicio import RestauranteServicio

class MainView(tk.Frame):
    """
    Panel principal de la aplicación gráfica restaurante_app para la Semana 14.
    Evoluciona la interfaz incorporando componentes y contenedores especializados
    (Notebook, LabelFrame, Entry, Combobox, Spinbox, Treeview, Scrollbars y Botones de acción con command=).
    
    Mantiene una estricta separación arquitectónica: toda operación y validación
    se delega a RestauranteServicio, sin interactuar directamente con archivos JSON.
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
        """Configura los estilos temáticos de ttk para contenedores, tablas y controles."""
        estilo = ttk.Style()
        estilo.theme_use("clam")

        # Contenedor de Pestañas (Notebook)
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

        # Contenedores LabelFrame
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
        """Construye la distribución de contenedores principales y áreas del sistema."""
        # 1. Barra Superior (Header)
        header = tk.Frame(self, bg="#1e293b", padx=20, pady=12)
        header.pack(fill="x", side="top")

        info_header = tk.Frame(header, bg="#1e293b")
        info_header.pack(side="left")

        lbl_app = tk.Label(
            info_header,
            text="🍽️ Restaurante App — Gestión Integral",
            font=("Helvetica", 14, "bold"),
            fg="#ffffff",
            bg="#1e293b"
        )
        lbl_app.pack(anchor="w")

        lbl_sesion = tk.Label(
            info_header,
            text=f"Sesión activa: {self.usuario_actual.nombre} | ID: {self.usuario_actual.identificacion}",
            font=("Helvetica", 9),
            fg="#94a3b8",
            bg="#1e293b"
        )
        lbl_sesion.pack(anchor="w")

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

        # 2. Contenedor de Navegación por Secciones (Notebook)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=12)

        # Secciones requeridas
        self._crear_tab_productos()
        self._crear_tab_usuarios()
        self._crear_tab_ventas_pendiente()

        # 3. Barra de Estado Inferior (Footer)
        self.footer = tk.Frame(self, bg="#e2e8f0", padx=15, pady=6)
        self.footer.pack(fill="x", side="bottom")

        self.lbl_footer_status = tk.Label(
            self.footer,
            text="Semana 14 — Componentes y Contenedores | Sistema listo y sincronizado.",
            font=("Helvetica", 8),
            fg="#475569",
            bg="#e2e8f0"
        )
        self.lbl_footer_status.pack(side="left")

    # =========================================================================
    # PESTAÑA: GESTIÓN DE PRODUCTOS (CRUD + FORMULARIO + TABLA)
    # =========================================================================
    def _crear_tab_productos(self) -> None:
        """
        Construye la sección de gestión de productos utilizando contenedores
        para separar el panel de métricas, el formulario y la tabla de catálogo.
        """
        tab = tk.Frame(self.notebook, bg="#ffffff", padx=14, pady=14)
        self.notebook.add(tab, text=" 📦 Gestión de Productos ")

        # --- A. Panel Superior: Métricas y Búsqueda ---
        panel_superior = tk.Frame(tab, bg="#ffffff")
        panel_superior.pack(fill="x", pady=(0, 10))

        # Tarjetas de estadísticas (Contenedor Frame)
        stats_frame = tk.Frame(panel_superior, bg="#f8fafc", bd=1, relief="solid", padx=12, pady=6)
        stats_frame.pack(side="left")

        self.lbl_total_prod = tk.Label(
            stats_frame,
            text=f"Total Platillos / Productos: {self.servicio.contar_productos()}",
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

        # Búsqueda rápida
        search_frame = tk.Frame(panel_superior, bg="#ffffff")
        search_frame.pack(side="right")

        tk.Label(
            search_frame,
            text="Filtrar:",
            font=("Helvetica", 9, "bold"),
            bg="#ffffff",
            fg="#374151"
        ).pack(side="left", padx=(0, 5))

        self.txt_buscar_prod = ttk.Entry(search_frame, width=20, font=("Helvetica", 9))
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

        # --- B. Contenedor Central Dividido: Formulario (Izq) y Catálogo (Der) ---
        panel_central = tk.Frame(tab, bg="#ffffff")
        panel_central.pack(fill="both", expand=True)

        # --- CONTENEDOR 1: Formulario de Operaciones (ttk.LabelFrame) ---
        self.frame_formulario = ttk.LabelFrame(
            panel_central,
            text=" Formulario de Producto ",
            padding=[14, 12]
        )
        self.frame_formulario.pack(side="left", fill="y", padx=(0, 12))

        # Grid interno del formulario para alineación precisa
        # Fila 0: Código y botón de consulta directa
        lbl_codigo = tk.Label(self.frame_formulario, text="Código del Producto *:", font=("Helvetica", 9, "bold"), bg="#ffffff", anchor="w")
        lbl_codigo.grid(row=0, column=0, sticky="w", pady=(2, 2))

        box_codigo = tk.Frame(self.frame_formulario, bg="#ffffff")
        box_codigo.grid(row=1, column=0, sticky="ew", pady=(0, 8))

        self.txt_codigo = ttk.Entry(box_codigo, width=15, font=("Helvetica", 9))
        self.txt_codigo.pack(side="left", fill="x", expand=True, padx=(0, 5))

        btn_consultar_codigo = tk.Button(
            box_codigo,
            text="🔍 Cargar",
            font=("Helvetica", 8, "bold"),
            bg="#3b82f6",
            fg="#ffffff",
            activebackground="#2563eb",
            activeforeground="#ffffff",
            cursor="hand2",
            relief="flat",
            padx=6,
            pady=2,
            command=self._cargar_producto_desde_formulario
        )
        btn_consultar_codigo.pack(side="right")

        # Fila 1: Nombre del Producto
        lbl_nombre = tk.Label(self.frame_formulario, text="Nombre del Platillo / Producto *:", font=("Helvetica", 9, "bold"), bg="#ffffff", anchor="w")
        lbl_nombre.grid(row=2, column=0, sticky="w", pady=(2, 2))

        self.txt_nombre = ttk.Entry(self.frame_formulario, width=32, font=("Helvetica", 9))
        self.txt_nombre.grid(row=3, column=0, sticky="ew", pady=(0, 8))

        # Fila 2: Categoría (ttk.Combobox)
        lbl_categoria = tk.Label(self.frame_formulario, text="Categoría *:", font=("Helvetica", 9, "bold"), bg="#ffffff", anchor="w")
        lbl_categoria.grid(row=4, column=0, sticky="w", pady=(2, 2))

        self.cmb_categoria = ttk.Combobox(
            self.frame_formulario,
            values=["Comida", "Bebida", "Acompañamiento", "Postre", "Cafetería"],
            font=("Helvetica", 9),
            state="normal"
        )
        self.cmb_categoria.set("Comida")
        self.cmb_categoria.grid(row=5, column=0, sticky="ew", pady=(0, 8))

        # Fila 3: Precio Unitario
        lbl_precio = tk.Label(self.frame_formulario, text="Precio Unitario ($) *:", font=("Helvetica", 9, "bold"), bg="#ffffff", anchor="w")
        lbl_precio.grid(row=6, column=0, sticky="w", pady=(2, 2))

        self.txt_precio = ttk.Entry(self.frame_formulario, width=32, font=("Helvetica", 9))
        self.txt_precio.grid(row=7, column=0, sticky="ew", pady=(0, 8))

        # Fila 4: Stock (ttk.Spinbox)
        lbl_stock = tk.Label(self.frame_formulario, text="Stock / Existencias *:", font=("Helvetica", 9, "bold"), bg="#ffffff", anchor="w")
        lbl_stock.grid(row=8, column=0, sticky="w", pady=(2, 2))

        self.spn_stock = ttk.Spinbox(
            self.frame_formulario,
            from_=0,
            to=9999,
            font=("Helvetica", 9),
            width=30
        )
        self.spn_stock.set(0)
        self.spn_stock.grid(row=9, column=0, sticky="ew", pady=(0, 10))

        # Mensaje de retroalimentación interna del formulario
        self.lbl_feedback_form = tk.Label(
            self.frame_formulario,
            text="Complete los campos para registrar o actualizar.",
            font=("Helvetica", 8, "italic"),
            bg="#ffffff",
            fg="#64748b",
            wraplength=250,
            justify="left"
        )
        self.lbl_feedback_form.grid(row=10, column=0, sticky="w", pady=(0, 10))

        # --- Contenedor de Botones de Acción (command=) ---
        frame_acciones = tk.Frame(self.frame_formulario, bg="#ffffff")
        frame_acciones.grid(row=11, column=0, sticky="ew", pady=(4, 0))

        # Fila 1 de botones: Registrar y Actualizar
        box_botones_1 = tk.Frame(frame_acciones, bg="#ffffff")
        box_botones_1.pack(fill="x", pady=(0, 5))

        btn_registrar = tk.Button(
            box_botones_1,
            text="➕ Registrar",
            font=("Helvetica", 9, "bold"),
            bg="#16a34a",
            fg="#ffffff",
            activebackground="#15803d",
            activeforeground="#ffffff",
            cursor="hand2",
            relief="flat",
            padx=10,
            pady=5,
            command=self._registrar_producto
        )
        btn_registrar.pack(side="left", fill="x", expand=True, padx=(0, 4))

        btn_actualizar = tk.Button(
            box_botones_1,
            text="✏️ Actualizar",
            font=("Helvetica", 9, "bold"),
            bg="#d97706",
            fg="#ffffff",
            activebackground="#b45309",
            activeforeground="#ffffff",
            cursor="hand2",
            relief="flat",
            padx=10,
            pady=5,
            command=self._actualizar_producto
        )
        btn_actualizar.pack(side="right", fill="x", expand=True, padx=(4, 0))

        # Fila 2 de botones: Eliminar y Limpiar
        box_botones_2 = tk.Frame(frame_acciones, bg="#ffffff")
        box_botones_2.pack(fill="x")

        btn_eliminar = tk.Button(
            box_botones_2,
            text="🗑️ Eliminar",
            font=("Helvetica", 9, "bold"),
            bg="#dc2626",
            fg="#ffffff",
            activebackground="#b91c1c",
            activeforeground="#ffffff",
            cursor="hand2",
            relief="flat",
            padx=10,
            pady=5,
            command=self._eliminar_producto
        )
        btn_eliminar.pack(side="left", fill="x", expand=True, padx=(0, 4))

        btn_limpiar = tk.Button(
            box_botones_2,
            text="🧹 Limpiar",
            font=("Helvetica", 9),
            bg="#6b7280",
            fg="#ffffff",
            activebackground="#4b5563",
            activeforeground="#ffffff",
            cursor="hand2",
            relief="flat",
            padx=10,
            pady=5,
            command=self._limpiar_formulario
        )
        btn_limpiar.pack(side="right", fill="x", expand=True, padx=(4, 0))

        # --- CONTENEDOR 2: Catálogo de Productos (ttk.LabelFrame) ---
        frame_catalogo = ttk.LabelFrame(
            panel_central,
            text=" Catálogo de Productos Registrados ",
            padding=[10, 10]
        )
        frame_catalogo.pack(side="right", fill="both", expand=True)

        # Contenedor para Treeview y Scrollbars
        table_container = tk.Frame(frame_catalogo, bg="#ffffff")
        table_container.pack(fill="both", expand=True)

        columnas = ("codigo", "nombre", "categoria", "precio", "stock")
        self.tree_prod = ttk.Treeview(
            table_container,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )

        self.tree_prod.heading("codigo", text="Código")
        self.tree_prod.heading("nombre", text="Nombre del Producto")
        self.tree_prod.heading("categoria", text="Categoría")
        self.tree_prod.heading("precio", text="Precio ($)")
        self.tree_prod.heading("stock", text="Stock")

        self.tree_prod.column("codigo", width=80, anchor="center")
        self.tree_prod.column("nombre", width=220, anchor="w")
        self.tree_prod.column("categoria", width=120, anchor="center")
        self.tree_prod.column("precio", width=95, anchor="e")
        self.tree_prod.column("stock", width=75, anchor="center")

        scroll_y = ttk.Scrollbar(table_container, orient="vertical", command=self.tree_prod.yview)
        self.tree_prod.configure(yscrollcommand=scroll_y.set)

        self.tree_prod.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

        # Barra de acciones inferiores para el catálogo (Cargar seleccionado y Eliminar seleccionado)
        acciones_catalogo = tk.Frame(frame_catalogo, bg="#ffffff", pady=6)
        acciones_catalogo.pack(fill="x")

        btn_cargar_seleccion = tk.Button(
            acciones_catalogo,
            text="📥 Cargar Seleccionado al Formulario",
            font=("Helvetica", 9, "bold"),
            bg="#2563eb",
            fg="#ffffff",
            activebackground="#1d4ed8",
            activeforeground="#ffffff",
            cursor="hand2",
            relief="flat",
            padx=12,
            pady=4,
            command=self._cargar_seleccion_tabla
        )
        btn_cargar_seleccion.pack(side="left", padx=(0, 8))

        btn_eliminar_seleccion = tk.Button(
            acciones_catalogo,
            text="🗑️ Eliminar Fila Seleccionada",
            font=("Helvetica", 9),
            bg="#fee2e2",
            fg="#991b1b",
            activebackground="#fecaca",
            activeforeground="#7f1d1d",
            cursor="hand2",
            relief="flat",
            padx=10,
            pady=4,
            command=self._eliminar_seleccion_tabla
        )
        btn_eliminar_seleccion.pack(side="left")

    # -------------------------------------------------------------------------
    # Operaciones del Formulario de Productos (Delegadas al Servicio)
    # -------------------------------------------------------------------------
    def _registrar_producto(self) -> None:
        """
        Captura los datos del formulario, delega la creación a RestauranteServicio
        y actualiza la interfaz si la operación es exitosa.
        """
        codigo = self.txt_codigo.get()
        nombre = self.txt_nombre.get()
        categoria = self.cmb_categoria.get()
        precio_str = self.txt_precio.get()
        stock_str = self.spn_stock.get()

        exito, mensaje, nuevo_prod = self.servicio.registrar_producto(
            codigo=codigo,
            nombre=nombre,
            categoria=categoria,
            precio=precio_str,
            stock=stock_str
        )

        if not exito:
            self._mostrar_feedback_form(mensaje, es_error=True)
            messagebox.showwarning("Atención al Registrar", mensaje, parent=self)
            return

        self._mostrar_feedback_form(mensaje, es_error=False)
        self._actualizar_estado_global(f"✅ {mensaje}")
        self._cargar_datos_productos()
        self._limpiar_formulario(conservar_mensaje=True)
        messagebox.showinfo("Registro Exitoso", mensaje, parent=self)

    def _cargar_producto_desde_formulario(self) -> None:
        """
        Consulta un producto por el código escrito en el campo 'Código'
        y carga sus datos en los demás campos del formulario.
        """
        codigo = self.txt_codigo.get().strip()
        if not codigo:
            self._mostrar_feedback_form("Por favor ingrese el código del producto a consultar.", es_error=True)
            messagebox.showwarning("Código Requerido", "Ingrese el código del producto que desea cargar.", parent=self)
            self.txt_codigo.focus_set()
            return

        producto = self.servicio.consultar_producto(codigo)
        if producto is None:
            msg = f"No existe ningún producto con el código '{codigo.upper()}'."
            self._mostrar_feedback_form(msg, es_error=True)
            messagebox.showwarning("No Encontrado", msg, parent=self)
            return

        self._poblar_formulario(producto)
        msg_exito = f"Producto '{producto.codigo}' cargado en el formulario."
        self._mostrar_feedback_form(msg_exito, es_error=False)
        self._actualizar_estado_global(f"🔍 {msg_exito}")

    def _actualizar_producto(self) -> None:
        """
        Toma los datos del formulario, solicita a RestauranteServicio la actualización
        del producto y refresca la tabla.
        """
        codigo = self.txt_codigo.get().strip()
        nombre = self.txt_nombre.get()
        categoria = self.cmb_categoria.get()
        precio_str = self.txt_precio.get()
        stock_str = self.spn_stock.get()

        if not codigo:
            self._mostrar_feedback_form("Indique el código del producto a actualizar.", es_error=True)
            messagebox.showwarning("Código Requerido", "Debe especificar el código del producto a actualizar.", parent=self)
            return

        exito, mensaje, prod_actualizado = self.servicio.actualizar_producto(
            codigo=codigo,
            nombre=nombre,
            categoria=categoria,
            precio=precio_str,
            stock=stock_str
        )

        if not exito:
            self._mostrar_feedback_form(mensaje, es_error=True)
            messagebox.showwarning("Atención al Actualizar", mensaje, parent=self)
            return

        self._mostrar_feedback_form(mensaje, es_error=False)
        self._actualizar_estado_global(f"✏️ {mensaje}")
        self._cargar_datos_productos()
        messagebox.showinfo("Actualización Exitosa", mensaje, parent=self)

    def _eliminar_producto(self) -> None:
        """
        Elimina el producto indicado en el campo código previa confirmación del usuario.
        """
        codigo = self.txt_codigo.get().strip()
        if not codigo:
            self._mostrar_feedback_form("Indique el código del producto que desea eliminar.", es_error=True)
            messagebox.showwarning("Código Requerido", "Debe escribir el código del producto a eliminar.", parent=self)
            return

        producto = self.servicio.consultar_producto(codigo)
        if producto is None:
            msg = f"No existe ningún producto con el código '{codigo.upper()}'."
            self._mostrar_feedback_form(msg, es_error=True)
            messagebox.showwarning("No Encontrado", msg, parent=self)
            return

        confirmar = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar el producto '{producto.nombre}' ({producto.codigo})?\n\nEsta acción actualizará permanentemente el catálogo del sistema.",
            parent=self
        )
        if not confirmar:
            return

        exito, mensaje = self.servicio.eliminar_producto(codigo)
        if not exito:
            self._mostrar_feedback_form(mensaje, es_error=True)
            messagebox.showerror("Error al Eliminar", mensaje, parent=self)
            return

        self._mostrar_feedback_form(mensaje, es_error=False)
        self._actualizar_estado_global(f"🗑️ {mensaje}")
        self._cargar_datos_productos()
        self._limpiar_formulario()
        messagebox.showinfo("Eliminación Exitosa", mensaje, parent=self)

    def _cargar_seleccion_tabla(self) -> None:
        """
        Carga los datos del producto seleccionado en la tabla hacia los campos del formulario.
        Cumple la interacción mediante botones con command= sin eventos bind complejos.
        """
        seleccion = self.tree_prod.selection()
        if not seleccion:
            messagebox.showinfo(
                "Seleccione un Producto",
                "Por favor haga clic sobre una fila del catálogo y luego presione este botón.",
                parent=self
            )
            return

        item_id = seleccion[0]
        valores = self.tree_prod.item(item_id, "values")
        if not valores:
            return

        codigo = valores[0]
        producto = self.servicio.consultar_producto(codigo)
        if producto:
            self._poblar_formulario(producto)
            msg = f"Producto '{producto.codigo}' cargado desde el catálogo."
            self._mostrar_feedback_form(msg, es_error=False)
            self._actualizar_estado_global(f"📥 {msg}")

    def _eliminar_seleccion_tabla(self) -> None:
        """
        Elimina el producto seleccionado directamente en la tabla tras confirmación.
        """
        seleccion = self.tree_prod.selection()
        if not seleccion:
            messagebox.showinfo(
                "Seleccione un Producto",
                "Seleccione el producto que desea eliminar en el catálogo.",
                parent=self
            )
            return

        item_id = seleccion[0]
        valores = self.tree_prod.item(item_id, "values")
        if not valores:
            return

        codigo = valores[0]
        nombre = valores[1]

        confirmar = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Desea eliminar el producto seleccionado: '{nombre}' ({codigo})?",
            parent=self
        )
        if not confirmar:
            return

        exito, mensaje = self.servicio.eliminar_producto(codigo)
        if exito:
            self._mostrar_feedback_form(mensaje, es_error=False)
            self._actualizar_estado_global(f"🗑️ {mensaje}")
            self._cargar_datos_productos()
            self._limpiar_formulario()
            messagebox.showinfo("Eliminación Exitosa", mensaje, parent=self)
        else:
            self._mostrar_feedback_form(mensaje, es_error=True)
            messagebox.showerror("Error al Eliminar", mensaje, parent=self)

    def _poblar_formulario(self, producto: Producto) -> None:
        """Puebla los campos de entrada del formulario con los atributos del objeto Producto."""
        self.txt_codigo.delete(0, tk.END)
        self.txt_codigo.insert(0, producto.codigo)

        self.txt_nombre.delete(0, tk.END)
        self.txt_nombre.insert(0, producto.nombre)

        self.cmb_categoria.set(producto.categoria)

        self.txt_precio.delete(0, tk.END)
        self.txt_precio.insert(0, f"{producto.precio:.2f}")

        self.spn_stock.delete(0, tk.END)
        self.spn_stock.insert(0, str(producto.stock))

    def _limpiar_formulario(self, conservar_mensaje: bool = False) -> None:
        """Restablece los campos de entrada del formulario a su estado predeterminado."""
        self.txt_codigo.delete(0, tk.END)
        self.txt_nombre.delete(0, tk.END)
        self.cmb_categoria.set("Comida")
        self.txt_precio.delete(0, tk.END)
        self.spn_stock.delete(0, tk.END)
        self.spn_stock.insert(0, "0")
        self.txt_codigo.focus_set()

        if not conservar_mensaje:
            self._mostrar_feedback_form("Formulario restablecido. Ingrese nuevos datos o consulte por código.", es_error=False)

    def _mostrar_feedback_form(self, mensaje: str, es_error: bool) -> None:
        """Muestra retroalimentación textual dentro del marco del formulario."""
        color = "#dc2626" if es_error else "#16a34a"
        self.lbl_feedback_form.config(text=mensaje, fg=color)

    def _actualizar_estado_global(self, mensaje: str) -> None:
        """Actualiza el texto de la barra de estado en el footer."""
        self.lbl_footer_status.config(text=mensaje)

    # -------------------------------------------------------------------------
    # Renderizado y Filtro de la Tabla de Productos
    # -------------------------------------------------------------------------
    def _cargar_datos_productos(self, lista: Optional[List[Producto]] = None) -> None:
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

        self.lbl_total_prod.config(text=f"Total Platillos / Productos: {self.servicio.contar_productos()}")
        self.lbl_stock_total.config(text=f"Existencias Totales: {self.servicio.obtener_stock_total()} u.")

    def _filtrar_productos(self) -> None:
        """Filtra productos en memoria a través del servicio."""
        termino = self.txt_buscar_prod.get()
        filtrados = self.servicio.buscar_productos(termino)
        self._cargar_datos_productos(filtrados)

    def _restablecer_productos(self) -> None:
        """Limpia el filtro de búsqueda y recarga todos los productos."""
        self.txt_buscar_prod.delete(0, tk.END)
        self._cargar_datos_productos()

    # =========================================================================
    # PESTAÑA: USUARIOS REGISTRADOS (CONSULTA)
    # =========================================================================
    def _crear_tab_usuarios(self) -> None:
        """Construye la vista de consulta de usuarios cargados mediante el servicio."""
        tab = tk.Frame(self.notebook, bg="#ffffff", padx=15, pady=15)
        self.notebook.add(tab, text=" 👥 Consulta de Usuarios ")

        # Panel de Resumen y Búsqueda
        top_panel = tk.Frame(tab, bg="#ffffff")
        top_panel.pack(fill="x", pady=(0, 10))

        stats_frame = tk.Frame(top_panel, bg="#f8fafc", bd=1, relief="solid", padx=12, pady=6)
        stats_frame.pack(side="left")

        self.lbl_total_user = tk.Label(
            stats_frame,
            text=f"Total Usuarios Registrados: {self.servicio.contar_usuarios()}",
            font=("Helvetica", 9, "bold"),
            fg="#1e40af",
            bg="#f8fafc"
        )
        self.lbl_total_user.pack(side="left")

        # Búsqueda de usuarios
        search_frame = tk.Frame(top_panel, bg="#ffffff")
        search_frame.pack(side="right")

        tk.Label(
            search_frame,
            text="Buscar Usuario:",
            font=("Helvetica", 9, "bold"),
            bg="#ffffff",
            fg="#374151"
        ).pack(side="left", padx=(0, 5))

        self.txt_buscar_user = ttk.Entry(search_frame, width=22, font=("Helvetica", 9))
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

        # Contenedor LabelFrame para la tabla de usuarios
        frame_tabla_usuarios = ttk.LabelFrame(
            tab,
            text=" Listado de Usuarios y Clientes del Restaurante ",
            padding=[10, 10]
        )
        frame_tabla_usuarios.pack(fill="both", expand=True)

        table_container = tk.Frame(frame_tabla_usuarios, bg="#ffffff")
        table_container.pack(fill="both", expand=True)

        columnas = ("identificacion", "nombre", "correo")
        self.tree_user = ttk.Treeview(table_container, columns=columnas, show="headings", selectmode="browse")

        self.tree_user.heading("identificacion", text="Cédula / Identificación")
        self.tree_user.heading("nombre", text="Nombre Completo")
        self.tree_user.heading("correo", text="Correo Electrónico")

        self.tree_user.column("identificacion", width=160, anchor="center")
        self.tree_user.column("nombre", width=280, anchor="w")
        self.tree_user.column("correo", width=280, anchor="w")

        scroll_y = ttk.Scrollbar(table_container, orient="vertical", command=self.tree_user.yview)
        self.tree_user.configure(yscrollcommand=scroll_y.set)

        self.tree_user.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

    def _cargar_datos_usuarios(self, lista: Optional[List[Usuario]] = None) -> None:
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

        self.lbl_total_user.config(text=f"Total Usuarios Registrados: {self.servicio.contar_usuarios()}")

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
    # PESTAÑA: VENTAS (MÓDULO FUTURO IDENTIFICADO)
    # =========================================================================
    def _crear_tab_ventas_pendiente(self) -> None:
        """
        Construye la sección informativa de Ventas, conservando la directriz
        de mantener identificadas las funcionalidades futuras sin desarrollarlas prematuramente.
        """
        tab = tk.Frame(self.notebook, bg="#ffffff", padx=20, pady=30)
        self.notebook.add(tab, text=" 🛒 Ventas (Próximamente) ")

        card = tk.Frame(tab, bg="#f8fafc", bd=1, relief="solid", padx=28, pady=25)
        card.place(relx=0.5, rely=0.5, anchor="center")

        lbl_icono = tk.Label(card, text="🛒", font=("Segoe UI Emoji", 42), bg="#f8fafc")
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
            text="ESTADO: FUNCIONALIDAD FUTURA EN DESARROLLO",
            font=("Helvetica", 8, "bold"),
            bg="#fef3c7",
            fg="#92400e",
            padx=8,
            pady=3
        )
        badge.pack(pady=(6, 15))

        texto_explicativo = (
            "En cumplimiento con el alcance pedagógico de la Semana 14, esta entrega se enfoca "
            "en el dominio de Componentes y Contenedores avanzados (LabelFrame, Treeview, Combobox, "
            "Spinbox, Formularios y operaciones CRUD de productos).\n\n"
            "El módulo transaccional de Ventas se integrará en las próximas semanas para:\n"
            "• Asociar ventas de usuarios y productos seleccionados.\n"
            "• Descontar existencias automáticamente tras cada orden.\n"
            "• Generar comprobantes y reportes de facturación."
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
