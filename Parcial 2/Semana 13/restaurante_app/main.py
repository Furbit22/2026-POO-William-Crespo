import os
import sys
import tkinter as tk
from tkinter import messagebox

# Asegurar que la ruta base de restaurante_app esté en el PYTHONPATH
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView
from modelos.usuario import Usuario

class AplicacionRestaurante:
    """
    Controlador principal de la aplicación con interfaz gráfica Tkinter.
    Orquesta la inicialización de los servicios, gestiona la ventana única
    y coordina la transición entre LoginView y MainView.
    """
    def __init__(self, root: tk.Tk, servicio: RestauranteServicio) -> None:
        self.root: tk.Tk = root
        self.servicio: RestauranteServicio = servicio
        self.vista_actual: tk.Widget = None

        self._configurar_ventana()

        # Contenedor central donde se alternan las vistas
        self.contenedor = tk.Frame(self.root, bg="#f3f4f6")
        self.contenedor.pack(fill="both", expand=True)

        # Iniciar mostrando la pantalla de acceso
        self.mostrar_login()

    def _configurar_ventana(self) -> None:
        """Configuración general de la ventana única de Tkinter."""
        self.root.title("Restaurante App - Sistema de Gestión")
        self.root.configure(bg="#f3f4f6")
        # Prevenir cierre abrupto sin confirmación si está en vista principal (opcional)
        self.root.protocol("WM_DELETE_WINDOW", self._al_cerrar_aplicacion)

    def _centrar_ventana(self, ancho: int, alto: int) -> None:
        """Centra la ventana en la pantalla del usuario."""
        self.root.update_idletasks()
        pantalla_ancho = self.root.winfo_screenwidth()
        pantalla_alto = self.root.winfo_screenheight()
        pos_x = max(0, (pantalla_ancho // 2) - (ancho // 2))
        pos_y = max(0, (pantalla_alto // 2) - (alto // 2))
        self.root.geometry(f"{ancho}x{alto}+{pos_x}+{pos_y}")
        self.root.minsize(ancho, alto)

    def mostrar_login(self) -> None:
        """
        Transición hacia la vista de acceso (LoginView).
        Destruye la vista previa y carga LoginView en la misma ventana.
        """
        if self.vista_actual is not None:
            self.vista_actual.destroy()

        self._centrar_ventana(460, 540)
        self.root.resizable(False, False)

        self.vista_actual = LoginView(
            parent=self.contenedor,
            servicio=self.servicio,
            on_login_success=self.mostrar_principal
        )
        self.vista_actual.pack(fill="both", expand=True)

    def mostrar_principal(self, usuario: Usuario) -> None:
        """
        Transición hacia la vista principal (MainView).
        Destruye LoginView y carga MainView dentro de la misma ventana.
        """
        if self.vista_actual is not None:
            self.vista_actual.destroy()

        self.root.resizable(True, True)
        self._centrar_ventana(900, 620)

        self.vista_actual = MainView(
            parent=self.contenedor,
            servicio=self.servicio,
            usuario_actual=usuario,
            on_logout=self._confirmar_cierre_sesion
        )
        self.vista_actual.pack(fill="both", expand=True)

    def _confirmar_cierre_sesion(self) -> None:
        """Solicita confirmación antes de cerrar la sesión activa."""
        respuesta = messagebox.askyesno(
            "Cerrar Sesión",
            "¿Está seguro de que desea cerrar la sesión actual y volver al login?",
            parent=self.root
        )
        if respuesta:
            self.mostrar_login()

    def _al_cerrar_aplicacion(self) -> None:
        """Manejador de cierre de la ventana única."""
        self.root.destroy()

def main() -> None:
    """Punto de entrada de la aplicación."""
    # Resolución de rutas hacia los archivos JSON en datos/
    ruta_datos = os.path.join(BASE_DIR, "datos")
    ruta_productos = os.path.join(ruta_datos, "productos.json")
    ruta_usuarios = os.path.join(ruta_datos, "usuarios.json")

    # Inicialización de la capa de servicios
    archivo_servicio = ArchivoServicio(ruta_productos, ruta_usuarios)
    restaurante_servicio = RestauranteServicio(archivo_servicio=archivo_servicio)

    # Inicialización de Tkinter (una sola instancia de Tk y un solo mainloop)
    root = tk.Tk()
    app = AplicacionRestaurante(root, restaurante_servicio)
    root.mainloop()

if __name__ == "__main__":
    main()
