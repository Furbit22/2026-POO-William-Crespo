Sistema Modular de Gestión de Restaurante

**Autor:** William Gynmar Crespo Farias  
**Fecha:** Junio 2026  
**Lenguaje:** Python 3  
**Paradigma:** Programación Orientada a Objetos (POO)

---

## 📋 Descripción del Proyecto

[cite_start] Este proyecto implementa un **sistema modular de gestión de restaurante** desarrollado bajo los principios de la Programación Orientada a Objetos (POO)[cite: 13, 138]. [cite_start]El sistema proporciona una arquitectura escalable y mantenible para administrar los elementos fundamentales de un negocio gastronómico[cite: 9, 138].

### Funcionalidades Principales:

- [cite_start]**Gestión de Productos:** Crear y administrar el menú del restaurante con categorías, precios y descripciones[cite: 26, 27, 76, 77].
- [cite_start]**Registro de Clientes:** Registrar clientes con identificadores únicos para llevar un seguimiento de los visitantes[cite: 29, 30, 76, 77].
- [cite_start]**Visualización de Datos:** Mostrar el menú organizado por categorías y listar los clientes registrados de manera clara y formateada en la consola[cite: 80, 92, 93, 94].
- **Validación de Duplicados:** Prevenir la duplicación de productos (por nombre) y clientes (por ID).
- [cite_start]**Presentación Profesional:** Interfaz en consola con formato legible y emojis para mejor experiencia del usuario.

---

## 🏗️ Estructura Modular del Proyecto

[cite_start]La arquitectura del proyecto sigue el patrón de **separación de responsabilidades** mediante tres capas principales, respetando la estructura mínima requerida[cite: 9, 36, 138, 141]:

### 📂 Estructura de Carpetas

restaurante_app/│├── 📄 README.md                    # Documentación del proyecto├── 📄 main.py                      # Punto de entrada del programa│├── 📁 modelos/                     # Capa de Modelos de Datos (Entidades)│   ├── producto.py                 # Clase Producto│   └── cliente.py                  # Clase Cliente│└── 📁 servicios/                   # Capa de Servicios y Lógica de Negocio└── restaurante.py              # Clase Restaurante (servicio principal)
### 📋 Descripción Detallada de Capas

#### **1️⃣ Capa de Modelos (`modelos/`)**

Esta capa contiene las **clases base** que representan las entidades puras del sistema[cite: 46, 52, 155].

**Archivo: `producto.py`**
- **Clase:** `Producto` [cite: 47, 53]
- **Responsabilidad:** Representar un plato, bebida o producto disponible en el restaurante[cite: 26, 27, 54].
- **Atributos:** `nombre` (str), `precio` (float), `categoria` (str)[cite: 76, 77].
- **Métodos:** `__init__()` (constructor) y `__str__()` (representación en texto legible)[cite: 74, 75, 81, 82, 84].

**Archivo: `cliente.py`**
- **Clase:** `Cliente` [cite: 48, 56]
- **Responsabilidad:** Representar a una persona que consume o realiza un pedido[cite: 29, 30, 57, 58].
- **Atributos:** `nombre` (str), `id_cliente` (int)[cite: 76, 77].
- **Métodos:** `__init__()` (constructor) y `__str__()` (representación en texto legible)[cite: 74, 75, 81, 82, 84].

#### **2️⃣ Capa de Servicios (`servicios/`)**

Esta capa contiene la **lógica de negocio** y la gestión de las operaciones principales[cite: 49, 52, 59, 60].

**Archivo: `restaurante.py`**
- **Clase:** `Restaurante` [cite: 50, 60]
- **Responsabilidad:** Administrar la colección de productos y clientes registrados[cite: 31, 32, 60].
- **Atributos:** `nombre_restaurante` (str), `productos` (list), `clientes` (list)[cite: 76, 77].
- **Métodos Principales:** `agregar_producto()`, `registrar_cliente()`, `mostrar_menu()` y `mostrar_clientes()`[cite: 79, 80].

#### **3️⃣ Punto de Entrada (`main.py`)**

El archivo principal que actúa como el **punto de arranque coordinado del programa**[cite: 51, 61, 62].

**Responsabilidades:**
- Instanciar la clase de servicio `Restaurante`[cite: 62, 88].
- Registrar 7 productos iniciales agrupados por categorías (superando el mínimo sugerido)[cite: 90].
- Registrar 4 clientes con identificadores únicos[cite: 90].
- Demostrar el funcionamiento de las validaciones de control de datos duplicados.
- Mostrar toda la información del sistema de forma organizada en la consola[cite: 63, 64, 92, 93, 94].

---

## 🔄 Importaciones y Dependencias

El proyecto utiliza una estructura de importaciones clara, directa y organizada entre módulos[cite: 85, 86, 87]:

```python
# En main.py
from servicios.restaurante import Restaurante

# En servicios/restaurante.py
from modelos.producto import Producto
from modelos.cliente import Cliente
Ventaja: Las dependencias se especifican de manera limpia descendente. main.py solo importa directamente la capa de servicio Restaurante, ya que las clases de la capa modelos son gestionadas internamente por el servicio, reduciendo el acoplamiento innecesario.  🔧 Cambios y Correcciones RealizadasDurante el ciclo de desarrollo en PyCharm, se aplicaron las siguientes optimizaciones de código:Importaciones y Estructura LimpiaRemoción de archivos innecesarios: Se eliminaron los archivos __init__.py para cumplir estrictamente con el árbol de archivos mínimos y la estructura de repositorio simplificada que exige la guía.  Corrección de Case-Sensitivity: Se estandarizaron los nombres de las carpetas de paquetes completamente en minúsculas (modelos y servicios) conforme a las buenas prácticas de Python (PEP 8) y las rutas físicas del proyecto.  Corrección de Tipos de Datos (IDs de Clientes)Modificación: Se cambiaron los códigos identificadores de los clientes de notación con ceros a la izquierda (001, 002...) a números enteros base 10 estándar (1001, 1002, 1003, 1004).Razón: Prevenir errores de sintaxis en el intérprete de Python, el cual restringe el uso de ceros a la izquierda en números enteros para evitar confusiones con la antigua notación de literales octales.💡 Importancia de la Modularización y Separación de ResponsabilidadesLa modularización y la separación de responsabilidades (aplicando las bases del principio SRP de SOLID) representan pilares fundamentales en el desarrollo de software profesional por las siguientes ventajas:  1. MantenibilidadPermite que las modificaciones o correcciones de errores aplicadas sobre un módulo en específico (por ejemplo, alterar el formato de despliegue en producto.py) estén totalmente focalizadas. Esto previene efectos secundarios o roturas imprevistas en la lógica de negocio general del sistema.  2. Reutilización de CódigoAl separar las clases base (Producto, Cliente) de los procesos de gestión, estas entidades se convierten en piezas de código independientes. Pueden ser importadas en nuevos módulos, sistemas de facturación o futuras aplicaciones sin necesidad de reescribir ni duplicar su lógica.  3. Escalabilidad y FlexibilidadFacilita la evolución controlada del software. Si en el futuro el restaurante requiere añadir nuevas características, una interfaz gráfica (GUI) o una base de datos para la persistencia, la arquitectura modular permite extender el programa agregando nuevos archivos o capas de servicio sin alterar la estabilidad del núcleo existente.  🚀 Cómo Ejecutar el ProyectoRequisitos:Python 3.6 o versiones superiores.Acceso a una terminal de comandos.Instrucciones de ejecución:Bash# 1. Acceder al directorio principal del proyecto
cd restaurante_app

# 2. Arrancar el programa principal coordinado
python main.py
Salida de Consola Esperada:Bloque informativo inicial mostrando el estado vacío del establecimiento.Registro exitoso de los 7 productos en el menú y los 4 clientes.  Mensajes informativos de bloqueo ante los casos de prueba de duplicidad.Impresión en consola del menú completo del restaurante formateado estéticamente por categorías (Entrada, Plato Principal, Bebida, Postre).  Listado numerado de todos los clientes válidos incorporados al sistema.  Última Actualización: Junio 2026Versión: 1.1.0