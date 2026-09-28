import os
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
from modelos.usuario import Usuario
from servicios.restaurante_servicio import RestauranteServicio

class LoginView(tk.Frame):
    """
    Vista gráfica de acceso (Login) para restaurante_app.
    Presenta los campos de usuario y contraseña, incorpora el logotipo oficial
    desde la carpeta assets/, delega la validación exclusivamente a RestauranteServicio
    y proporciona retroalimentación visual al usuario.
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

        self.logo_img: Optional[tk.PhotoImage] = None
        self._cargar_recursos_assets()
        self._crear_interfaz()

    def _cargar_recursos_assets(self) -> None:
        """Carga el logotipo del restaurante desde la carpeta assets/."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_logo = os.path.join(base_dir, "assets", "logo_login.png")

        if not os.path.exists(ruta_logo):
            ruta_logo = os.path.join(base_dir, "assets", "logo_restaurante.png")

        if os.path.exists(ruta_logo):
            try:
                self.logo_img = tk.PhotoImage(file=ruta_logo)
            except Exception as e:
                print(f"[LoginView] No se pudo cargar el logo desde assets: {e}")
                self.logo_img = None

    def _crear_interfaz(self) -> None:
        """Construye los componentes visuales de la pantalla de acceso."""
        # Contenedor central tipo tarjeta
        tarjeta = tk.Frame(self, bg="#ffffff", bd=1, relief="solid", padx=32, pady=28)
        tarjeta.place(relx=0.5, rely=0.5, anchor="center")

        # 1. Encabezado con Logotipo desde assets/
        if self.logo_img is not None:
            lbl_logo = tk.Label(tarjeta, image=self.logo_img, bg="#ffffff")
            lbl_logo.pack(pady=(0, 6))
        else:
            lbl_icono = tk.Label(tarjeta, text="🍽️", font=("Segoe UI Emoji", 36), bg="#ffffff")
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
            text="Manejo de Eventos & Gestión de Usuarios — Semana 16 (POO)",
            font=("Helvetica", 9),
            fg="#6b7280",
            bg="#ffffff"
        )
        lbl_subtitulo.pack(pady=(2, 16))

        # 2. Formulario de entrada
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
        self.txt_usuario.pack(fill="x", pady=(0, 12))
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

        # Atajo de teclado: presionar Enter en los campos dispara el inicio de sesión
        self.txt_usuario.bind("<Return>", self._al_iniciar_sesion)
        self.txt_contrasenia.bind("<Return>", self._al_iniciar_sesion)

        # Etiqueta de retroalimentación visual (mensajes de error/éxito)
        self.lbl_mensaje = tk.Label(
            tarjeta,
            text="",
            font=("Helvetica", 9),
            bg="#ffffff",
            wraplength=280
        )
        self.lbl_mensaje.pack(fill="x", pady=(0, 8))

        # Botón de Inicio de Sesión
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
            command=self._al_iniciar_sesion
        )
        self.btn_ingresar.pack(fill="x", pady=(4, 12))

        # Cuadro de ayuda pedagógica de credenciales por rol (Semana 16)
        credenciales_frame = tk.Frame(
            tarjeta,
            bg="#f8fafc",
            bd=1,
            relief="solid",
            padx=10,
            pady=8
        )
        credenciales_frame.pack(fill="x")

        tk.Label(
            credenciales_frame,
            text="Credenciales de Prueba por Rol (Semana 16):",
            font=("Helvetica", 8, "bold"),
            fg="#1e40af",
            bg="#f8fafc"
        ).pack(anchor="w")

        info_credenciales = (
            "• Admin: 'ADMIN' o '1005' | Clave: '1234'\n"
            "• Empleado: '1002' (Ana) | Clave: '1234'\n"
            "• Cliente: '1001' (Carlos) | Clave: '1234'"
        )
        tk.Label(
            credenciales_frame,
            text=info_credenciales,
            font=("Helvetica", 8),
            fg="#4b5563",
            bg="#f8fafc",
            justify="left"
        ).pack(anchor="w")

    def _al_iniciar_sesion(self, event: Optional[tk.Event] = None) -> None:
        """
        Callback asociado al botón 'Iniciar Sesión' mediante command=
        y al evento <Return> mediante bind().
        Obtiene los datos de la vista y delega la validación exclusivamente al servicio.
        """
        user_val = self.txt_usuario.get()
        pass_val = self.txt_contrasenia.get()

        exito, mensaje, usuario = self.servicio.validar_acceso(user_val, pass_val)

        if exito and usuario is not None:
            self.lbl_mensaje.config(text=mensaje, fg="#16a34a")
            self.update_idletasks()
            self.after(200, lambda: self.on_login_success(usuario))
        else:
            self.lbl_mensaje.config(text=mensaje, fg="#dc2626")
            self.txt_contrasenia.delete(0, tk.END)
            self.txt_contrasenia.focus_set()
