# Explicación del Proyecto - Sistema de Restaurante

**Estudiante: William Crespo**  
**Materia: Programación Orientada a Objetos**

Este documento detalla la estructura y el funcionamiento del código desarrollado para el sistema de gestión del restaurante (`restaurante_app`), aplicando conceptos avanzados de Programación Orientada a Objetos en Python tales como constructores, encapsulamiento mediante decoradores `@property` y `@setter`, clases de datos (`@dataclass`) y arquitectura por capas.

---

## 1. Estructura del Proyecto

El sistema se organiza en una arquitectura modular por capas para separar las responsabilidades de los modelos de datos, la lógica del servicio y la interacción con el usuario:

- **`modelos/`**: Capa de datos y definición de entidades.
  - `producto.py`: Contiene la clase `Producto` con encapsulamiento tradicional.
  - `cliente.py`: Contiene la clase `Cliente` implementada como dataclass.
- **`servicios/`**: Capa de lógica de negocio.
  - `restaurante.py`: Gestiona las listas de productos y clientes (registro, listado y búsqueda).
- **`main.py`**: Interfaz de usuario por consola.

---

## 2. Explicación Detallada del Código

### Capa de Modelos (`modelos/`)

#### A. Clase `Producto` (`modelos/producto.py`)
Esta clase representa un artículo del menú del restaurante. Se diseñó usando el paradigma tradicional de POO en Python, asegurando el control y validación de los datos mediante propiedades y setters:

1. **Constructor (`__init__`)**:
   Inicializa los atributos del producto. En lugar de asignar directamente a variables privadas, utiliza las propiedades de asignación (`self.nombre = nombre`) para asegurar que cualquier dato que intente registrarse pase por las validaciones de los setters antes de ser almacenado.
2. **Propiedades (`@property` y `@setter`)**:
   - **`nombre`**: Cuenta con validación para evitar cadenas vacías o espacios en blanco únicamente (`strip()`).
   - **`categoria`**: Igualmente, se valida que pertenezca a una categoría no vacía.
   - **`precio`**: Se valida que sea un valor numérico real y que sea estrictamente mayor que cero (`> 0`). De lo contrario, se lanza una excepción de tipo `ValueError`.
   - **`disponible`**: Variable booleana para representar el estado del plato en el inventario.
3. **Método `mostrar_informacion`**:
   Retorna una cadena formateada de manera elegante mostrando el nombre, categoría, precio con formato monetario de dos decimales (`.2f`), y la disponibilidad actual.

#### B. Clase `Cliente` (`modelos/cliente.py`)
Representa a los clientes del restaurante. Para simplificar esta clase que solo almacena información y no requiere complejas validaciones en su estructura interna, se utiliza el decorador **`@dataclass`** de Python:
- **`@dataclass`**: Genera automáticamente métodos especiales como `__init__`, `__repr__` (para impresión en consola) y `__eq__` (comparaciones), reduciendo de manera drástica el código repetitivo (*boilerplate code*).
- Define los campos: `nombre`, `correo` e `id_cliente`.

---

### Capa de Servicios (`servicios/`)

#### Clase `Restaurante` (`servicios/restaurante.py`)
Actúa como el motor del sistema. Se encarga de administrar las bases de datos en memoria (listas de Python) para los productos y los clientes.

- **Atributos**: `_productos` y `_clientes` (listas privadas).
- **Funcionalidades de Productos**:
  - `registrar_producto(producto)`: Inserta un nuevo objeto `Producto` en la lista.
  - `listar_productos()`: Devuelve todos los productos almacenados.
  - `buscar_producto(nombre)`: Realiza una búsqueda insensible a mayúsculas/minúsculas y parcial. Si el término buscado es subcadena de algún producto, lo añade a los resultados de búsqueda.
- **Funcionalidades de Clientes**:
  - `registrar_cliente(cliente)`: Inserta una instancia de la dataclass `Cliente` en la lista.
  - `listar_clientes()`: Devuelve el listado completo de clientes.
  - `buscar_cliente(id_cliente)`: Busca de forma exacta mediante el identificador único `id_cliente`. Retorna la instancia de cliente o `None` en caso de no ser encontrado.

---

### Capa de Interfaz (`main.py`)

Es el punto de entrada de la aplicación. Gestiona el ciclo de vida del menú interactivo en consola mediante un bucle `while True`:
- **Menú Interactivo**: Ofrece las opciones obligatorias del 1 al 7.
- **Flujo de Datos**:
  1. El usuario ingresa datos por consola (`input()`).
  2. El sistema intenta crear las instancias correspondientes (`Producto` o `Cliente`).
  3. Si las validaciones fallan (por ejemplo, precio negativo o campos vacíos), captura los errores (`ValueError`) de forma controlada sin interrumpir la ejecución del programa.
  4. Si los datos son correctos, el objeto creado es enviado a la clase de servicio `Restaurante` para ser almacenado.
