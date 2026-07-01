# Restaurante App (POO Python)
William Gynmar Crespo Farias
POO SEMANA 6 - PARCIAL 1
Este proyecto es una versión mejorada del sistema `restaurante_app` utilizando Programación Orientada a Objetos en Python, diseñado para la Semana 6 del Parcial 1.

## Estructura del Proyecto

```text
restaurante_app/
├── modelos/
│   ├── __init__.py
│   ├── producto.py    (Clase base abstracta Producto)
│   ├── platillo.py    (Clase hija Platillo)
│   └── bebida.py      (Clase hija Bebida)
├── servicios/
│   ├── __init__.py
│   └── restaurante.py (Servicio de administración de productos)
├── main.py            (Punto de entrada principal)
└── README.md          (Esta documentación)
```

## Conceptos Clave de POO Aplicados

1. **Herencia (Inheritance)**:
   - `Producto` hereda de `abc.ABC` convirtiéndose en una clase base abstracta que no puede ser instanciada directamente.
   - `Platillo` y `Bebida` heredan los atributos y comportamientos comunes de `Producto` utilizando `super().__init__()` en sus constructores.

2. **Encapsulación (Encapsulation)**:
   - El atributo `__precio` en `Producto` es estrictamente privado.
   - La lectura y modificación se realizan mediante métodos públicos (`obtener_precio()` y `cambiar_precio()`).

3. **Validación**:
   - `cambiar_precio()` contiene una regla de negocio que rechaza cualquier precio menor o igual a cero (`<= 0`).

4. **Polimorfismo (Polymorphism)**:
   - **Primer Nivel**: Sobrescritura de `mostrar_informacion()` en ambas subclases (`Platillo` y `Bebida`), imprimiendo datos específicos (tiempo de preparación y volumen en ml).
   - **Segundo Nivel**: Declaración de un método abstracto `servir()` en la clase padre implementado de forma específica en cada clase hija para simular la preparación del platillo o servicio de bebida.
   - La clase `Restaurante` procesa y ejecuta estos comportamientos polimórficamente recorriendo su lista de productos genéricos.

---

## Resultados de Ejecución de Pruebas

Al ejecutar `python main.py` se obtiene la siguiente salida en consola:

```text
--- INICIANDO SISTEMA RESTAURANTE APP ---

Producto 'Lomo Saltado' registrado con éxito en el restaurante 'El Rincón del Sabor'.
Producto 'Ceviche Clásico' registrado con éxito en el restaurante 'El Rincón del Sabor'.
Producto 'Chicha Morada' registrado con éxito en el restaurante 'El Rincón del Sabor'.
Producto 'Pisco Sour' registrado con éxito en el restaurante 'El Rincón del Sabor'.

============================================================
MENÚ DEL RESTAURANTE: EL RINCÓN DEL SABOR
============================================================
1. [Platillo] Producto: Lomo Saltado | Precio: $12.50 | Estado: Disponible | Prep: 20 min
2. [Platillo] Producto: Ceviche Clásico | Precio: $15.00 | Estado: Disponible | Prep: 15 min
3. [Bebida] Producto: Chicha Morada | Precio: $3.50 | Estado: Disponible | Volumen: 500 ml
4. [Bebida] Producto: Pisco Sour | Precio: $8.00 | Estado: Disponible | Volumen: 250 ml
============================================================


============================================================
PREPARACIÓN Y SERVICIO EN: EL RINCÓN DEL SABOR
============================================================
1. El platillo 'Lomo Saltado' se está cocinando en cocina. Tiempo de espera: 20 min. ¡Se servirá caliente!
2. El platillo 'Ceviche Clásico' se está cocinando en cocina. Tiempo de espera: 15 min. ¡Se servirá caliente!
3. La bebida 'Chicha Morada' (500 ml) se está sirviendo en la barra. ¡Se servirá fría con hielo!
4. La bebida 'Pisco Sour' (250 ml) se está sirviendo en la barra. ¡Se servirá fría con hielo!
============================================================

--- DEMOSTRACIÓN DE VALIDACIÓN Y ENCAPSULACIÓN ---
Precio actual de Lomo Saltado: $12.50

Intentando cambiar precio de Lomo Saltado a -$5.00...
Error de validación: El precio para 'Lomo Saltado' debe ser mayor a 0 (Intentado: -5.0)
Precio después del intento: $12.50

Intentando cambiar precio de Lomo Saltado a $0.00...
Error de validación: El precio para 'Lomo Saltado' debe ser mayor a 0 (Intentado: 0.0)
Precio después del intento: $12.50

Intentando cambiar precio de Lomo Saltado a $13.99...
¡Precio actualizado con éxito!
Precio final: $13.99

--- MENÚ ACTUALIZADO ---

============================================================
MENÚ DEL RESTAURANTE: EL RINCÓN DEL SABOR
============================================================
1. [Platillo] Producto: Lomo Saltado | Precio: $13.99 | Estado: Disponible | Prep: 20 min
2. [Platillo] Producto: Ceviche Clásico | Precio: $15.00 | Estado: Disponible | Prep: 15 min
3. [Bebida] Producto: Chicha Morada | Precio: $3.50 | Estado: Disponible | Volumen: 500 ml
4. [Bebida] Producto: Pisco Sour | Precio: $8.00 | Estado: Disponible | Volumen: 250 ml
============================================================
```
