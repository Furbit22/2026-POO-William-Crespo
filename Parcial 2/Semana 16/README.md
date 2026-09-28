# 🍽️ Restaurante App — Semana 16
## Manejo de Eventos Aplicado a la Gestión de Usuarios en Tkinter

> **Asignatura:** Programación Orientada a Objetos (POO) — Python  
> **Nivel:** Semestre 2 | Parcial 2 — Semana 16  
> **Autor:** William Crespo  
> **Universidad Estatal Amazónica (UEA)**

---

## 📋 1. Propósito y Contexto de la Semana 16

La presente entrega representa la evolución progresiva de **`restaurante_app`**, consolidando la arquitectura modular en capas (Datos, Modelos, Servicios, Interfaz Gráfica y Punto de Entrada) e implementando de manera integral el **Manejo de Eventos en Tkinter**.

El núcleo temático de esta semana se enfoca en la **Gestión de Usuarios**, donde los eventos de teclado (`<Return>`, `<Escape>`), eventos virtuales de componentes `ttk` (`<<TreeviewSelect>>`, `<<ComboboxSelected>>`) y llamadas directas mediante `command=` interactúan armónicamente para brindar una experiencia de usuario fluida, reactiva y robusta.

### Flujo de Interacción y Manejo de Eventos
El sistema implementa estrictamente la cadena de responsabilidades requerida:
```
USUARIO (Interacción)
       ↓
EVENTO (Virtual o de Hardware)
       ↓
bind() / command=
       ↓
CALLBACK (Manejador en UI)
       ↓
RESTAURANTE_SERVICIO (Reglas de Negocio y Validación)
       ↓
ARCHIVO_SERVICIO (Persistencia en usuarios.json)
       ↓
RESPUESTA VISUAL (Treeview, Feedback y Barra de Estado)
```

---

## 🚀 2. Evolución del Proyecto (Semana 15 → Semana 16)

A partir de la base construida en la Semana 15 (inicio de sesión, catálogo de productos con stock y transacciones de ventas), la aplicación evoluciona en los siguientes aspectos:

1. **Evolución del Modelo `Usuario`:**
   - Incorporación del atributo obligatorio **`rol`** (`"Administrador"`, `"Empleado"`, `"Cliente"`).
   - Validaciones de dominio para evitar roles inválidos.
   - Propiedades de consulta rápida: `es_administrador`, `es_empleado`, `es_cliente`.
   - Método `actualizar_datos(nombre, correo, rol)`.
   - Persistencia completa en `usuarios.json` mediante `a_diccionario()` y `desde_diccionario()`.

2. **Control de Acceso y Gestión Basada en Roles:**
   - **Administrador:** Dispone del panel administrativo completo para registrar, consultar, actualizar y eliminar usuarios (`CRUD`), con atajos de teclado y selección interactiva.
   - **Empleado y Cliente:** Acceden a la aplicación para sus labores operativas (ventas y consulta de platillos), pero su acceso a la gestión de cuentas está **restringido**, visualizando un banner informativo de seguridad sin controles de modificación.

3. **Seguridad y Reglas de Negocio:**
   - **Protección contra auto-eliminación:** El administrador autenticado **no puede eliminar su propia cuenta en sesión**, evitando bloqueos accidentales.
   - **Protección del único administrador:** El sistema impide eliminar al único administrador activo del restaurante.
   - **Confirmación de eliminación:** Se requiere confirmación explícita (`messagebox.askyesno`) antes de borrar cualquier registro.
   - **Separación de responsabilidades:** La interfaz `main_view.py` **no lee ni escribe archivos JSON directamente**; delega todas las operaciones y validaciones a `RestauranteServicio`.

---

## ⌨️ 3. Eventos Implementados y Diferencia Pedagógica

La aplicación demuestra de forma práctica y justificada los distintos mecanismos de captura de interacción en Tkinter:

| Mecanismo / Evento | Tipo | Origen | Callback Asociado | Función en el Sistema |
|---|---|---|---|---|
| `<<TreeviewSelect>>` | Evento Virtual `ttk` | `self.tree_user.bind()` | `_al_seleccionar_usuario_treeview` | Al hacer clic sobre cualquier fila de la tabla, obtiene el identificador, consulta el objeto `Usuario` en `RestauranteServicio` y carga sus datos al formulario (sin almacenar contraseñas en la tabla). |
| `<Return>` | Evento de Teclado (Enter) | `Entry.bind("<Return>")` | `_al_presionar_enter_usuario` | Funciona como atajo de confirmación rápida desde cualquier campo del formulario. **Reutiliza** el método `_registrar_usuario()` sin duplicar lógica. |
| `<Escape>` | Evento de Teclado (Esc) | `Entry.bind("<Escape>")` y `Treeview.bind("<Escape>")` | `_al_presionar_escape_usuario` | Restablece los campos del formulario, deselecciona la fila activa en la tabla y devuelve la interfaz a su estado inicial reutilizando `_limpiar_formulario_usuario()`. |
| `<<ComboboxSelected>>` | Evento Virtual `ttk` | `self.combo_user_rol.bind()` | `_al_cambiar_rol_combobox` | Se dispara al cambiar la selección del rol en el Combobox, actualizando de inmediato una micro-tarjeta informativa con las funciones permitidas para dicho rol. |
| `command=` | Asignación Directa | Botones de la Vista | `_registrar_usuario`<br>`_actualizar_usuario`<br>`_eliminar_usuario`<br>`_limpiar_formulario_usuario` | Permite ejecutar las acciones principales mediante clic en los botones estilizados del formulario. |

### Diferencia conceptual: `bind()` vs. `command=`
- **`command=`**: Es una propiedad específica de los widgets tipo botón (`tk.Button`). Ejecuta un callback simple sin recibir metadatos del evento (no recibe parámetro `event`).
- **`bind()`**: Es un método universal de enlaces de eventos en Tkinter. Permite capturar eventos de hardware (pulsación de teclas como `<Return>` o `<Escape>`), eventos virtuales de componentes complejos (`<<TreeviewSelect>>`, `<<ComboboxSelected>>`) y eventos de ratón (`<Button-1>`, `<KeyRelease>`), inyectando automáticamente un objeto `tk.Event` al callback correspondiente.

---

## 📂 4. Estructura Modular del Proyecto

El proyecto mantiene la separación de responsabilidades trabajada a lo largo del semestre:

```text
Semana 16/
├── README.md                                  <- Documentación técnica integral de la Semana 16
└── restaurante_app/
    ├── assets/                                <- Recursos visuales obligatorios
    │   ├── icono_app.png                      <- Ícono oficial de la ventana principal
    │   ├── icono_chef.png                     <- Ícono auxiliar de perfil
    │   ├── logo_header.png                    <- Logotipo institucional para el encabezado
    │   ├── logo_login.png                     <- Logotipo para la pantalla de acceso
    │   └── logo_restaurante.png               <- Logotipo general del restaurante
    ├── datos/                                 <- Persistencia en archivos JSON
    │   ├── productos.json                     <- Catálogo de productos y existencias
    │   ├── usuarios.json                      <- Registro de usuarios con roles asignados
    │   └── ventas.json                        <- Historial de transacciones de venta
    ├── modelos/                               <- Entidades del dominio
    │   ├── __init__.py                        <- Exportación del paquete de modelos
    │   ├── producto.py                        <- Entidad Producto con validaciones y stock
    │   ├── usuario.py                         <- Entidad Usuario evolucionada con rol
    │   └── venta.py                           <- Entidad Venta comercial
    ├── servicios/                             <- Capa de lógica de negocio y persistencia
    │   ├── __init__.py                        <- Exportación del paquete de servicios
    │   ├── archivo_servicio.py                <- E/S segura de archivos JSON
    │   └── restaurante_servicio.py            <- Reglas de negocio, CRUD usuarios y ventas
    ├── ui/                                    <- Capa de presentación (Tkinter)
    │   ├── __init__.py                        <- Exportación del paquete UI
    │   ├── login_view.py                      <- Pantalla de acceso con atajo Enter y roles
    │   └── main_view.py                       <- Panel principal: Productos, Usuarios (Eventos) y Ventas
    ├── tests/                                 <- Pruebas unitarias y de integración
    │   ├── __init__.py
    │   ├── test_gestion_usuarios_semana16.py  <- 21 pruebas completas de eventos y roles
    │   └── test_integracion_semana15.py       <- 11 pruebas de regresión (ventas y stock)
    └── main.py                                <- Punto de entrada principal del sistema
```

---

## 👥 5. Credenciales de Prueba por Rol

Para verificar el control de acceso y el comportamiento según el rol, se encuentran disponibles las siguientes cuentas preconfiguradas:

| Rol | Usuario / ID | Contraseña | Privilegios en el Sistema |
|---|---|---|---|
| **Administrador** | `ADMIN` o `1005` (William Crespo) | `1234` | **Acceso total:** Gestión administrativa de usuarios (registro, edición, eliminación, atajos Enter/Esc, selección en Treeview), catálogo de productos y registro de ventas. |
| **Empleado** | `1002` (Ana Gómez) o `1004` (María Morales) | `1234` | **Operativo:** Registro de ventas, consulta de platillos y directorio de usuarios en modo solo lectura (gestión administrativa restringida). |
| **Cliente** | `1001` (Carlos Mendoza) o `1003` (Luis Ramírez) | `1234` | **Consulta:** Visualización de platillos, compras y directorio informativo de usuarios (gestión administrativa restringida). |

---

## ⚙️ 6. Instrucciones de Ejecución

### Prerrequisitos
- **Python 3.8** o superior instalado en el sistema.
- Biblioteca **Tkinter** (incluida por defecto en las distribuciones estándar de Python en Windows, macOS y Linux).

### Pasos para iniciar la aplicación:
1. Abra una terminal o consola de comandos en la carpeta del proyecto:
   ```powershell
   cd "Parcial 2/Semana 16/restaurante_app"
   ```
2. Ejecute el script principal:
   ```powershell
   python main.py
   ```
3. Inicie sesión con una cuenta de **Administrador** (`ADMIN` / `1234`) para comprobar la gestión completa de usuarios.
4. Pruebe las interacciones de eventos:
   - Haga clic sobre una fila del catálogo de usuarios y compruebe cómo `<<TreeviewSelect>>` carga sus datos al formulario.
   - Cambie el rol en el Combobox y observe la respuesta visual activada por `<<ComboboxSelected>>`.
   - Ingrese datos en el formulario y presione la tecla <kbd>Enter</kbd> para registrar al usuario mediante `<Return>`.
   - Presione la tecla <kbd>Esc</kbd> para limpiar el formulario y deseleccionar la tabla mediante `<Escape>`.
   - Modifique un registro y presione el botón `✏️ Actualizar` (`command=`).
   - Seleccione un usuario y presione `🗑️ Eliminar` para verificar la confirmación previa y comprobar que no puede eliminarse la cuenta activa.

---

## 🧪 7. Pruebas Automatizadas

El proyecto incluye una suite de pruebas automatizadas que certifica el correcto funcionamiento del modelo, las reglas de negocio, la persistencia y los eventos de la interfaz:

```powershell
python -m unittest tests/test_gestion_usuarios_semana16.py
```
**Resultado obtenido:**
```text
Ran 21 tests in 3.586s
OK
```

Adicionalmente, se puede ejecutar la suite de regresión de la Semana 15 para validar la interoperabilidad con el módulo de ventas y existencias:
```powershell
python -m unittest tests/test_integracion_semana15.py
```
**Resultado obtenido:**
```text
Ran 11 tests in 1.949s
OK
```

---

## 🌟 8. Criterios de Evaluación Cumplidos

- **1. Evolución, arquitectura y reutilización (2/2):** Continuidad desde la Semana 15 conservando la arquitectura en capas (`datos`, `modelos`, `servicios`, `ui`, `main.py`), sin duplicar lógica y delegando responsabilidades.
- **2. Gestión de usuarios y roles (2/2):** Implementación integral del CRUD de usuarios con roles `Administrador`, `Empleado` y `Cliente`, control de acceso y persistencia inmediata en `usuarios.json`.
- **3. Aplicación del manejo de eventos (2/2):** Integración rigurosa de `<<TreeviewSelect>>`, `<Return>`, `<Escape>`, `<<ComboboxSelected>>` y diferenciación con `command=`.
- **4. Interfaz y experiencia de usuario (2/2):** Diseño limpio, intuitivo y responsivo con componentes `ttk`, barra de estado dinámica y uso obligatorio de recursos gráficos en `assets/`.
- **5. Documentación del sistema (2/2):** `README.md` exhaustivo y detallado con explicación de arquitectura, roles, eventos, guía de ejecución y credenciales de prueba.
