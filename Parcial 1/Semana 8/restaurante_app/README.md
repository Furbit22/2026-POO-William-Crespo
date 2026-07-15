William Gynmar Crespo Farias
Programacion Orientada a Objetos
# Sistema de Restaurante App

Este es un sistema básico de consola para la gestión de productos, bebidas y clientes de un restaurante, diseñado en Python bajo el paradigma de la Programación Orientada a Objetos (POO) y aplicando principios de diseño de software (SOLID).

## Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

```text
restaurante_app/
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── bebida.py
│   └── cliente.py
├── servicios/
│   ├── __init__.py
│   └── restaurante.py
└── main.py
```

* **`modelos/producto.py`**: Contiene la clase base `Producto` con sus datos generales.
* **`modelos/bebida.py`**: Contiene la clase `Bebida` que hereda de `Producto` agregando atributos específicos (`tamano`, `envase`).
* **`modelos/cliente.py`**: Contiene la clase `Cliente`.
* **`servicios/restaurante.py`**: Contiene la clase de servicio `Restaurante`, encargada de administrar las colecciones, validaciones de unicidad y lógica del negocio.
* **`main.py`**: Punto de arranque que interactúa con el usuario mediante un menú en consola.

## Principios SOLID Aplicados

1. **Responsabilidad Única (Single Responsibility Principle - SRP)**: Cada clase tiene una sola razón para cambiar. Los modelos representan los datos, el servicio administra la persistencia temporal en memoria y validación, y `main.py` maneja la interfaz de consola.
2. **Abierto/Cerrado (Open/Closed Principle - OCP)**: El sistema está abierto a la extensión pero cerrado a la modificación. Al añadir `Bebida`, extendimos `Producto` sin necesidad de alterar la lógica del servicio `Restaurante` para registrar o listar productos.
3. **Sustitución de Liskov (Liskov Substitution Principle - LSP)**: Las instancias de la subclase `Bebida` pueden reemplazar a las de `Producto` en la colección única administrada por `Restaurante` sin alterar la corrección del programa, permitiendo el uso uniforme del método `mostrar_informacion()`.

## Relación entre Producto y Bebida: Justificación de la Herencia ("Es Un")

En la Programación Orientada a Objetos, la herencia se utiliza para modelar relaciones de especialización donde una subclase es un tipo específico de la superclase (relación **"es un"** / **"is-a"**). 

En este sistema:
* **Bebida "es un" Producto**: Una bebida comparte todas las características esenciales de cualquier producto del restaurante (tiene un código de identificación, un nombre comercial, pertenece a una categoría y posee un precio de venta).
* **Especialización**: Además de los atributos comunes, la bebida requiere almacenar propiedades particulares como el `tamaño` (ej. 500ml, 1L) y el `tipo de envase` (ej. Vidrio, Plástico, Lata).
* **Reutilización y Consistencia**: Al heredar de `Producto`, la clase `Bebida` evita duplicar código y garantiza que cualquier cambio en la estructura o comportamiento base de un producto se propague automáticamente a las bebidas, preservando la consistencia del dominio.

## Reflexión sobre el Diseño de Software Mantenible

Diseñar software dividiendo responsabilidades claras (aplicando modularidad y principios SOLID) tiene un impacto directo en la mantenibilidad y escalabilidad del código a largo plazo:

1. **Facilidad de Extensión**: Si en el futuro el restaurante decide vender platos elaborados (combos, postres) con atributos específicos como ingredientes o alérgenos, solo se requiere crear una nueva subclase que herede de `Producto`. La clase de servicio `Restaurante` y la lógica de listado no necesitarían modificaciones, cumpliendo con el principio Abierto/Cerrado (OCP).
2. **Reducción del Acoplamiento**: Al desacoplar la interfaz de usuario (`main.py`) de la lógica de negocio (`restaurante.py`), es sumamente sencillo migrar la aplicación desde una consola a una API web o interfaz gráfica en el futuro sin reescribir las reglas del negocio ni los modelos de datos.
3. **Código Limpio y Legible**: Evitar condicionales repetidos (como `isinstance` o `type`) para formatear la información de cada producto en la consola (apoyándonos en el polimorfismo) resulta en un código mucho más limpio, fácil de leer y libre de errores humanos al agregar nuevos tipos de productos.

## Instrucciones de Ejecución

Para ejecutar el programa, asegúrate de estar en el directorio `restaurante_app` y ejecuta:

```bash
python main.py
```
