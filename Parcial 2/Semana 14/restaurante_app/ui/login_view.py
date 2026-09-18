import tkinter as tk
from tkinter import ttk
from typing import Callable
from modelos.usuario import Usuario
from servicios.restaurante_servicio import RestauranteServicio

class LoginView(tk.Frame):
    """
    Vista gráfica de acceso (Login) para restaurante_app utilizando Tkinter.
    Presenta los campos de usuario y contraseña, delega la validación exclusivamente
    a RestauranteServicio y proporciona retroalimentación visual al usuario.
    """
    def __init__(
        self,
        parent: tk.Widget,
        servicio: RestauranteServicio,
        on_login_success: Callable[[Usuario], None]
    ) -> None:
        super().__init__(parent, bg="#f3f4f6")
        self.servicio: RestauranteServicio = servicio
        self.on_login_success: Callable[[Usuario], None] = on_login_success

        self._crear_interfaz()

    def _crear_interfaz(self) -> None:
        """Construye los componentes visuales de la pantalla de acceso."""
        # Contenedor central tipo tarjeta
        tarjeta = tk.Frame(self, bg="#ffffff", bd=1, relief="solid", padx=32, pady=32)
        tarjeta.place(relx=0.5, rely=0.5, anchor="center")

        # Encabezado con título e ícono
        lbl_icono = tk.Label(
            tarjeta,
            text="🍽️",
            font=("Segoe UI Emoji", 36),
            bg="#ffffff"
        )
        lbl_icono.pack(pady=(0, 5))

        lbl_titulo = tk.Label(
            tarjeta,
            text="Restaurante App",
            font=("Helvetica", 18, "bold"),
            fg="#1f2937",
            bg="#ffffff"
        )
        lbl_titulo.pack()

        lbl_subtitulo = tk.Label(
            tarjeta,
            text="Componentes y Contenedores — Semana 14 (POO)",
            font=("Helvetica", 9),
            fg="#6b7280",
            bg="#ffffff"
        )
        lbl_subtitulo.pack(pady=(2, 20))

        # Formulario de entrada
        form_frame = tk.Frame(tarjeta, bg="#ffffff")
        form_frame.pack(fill="x")

        # Campo: Usuario
        lbl_usuario = tk.Label(
            form_frame,
            text="Usuario / Identificación:",
            font=("Helvetica", 10, "bold"),
            fg="#374151",
            bg="#ffffff",
            anchor="w"
        )
        lbl_usuario.pack(fill="x", pady=(0, 4))

        self.txt_usuario = ttk.Entry(form_frame, font=("Helvetica", 11), width=28)
        self.txt_usuario.pack(fill="x", pady=(0, 14))
        self.txt_usuario.focus_set()

        # Campo: Contraseña
        lbl_contrasenia = tk.Label(
            form_frame,
            text="Contraseña:",
            font=("Helvetica", 10, "bold"),
            fg="#374151",
            bg="#ffffff",
            anchor="w"
        )
        lbl_contrasenia.pack(fill="x", pady=(0, 4))

        self.txt_contrasenia = ttk.Entry(
            form_frame,
            font=("Helvetica", 11),
            show="•",
            width=28
        )
        self.txt_contrasenia.pack(fill="x", pady=(0, 10))

        # Etiqueta de retroalimentación visual (mensajes de error/éxito)
        self.lbl_mensaje = tk.Label(
            tarjeta,
            text="",
            font=("Helvetica", 9),
            bg="#ffffff",
            fg="#ef4444",
            wraplength=280,
            justify="center"
        )
        self.lbl_mensaje.pack(fill="x", pady=(0, 15))

        # Botón de Inicio de Sesión
        btn_ingresar = tk.Button(
            tarjeta,
            text="Iniciar Sesión",
            font=("Helvetica", 11, "bold"),
            bg="#2563eb",
            fg="#ffffff",
            activebackground="#1d4ed8",
            activeforeground="#ffffff",
            cursor="hand2",
            relief="flat",
            pady=8,
            command=self._procesar_ingreso
        )
        btn_ingresar.pack(fill="x")

        # Vincular tecla Enter al formulario
        self.txt_usuario.bind("<Return>", lambda event: self._procesar_ingreso())
        self.txt_contrasenia.bind("<Return>", lambda event: self._procesar_ingreso())

        # Guía pedagógica inferior
        lbl_ayuda = tk.Label(
            tarjeta,
            text="Acceso Demo: admin / 1234  o  cédula de usuario / 1234",
            font=("Helvetica", 8, "italic"),
            fg="#9ca3af",
            bg="#ffffff"
        )
        lbl_ayuda.pack(pady=(15, 0))

    def _procesar_ingreso(self) -> None:
        """
        Ejecuta la validación de credenciales a través de RestauranteServicio
        y gestiona la retroalimentación en la interfaz gráfica.
        """
        usuario_texto = self.txt_usuario.get()
        contrasenia_texto = self.txt_contrasenia.get()

        # Delegar la validación al servicio
        exito, mensaje, usuario = self.servicio.validar_acceso(usuario_texto, contrasenia_texto)

        if not exito:
            self._mostrar_mensaje(mensaje, es_error=True)
            self.txt_contrasenia.delete(0, tk.END)
            self.txt_contrasenia.focus_set()
            return

        # Acceso concedido
        self._mostrar_mensaje(mensaje, es_error=False)
        self.update_idletasks()

        # Notificar al controlador principal para la transición de vista
        if self.on_login_success and usuario is not None:
            self.on_login_success(usuario)

    def _mostrar_mensaje(self, texto: str, es_error: bool = True) -> None:
        """Presenta retroalimentación visual al usuario en la pantalla de login."""
        color = "#ef4444" if es_error else "#16a34a"
        self.lbl_mensaje.config(text=texto, fg=color)
