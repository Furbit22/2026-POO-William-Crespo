# Gestión de mascotas — Programación Tradicional vs Programación Orientada a Objetos

Estudiante: William Crespo POO Paralelo C

Descripción
-----------
Este repositorio contiene dos implementaciones de un pequeño sistema de
gestión de mascotas que registran y muestran la información básica de una
mascota (nombre, especie y edad):

- `programacion_tradicional/tradicional.py`: solución usando programación
  tradicional (sin clases). Utiliza variables, diccionarios y funciones para
  solicitar datos por teclado, validar entradas y mostrar la información.
- `programacion_poo/`: versión orientada a objetos.
  - `programacion_poo/mascota.py`: define la clase `Mascota` con los atributos
	`nombre`, `especie` y `edad`, y los métodos `mostrar_informacion()` y
	`hacer_sonido()`.
  - `programacion_poo/main.py`: crea varias instancias de `Mascota` y
	demuestra el uso de sus métodos.


Reflexión sobre Programación Tradicional vs Programación Orientada a Objetos
-----------------------------------------------------------------------------
1. Abstracción y representación de datos:
   - Tradicional: los datos de una mascota se representan típicamente con
	 diccionarios o tuplas y las operaciones se implementan como funciones
	 que reciben estos datos. Esto es directo y suficiente para programas
	 pequeños.
   - POO: la mascota se modela como una entidad (objeto) que encapsula sus
	 atributos y comportamientos. Esto facilita razonar sobre el dominio y
	 usar métodos que actúan sobre la misma entidad.

2. Encapsulación y organización:
   - Tradicional: la lógica y los datos pueden dispersarse entre funciones,
	 lo que en proyectos grandes puede hacer difícil el mantenimiento.
   - POO: agrupar datos y comportamiento en clases mejora la organización,
	 la legibilidad y reduce el acoplamiento accidental.

3. Reutilización y extensibilidad:
   - Tradicional: reutilizar y extender comportamiento puede implicar
	 copiar/ajustar funciones o cambiar muchas partes del código.
   - POO: se facilita la extensión (herencia, composición) y la reutilización
	 mediante métodos bien definidos y estructuras de clase.

4. Complejidad y sobrecoste:
   - Tradicional: más sencillo y con menos "overhead" conceptual para tareas
	 pequeñas o scripts rápidos.
   - POO: introduce una capa de abstracción útil cuando el dominio crece; en
	 proyectos muy pequeños puede parecer verboso.

5. Cuándo usar cada uno:
   - Para ejercicios simples, scripts o tareas puntuales la programación
	 tradicional es rápida y clara.
   - Para sistemas con entidades del dominio, comportamiento asociado y
	 crecimiento previsto, la POO aporta estructura, mantenibilidad y
	 extensibilidad.

Conclusión
----------
Ambos enfoques resuelven el mismo problema funcionalmente. La elección entre
uno u otro depende del tamaño del proyecto, la necesidad de modelar entidades
de forma natural y la expectativa de crecimiento y reutilización del código.
En el ejercicio se evidencia cómo la POO facilita agrupar datos y comportamiento
en una unidad coherente (`Mascota`), mientras que la versión tradicional
permite una solución más directa sin la formalidad de clases.

