# Sistema de Gestión de Restaurante - Organización Modular

**Estudiante:** WILLIAM GYNMAR CRESPO FARIAS  
**Asignatura:** Programación Orientada a Objetos  
**Semana:** Semana 5 - Taller Práctico  

---

## 📝 Descripción del Sistema
Este proyecto consiste en una aplicación de consola desarrollada en Python que simula un sistema básico de gestión para un restaurante ("El Buen Sabor"). El objetivo principal es demostrar la correcta aplicación de conceptos fundamentales de la Programación Orientada a Objetos (POO) y las buenas prácticas de diseño de software, tales como el uso de identificadores descriptivos, tipado explícito de datos, empaquetamiento modular e integración de componentes mediante importaciones limpias.

---

## 📁 Estructura del Proyecto
El sistema está rigurosamente estructurado de forma modular para separar las responsabilidades de almacenamiento de datos de la lógica de negocio, quedando distribuido de la siguiente manera:

- **`modelos/`**: Paquete encargado de definir las entidades de datos del negocio.
  - `__init__.py`: Archivo obligatorio para inicializar el paquete.
  - `producto.py`: Contiene la clase `Producto` para modelar los platos y bebidas (nombre, precio, stock, disponibilidad).
  - `cliente.py`: Contiene la clase `Cliente` para registrar los datos de los comensales (cédula, nombre completo, edad, estado de cliente frecuente).
- **`servicios/`**: Paquete encargado de la lógica operativa.
  - `__init__.py`: Archivo de inicialización del paquete.
  - `restaurante.py`: Contiene la clase `Restaurante`, la cual actúa como el núcleo del sistema, administrando las colecciones de datos.
- **`main.py`**: Punto de entrada y arranque principal de la aplicación. Se encarga de instanciar los objetos, poblar las listas y ejecutar la salida en consola.

---

## 📊 Tipos de Datos Utilizados
Para cumplir con los requerimientos técnicos de la rúbrica, se implementaron de manera explícita tanto tipos de datos básicos como compuestos:

1. **`str` (Cadena de texto)**: Utilizado para textos identificativos y descriptivos como `nombre`, `cedula` y `nombre_completo`.
2. **`float` (Decimal)**: Aplicado al atributo `precio` de los productos para manejar valores monetarios con precisión exacta.
3. **`int` (Entero)**: Utilizado para cuantificar variables discretas y contables como la `edad` de los clientes y el `stock` disponible en el inventario.
4. **`bool` (Booleano)**: Empleado para banderas de estado y validación lógica como `disponible` (si un plato está agotado o no) y `es_frecuente` (para la clasificación comercial del cliente).
5. **`list` (Tipo de dato compuesto)**: Implementado en el servicio principal (`lista_productos` y `lista_clientes`) para almacenar dinámicamente colecciones de objetos complejos e iterar sobre ellos.

---

## 🚀 Cómo Ejecutar el Programa

### Requisitos Previos
- Python 3.8 o superior instalado
- Acceso a terminal/consola del sistema operativo

### Pasos para Ejecutar
1. **Abre una terminal** y navega a la carpeta del proyecto:
   ```bash
   cd restaurante_app
   ```

2. **Ejecuta el programa principal**:
   ```bash
   python main.py
   ```

3. **Observa la salida en consola** que muestra todos los productos y clientes registrados de forma organizada.

---

## 📋 Clases del Sistema

### 1. **Clase Producto**
- **Ubicación**: `modelos/producto.py`
- **Atributos**:
  - `nombre: str` → Nombre del plato o bebida
  - `precio: float` → Precio en unidades monetarias
  - `stock: int` → Cantidad disponible en inventario
  - `disponible: bool` → Estado de disponibilidad
- **Métodos**:
  - `__init__(nombre, precio, stock, disponible)` → Constructor inicializador
  - `__str__()` → Retorna representación legible del producto

### 2. **Clase Cliente**
- **Ubicación**: `modelos/cliente.py`
- **Atributos**:
  - `cedula: str` → Número de identificación
  - `nombre_completo: str` → Nombre y apellido
  - `edad: int` → Edad en años
  - `es_frecuente: bool` → Clasificación como cliente frecuente
- **Métodos**:
  - `__init__(cedula, nombre_completo, edad, es_frecuente)` → Constructor inicializador
  - `__str__()` → Retorna representación legible del cliente

### 3. **Clase Restaurante**
- **Ubicación**: `servicios/restaurante.py`
- **Atributos**:
  - `nombre_restaurante: str` → Nombre del establecimiento
  - `lista_productos: list[Producto]` → Inventario de productos
  - `lista_clientes: list[Cliente]` → Base de datos de clientes
- **Métodos**:
  - `__init__(nombre_restaurante)` → Constructor inicializador
  - `agregar_producto(producto)` → Añade un producto al inventario
  - `registrar_cliente(cliente)` → Registra un nuevo cliente
  - `mostrar_informacion_sistema()` → Imprime toda la información en consola

---

## 📊 Datos de Ejemplo

El programa incluye datos ficticios de prueba:

| Producto | Precio | Stock | Estado |
|----------|--------|-------|--------|
| Ceviche Peruano | $18.50 | 25 | Disponible |
| Chicha Morada | $5.00 | 40 | Disponible |

| Cédula | Cliente | Edad | Tipo |
|--------|---------|------|------|
| 1023456789 | Carlos Mendoza García | 35 | Frecuente |
| 1087654321 | María López Rodríguez | 28 | Nuevo |

---

## 💡 Reflexión sobre las Buenas Prácticas en Python

La realización de este taller práctico destaca tres pilares fundamentales para el desarrollo de software profesional:

* **Identificadores descriptivos y Convenciones (`PascalCase` / `snake_case`)**: El uso de nombres claros para variables, métodos y clases elimina la ambigüedad. Permite que el código sea autoexplicativo, facilitando que cualquier otro programador (o nosotros mismos en el futuro) entienda la utilidad de cada componente sin necesidad de descifrar abreviaturas confusas.
* **Tipado de datos correcto**: Definir explícitamente qué tipo de dato requiere cada atributo (mediante *type hinting*) previene errores en tiempo de ejecución, optimiza el comportamiento del entorno de desarrollo (como el autocompletado en PyCharm) y restringe el flujo del programa a operaciones seguras y coherentes.
* **Modularización y Colecciones (`list`)**: Agrupar el código en archivos y paquetes específicos según su responsabilidad evita que el software se convierta en un script masivo e imposible de mantener. Además, el uso de tipos de datos compuestos como las listas (`list[Objeto]`) nos dota de la flexibilidad necesaria para centralizar, almacenar y procesar múltiples registros dinámicamente, lo cual constituye el cimiento de cualquier sistema de información escalable.

---

## 🎯 Conceptos de POO Aplicados

✅ **Encapsulamiento**: Los datos se organizan dentro de clases específicas  
✅ **Abstracción**: Cada clase representa una entidad del negocio  
✅ **Métodos especiales**: Uso de `__init__` y `__str__` para inicialización y representación  
✅ **Importaciones modulares**: Separación clara entre modelos y servicios  
✅ **Type Hints**: Anotaciones de tipo para mayor seguridad  
✅ **Colecciones dinámicas**: Uso de listas para gestionar múltiples objetos  

---

## 📝 Autor
**WILLIAM GYNMAR CRESPO FARIAS**  
Programación Orientada a Objetos - Semana 5  
Universidad EAN - 2026