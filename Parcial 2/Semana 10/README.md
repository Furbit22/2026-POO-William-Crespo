William Gynmar Crespo Farias
Programación Orientada a Objetos - Semana 10

# Sistema de Restaurante App (Semana 10)

Este es un sistema básico de consola para la administración de productos y usuarios de un restaurante, diseñado en Python. En esta semana, el proyecto ha evolucionado para incorporar **persistencia de datos mediante archivos JSON**, permitiendo que la información de los productos y usuarios se conserve cuando la aplicación se cierra y se recupere automáticamente al iniciar una nueva ejecución.

## Estructura del Proyecto

El proyecto está organizado bajo la estructura modular de capas requerida:

```text
restaurante_app/
├── datos/
│   ├── productos.json
│   └── usuarios.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   └── usuario.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante.py
├── main.py
└── README.md
```

## Responsabilidad de los Componentes

*   **`datos/`**: Carpeta utilizada exclusivamente para el almacenamiento persistente de archivos JSON. No forma parte de la lógica del sistema.
    *   **`productos.json`**: Almacena los productos en formato JSON (como una lista de diccionarios).
    *   **`usuarios.json`**: Almacena los usuarios en formato JSON (como una lista de diccionarios).
*   **`modelos/producto.py`**: Contiene la clase `Producto` con sus validaciones internas (evitando valores vacíos y precios negativos) y provee los métodos `a_diccionario()` y `desde_diccionario()` para facilitar la serialización a JSON.
*   **`modelos/usuario.py`**: Contiene la clase `Usuario` con sus validaciones de campos y formato de correo electrónico, además de los métodos `a_diccionario()` y `desde_diccionario()`.
*   **`servicios/archivo_servicio.py`**: Concentra de forma centralizada la lectura y escritura de los archivos JSON. Utiliza `with open()` y codificación `utf-8`. Implementa el control robusto de excepciones.
*   **`servicios/restaurante.py`**: Representa la lógica de negocio del restaurante. Gestiona las colecciones en memoria de productos y usuarios, las búsquedas, registros, actualizaciones y eliminaciones. Está completamente desacoplado del acceso directo a archivos.
*   **`main.py`**: Punto de inicio de la aplicación. Crea el servicio `ArchivoServicio`, carga la base de datos al arrancar, instancia el servicio `Restaurante` con los datos recuperados, coordina el menú interactivo y solicita al servicio de archivos guardar los datos tras cada operación de modificación.

---

## Flujo de Datos

### Flujo de Carga al Iniciar
1. `main.py` crea la instancia de `ArchivoServicio`.
2. Se intenta leer `datos/productos.json` y `datos/usuarios.json`.
3. `json.load()` recupera los datos guardados en una estructura nativa de Python.
4. Cada registro se valida estructuralmente. Si faltan datos (`KeyError`) o no cumplen las validaciones del constructor (`ValueError`), el elemento defectuoso es omitido de forma controlada imprimiendo una advertencia, permitiendo cargar el resto.
5. Los objetos válidos de tipo `Producto` y `Usuario` reconstruidos se pasan al constructor del servicio `Restaurante`.
6. El menú de consola opera con los objetos cargados en memoria.

### Flujo de Guardado al Modificar
1. El usuario registra, actualiza o elimina un elemento a través del menú.
2. `main.py` delega la operación al servicio `Restaurante`.
3. `Restaurante` realiza la operación sobre las listas en memoria.
4. Si la operación es exitosa, `main.py` invoca al método de guardado correspondiente de `ArchivoServicio`.
5. `ArchivoServicio` obtiene los objetos de `Restaurante`, los convierte a diccionarios mediante `a_diccionario()` y los serializa a archivos JSON usando `json.dump()`.

---

## Excepciones Controladas

El acceso a archivos y la reconstrucción de objetos manejan de forma explícita las siguientes excepciones:
1.  **`FileNotFoundError`**: Si los archivos JSON no existen todavía (por ejemplo, en la primera ejecución), el programa arranca con listas vacías en lugar de detenerse.
2.  **`json.JSONDecodeError`**: Se captura si el archivo está dañado o no es un formato JSON legible, notificando al usuario e iniciando con datos vacíos para no romper la ejecución.
3.  **`PermissionError`**: Si el sistema operativo deniega el permiso para leer o escribir en las rutas especificadas, se emite un mensaje descriptivo controlado sin colapsar el programa.
4.  **`KeyError`**: Se captura al reconstruir los objetos si falta algún campo obligatorio esperado dentro de los diccionarios almacenados.
5.  **`ValueError`**: Se valida tanto la conversión de precios a tipo decimal (`float`), precios negativos y el formato de datos de las clases `Producto` y `Usuario`.

---

## Instrucciones de Ejecución

Para iniciar el programa, sitúate en el directorio de la aplicación y ejecuta:

```bash
python main.py
```

---

## Comprobación de Persistencia Real

La persistencia del programa fue probada con los siguientes pasos:
1. **Ejecución Inicial**: Se inició la aplicación sin existir los archivos JSON en `datos/`. El programa arrancó correctamente con 0 productos y 0 usuarios.
2. **Registro de Datos**: Se registraron 2 productos ("P001", Hamburguesa, $8.50) y ("P002", Refresco, $1.50) y 1 usuario ("U001", William, william@mail.com).
3. **Validación de Archivos**: Se constató la creación automática de la carpeta `datos/` y los archivos `productos.json` y `usuarios.json` con los contenidos correspondientes en formato de lista de diccionarios.
4. **Prueba de Persistencia**: Se cerró la aplicación seleccionando la opción 9.
5. **Reinicio**: Se ejecutó `python main.py` nuevamente. Al seleccionar la opción de listar productos y listar usuarios, se comprobó que los registros anteriores se cargaron correctamente.
6. **Modificación y Eliminación**: Se actualizó el precio del producto "P001" a $9.00 y se eliminó "P002". Se cerró el programa y, al volver a abrirlo, se validó que los cambios persistieran en el archivo y en la interfaz.
