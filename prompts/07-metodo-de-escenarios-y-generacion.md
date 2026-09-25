# Método de escenarios y generación

Esto no es un prompt: es el procedimiento que se descubrió a golpes y que ahora es obligatorio. Nació cuando el gallo del letrero cambiaba de sitio en cada imagen y los escenarios salían distintos cada vez.

## La regla de oro

**Primero el plano con medidas. Después la maqueta 3D. Y solo entonces la imagen realista, generada usando la vista de la maqueta como referencia.**

Nunca al revés. Una imagen bonita sin plano detrás produce un escenario que no se puede repetir, y a los tres videos el espectador nota que el lugar cambia.

### Paso 1 · El plano

Se dibuja por código con Python y PIL, con medidas reales en metros: planta, fachada y corte. Scripts en `planos_diseno\`. El usuario rechaza escenarios chicos o sin medidas, y con razón: el taller pasó de una caja a 24 × 30 m cuando se dibujó de verdad.

### Paso 2 · La maqueta

Se construye en Remotion con three.js, con las medidas exactas del plano, y se renderizan vistas desde cámaras colocadas dentro. Aquí aparecen los errores que el plano esconde: así se descubrió que la estantería de llantas chocaba con el almacén al correrse.

### Paso 3 · La imagen realista

Se genera con Nano Banana Pro pasándole **la vista de la maqueta como imagen de referencia**, y un prompt que empieza diciendo que respete exactamente cámara, encuadre, perspectiva y posición de cada objeto, y que solo reemplace los bloques grises por materiales reales.

### Paso 4 · El video

Con Veo, usando esa imagen como **cuadro inicial**. Si la cámara se mueve mucho, hay que dar **cuadro inicial y cuadro final**, porque si no, a mitad del clip el personaje cambia de ropa.

## Reglas de generación aprendidas a costa de créditos

| Regla | Por qué |
| --- | --- |
| Nunca escribir "TikTok" en un prompt de Veo | Le pone el logo de TikTok a la ropa de los personajes |
| Pedir cantidades exactas en mayúsculas, y usar solo el tramo donde se cumple | Veo agrega objetos: se pidieron 3 gomitas y cayeron 8 |
| Revisar una tira de cuadros de cada clip antes de montar | Los defectos aparecen en el segundo 3, no en el 0 |
| Recortar bordes redondeados de las imágenes de referencia | El borde se contagia a todas las imágenes generadas después |
| Las hojas de personaje son la referencia de todo | Tres vistas del mismo personaje, fondo gris, luz pareja |
| Para el producto, subir la foto oficial como referencia | Si no, la IA inventa la etiqueta |

## Consistencia de personajes

Cada personaje tiene su hoja con tres vistas. Toda imagen donde aparezca se genera pasando esa hoja como referencia, y el prompt describe su ropa completa otra vez. Aun así, en primeros planos el plumaje y las narices derivan: es el defecto conocido que sigue abierto.

## Montaje sobre el ritmo

Cuando hay música, se detecta el tempo y se arma la grilla de golpes (`golpe n = primer golpe + n × duración del compás`). Cada corte cae en un golpe. Las duraciones se miden en cuadros enteros desde el inicio del video, nunca sumando duraciones sueltas, porque cincuenta cortes se corren solos y al final el video se desincroniza.
