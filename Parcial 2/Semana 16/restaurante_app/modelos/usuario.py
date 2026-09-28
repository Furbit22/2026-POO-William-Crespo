from typing import Any, Dict, Tuple

ROLES_PERMITIDOS: Tuple[str, ...] = ("Administrador", "Empleado", "Cliente")

class Usuario:
    """
    Representa a un usuario dentro del sistema del restaurante para la Semana 16.
    Evolución respecto a la Semana 15: incorpora el atributo 'rol' para diferenciar
    entre 'Administrador', 'Empleado' y 'Cliente', permitiendo control de acceso
    y gestión administrativa basada en eventos.
    """
    def __init__(
        self,
        identificacion: str,
        nombre: str,
        correo: str,
        rol: str = "Cliente"
    ) -> None:
        if not isinstance(identificacion, str) or not identificacion.strip():
            raise ValueError("La identificación del usuario no puede estar vacía.")
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del usuario no puede estar vacío.")
        if not isinstance(correo, str) or "@" not in correo or not correo.strip():
            raise ValueError("El correo electrónico del usuario debe ser válido (contener '@').")

        rol_limpio = str(rol).strip().capitalize() if isinstance(rol, str) else ""
        # Normalizar casos como "administrador" -> "Administrador"
        rol_normalizado = None
        for r in ROLES_PERMITIDOS:
            if r.lower() == str(rol).strip().lower():
                rol_normalizado = r
                break

        if rol_normalizado is None:
            roles_validos_str = ", ".join(ROLES_PERMITIDOS)
            raise ValueError(
                f"El rol '{rol}' no es válido. Los roles permitidos son: {roles_validos_str}."
            )

        self.identificacion: str = identificacion.strip()
        self.nombre: str = nombre.strip()
        self.correo: str = correo.strip()
        self.rol: str = rol_normalizado

    @property
    def es_administrador(self) -> bool:
        """Indica si el usuario cuenta con el rol de Administrador."""
        return self.rol == "Administrador"

    @property
    def es_empleado(self) -> bool:
        """Indica si el usuario cuenta con el rol de Empleado."""
        return self.rol == "Empleado"

    @property
    def es_cliente(self) -> bool:
        """Indica si el usuario cuenta con el rol de Cliente."""
        return self.rol == "Cliente"

    def actualizar_datos(self, nombre: str, correo: str, rol: str) -> None:
        """
        Actualiza los datos del usuario validando la integridad de cada atributo.
        """
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del usuario no puede estar vacío.")
        if not isinstance(correo, str) or "@" not in correo or not correo.strip():
            raise ValueError("El correo electrónico debe ser válido (contener '@').")

        rol_normalizado = None
        for r in ROLES_PERMITIDOS:
            if r.lower() == str(rol).strip().lower():
                rol_normalizado = r
                break

        if rol_normalizado is None:
            roles_validos_str = ", ".join(ROLES_PERMITIDOS)
            raise ValueError(
                f"El rol '{rol}' no es válido. Los roles permitidos son: {roles_validos_str}."
            )

        self.nombre = nombre.strip()
        self.correo = correo.strip()
        self.rol = rol_normalizado

    def mostrar_informacion(self) -> str:
        """Retorna una representación textual con la información completa del usuario."""
        return f"ID: {self.identificacion} | Nombre: {self.nombre} | Correo: {self.correo} | Rol: {self.rol}"

    def a_diccionario(self) -> Dict[str, Any]:
        """Serializa la entidad Usuario a un formato de diccionario para persistencia JSON."""
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
            "rol": self.rol
        }

    @classmethod
    def desde_diccionario(cls, datos: Dict[str, Any]) -> "Usuario":
        """Reconstruye una instancia de Usuario a partir de un diccionario."""
        identificacion: str = datos["identificacion"]
        nombre: str = datos["nombre"]
        correo: str = datos["correo"]
        # Compatibilidad hacia atrás: si no existe el campo rol, asignar Administrador si ID es ADMIN, de lo contrario Cliente
        rol: str = datos.get("rol", "Administrador" if str(identificacion).upper() == "ADMIN" else "Cliente")
        return cls(identificacion, nombre, correo, rol)

