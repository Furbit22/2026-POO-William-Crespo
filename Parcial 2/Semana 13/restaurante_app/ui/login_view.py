import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
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
        tarjeta = tk.Frame(self, bg="#ffffff", bd=1, relief="solid", padx=30, pady=30)
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
            text="Simulación de Acceso - Semana 13 (POO)",
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
            fg="#dc2626",
            bg="#ffffff",
            wraplength=260,
            justify="center"
        )
        self.lbl_mensaje.pack(pady=(0, 12))

        # Botón de Ingreso
        self.btn_ingresar = tk.Button(
            tarjeta,
            text="Iniciar Sesión",
            font=("Helvetica", 10, "bold"),
            bg="#2563eb",
            fg="#ffffff",
            activebackground="#1d4ed8",
            activeforeground="#ffffff",
            cursor="hand2",
            relief="flat",
            pady=8,
            command=self._procesar_ingreso
        )
        self.btn_ingresar.pack(fill="x")

        # Permitir enviar formulario con la tecla Enter
        self.txt_usuario.bind("<Return>", lambda event: self._procesar_ingreso())
        self.txt_contrasenia.bind("<Return>", lambda event: self._procesar_ingreso())

        # Panel informativo pedagógico
        info_frame = tk.Frame(tarjeta, bg="#f9fafb", bd=1, relief="groove", padx=10, pady=8)
        info_frame.pack(fill="x", pady=(20, 0))

        lbl_guia_titulo = tk.Label(
            info_frame,
            text="💡 Credenciales de acceso:",
            font=("Helvetica", 8, "bold"),
            fg="#4b5563",
            bg="#f9fafb",
            anchor="w"
        )
        lbl_guia_titulo.pack(fill="x")

        lbl_guia_detalle = tk.Label(
            info_frame,
            text="• Usuario: admin\n• Contraseña: 1234",
            font=("Helvetica", 8),
            fg="#6b7280",
            bg="#f9fafb",
            justify="left",
            anchor="w"
        )
        lbl_guia_detalle.pack(fill="x", pady=(2, 0))

    def _procesar_ingreso(self) -> None:
        """
        Gestiona la acción de login delegando la validación a RestauranteServicio.
        Actualiza los mensajes visuales según el resultado.
        """
        usuario_input = self.txt_usuario.get()
        contrasenia_input = self.txt_contrasenia.get()

        # Delegación obligatoria al servicio de negocio
        exito, mensaje, usuario = self.servicio.validar_acceso(usuario_input, contrasenia_input)

        if not exito:
            # Respuesta visual ante error o campos vacíos
            self.lbl_mensaje.config(text=mensaje, fg="#dc2626")
            self.txt_contrasenia.delete(0, tk.END)
            self.txt_contrasenia.focus_set()
        else:
            # Respuesta visual de éxito y transición a vista principal
            self.lbl_mensaje.config(text=mensaje, fg="#16a34a")
            self.after(300, lambda: self._completar_login(usuario))

    def _completar_login(self, usuario: Optional[Usuario]) -> None:
        """Limpia el mensaje y activa la transición en el controlador principal."""
        self.lbl_mensaje.config(text="")
        if usuario is not None and self.on_login_success:
            self.on_login_success(usuario)

    def limpiar_campos(self) -> None:
        """Restablece los campos de texto al cerrar sesión."""
        self.txt_usuario.delete(0, tk.END)
        self.txt_contrasenia.delete(0, tk.END)
        self.lbl_mensaje.config(text="")
        self.txt_usuario.focus_set()
