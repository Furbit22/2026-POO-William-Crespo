William Gynmar Crespo Farias
Programación Orientada a Objetos - Semana 9

# Sistema de Restaurante App (Semana 9)

Este es un sistema básico de consola para la administración de productos y usuarios de un restaurante, diseñado en Python. En esta semana, el proyecto ha evolucionado para incorporar y justificar el uso de las cuatro estructuras de datos principales de Python (`list`, `tuple`, `dict`, `set`), manteniendo una separación limpia de responsabilidades (Modelos, Servicios, Interfaz).

## Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

```text
restaurante_app/
├── data/
│   ├── productos.json
│   └── usuarios.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   └── usuario.py
├── servicios/
│   ├── __init__.py
│   └── restaurante.py
└── main.py
```

## Responsabilidad de los Componentes

*   **`data/`**: Carpeta destinada a la persistencia local de datos en formato JSON.
    *   **`productos.json`**: Almacena de forma permanente los productos registrados.
    *   **`usuarios.json`**: Almacena de forma permanente los usuarios registrados.
*   **`modelos/producto.py`**: Contiene la clase `Producto`, que representa las características individuales de cada producto (código, nombre, categoría y precio).
*   **`modelos/usuario.py`**: Contiene la clase `Usuario`, que representa la información general de una persona registrada en el sistema (identificación, nombre y correo).
*   **`servicios/restaurante.py`**: Contiene la clase `Restaurante`, encargada de administrar las colecciones mediante una estructura de diccionario centralizado, persistir la información en archivos JSON (lectura y escritura automática al registrar/modificar/eliminar), implementar la lógica de negocio (búsqueda, inserción, actualización, eliminación y validación de duplicados) y exponer los métodos necesarios a la interfaz de usuario.
*   **`main.py`**: Constituye el punto de arranque de la aplicación. Coordina el menú interactivo, valida la entrada de datos por consola e interactúa con el servicio `Restaurante` delegando el control de los datos.

## Aplicación de Estructuras de Datos

En este proyecto se integran de forma funcional y justificada las siguientes estructuras de datos:

1.  **Lista (`list`)**:
    *   **Ubicación**: En las colecciones dinámicas dentro del diccionario de datos de `servicios/restaurante.py` (`self._datos["productos"]` y `self._datos["usuarios"]`).
    *   **Justificación**: Se utiliza para mantener colecciones dinámicas y mutables de objetos (`Producto` y `Usuario`), lo que permite registrar, buscar, actualizar y eliminar elementos de forma flexible durante el ciclo de vida del programa.
2.  **Tupla (`tuple`)**:
    *   **Ubicación**: En `main.py` (`MENU_OPCIONES`).
    *   **Justificación**: Se emplea para representar información de configuración estable que no debe cambiar durante la ejecución del programa (los textos del menú principal). Su inmutabilidad previene alteraciones accidentales.
3.  **Diccionario (`dict`)**:
    *   **Ubicación**: 
        1. En `servicios/restaurante.py` (`self._datos`): Utilizado como la estructura central de almacenamiento del sistema para organizar y guardar las colecciones del programa bajo llaves descriptivas (`"productos"` y `"usuarios"`).
        2. En `main.py` (`acciones` dentro de `main()`): Mapea de forma directa la opción seleccionada por el usuario (clave string) con su función correspondiente (valor ejecutable). Esto optimiza el flujo del programa al evitar una estructura anidada de condicionales `if-elif-else`.
4.  **Conjunto (`set`)**:
    *   **Ubicación**: En `servicios/restaurante.py` (`obtener_categorias_unicas`).
    *   **Justificación**: Almacena y devuelve únicamente las categorías de productos registrados sin duplicados, aprovechando la propiedad de unicidad de los conjuntos de manera eficiente.

## Reflexión: Importancia de la Selección de Estructuras de Datos

La elección de la estructura de datos correcta es fundamental para el diseño de software eficiente y limpio:
*   El uso de **listas** es ideal cuando requerimos mantener el orden de inserción y mutabilidad para colecciones dinámicas.
*   Las **tuplas** aportan seguridad al código al garantizar que ciertos datos permanezcan constantes e inmutables (evitando bugs de efectos secundarios).
*   Los **diccionarios** permiten accesos directos de tipo O(1) mediante llaves únicas, facilitando el mapeo y simplificando el flujo lógico.
*   Los **conjuntos** nos ahorran la sobrecarga de escribir bucles manuales de filtrado para eliminar elementos duplicados, ya que gestionan la unicidad de forma nativa a nivel del motor de Python.

Elegir la estructura adecuada no solo mejora el rendimiento de ejecución, sino que también produce un código más legible, intuitivo y fácil de mantener.

## Instrucciones de Ejecución

Para ejecutar el programa, asegúrate de estar en el directorio `restaurante_app` (Semana 9) y ejecuta:

```bash
python main.py
```
