# Referencias visuales, en liviano

Todo lo que ya está generado, reducido a JPG (lado mayor de 1.200 a 1.800 px, calidad 78).
Son 88 imágenes y algo más de 8 MB, contra 300 MB de los originales.

**Para qué sirven:** para ver lo que ya existe antes de gastar un crédito. Los originales a
resolución completa viven en `C:\pesonajes para videos\`; estos son para mirar y comparar,
no para usar como referencia de generación.

| Carpeta | Qué hay | Vigencia |
| --- | --- | --- |
| `personajes/` | Las 9 hojas de personaje y la foto de elenco | **Vigentes.** Faltan Yadira y Kevin |
| `personajes-laminas/` | Expresiones y poses, 7 personajes | Vigentes |
| `planos/` | Los 6 planos dibujados con PIL | **Versión Perú, se rehacen** |
| `maqueta/` | Las vistas crudas de la maqueta 3D, sin realismo | Geometría vigente |
| `escenarios/` | Arte de concepto de los escenarios | **Versión Perú, se rehacen** |
| `vistas-desde-maqueta/` | Las vistas de la maqueta ya convertidas en foto realista | Geometría vigente, ambiente de Perú |
| `prueba-escena/` | Los cuadros de la prueba del episodio 1 | Vigentes como prueba de escala |
| `planos-ecuador/` | Los 6 planos rehechos para Ecuador | **Vigentes.** Reemplazan a `planos/` |
| `maqueta-ecuador/` | Las 7 vistas del taller y las 6 del bar y el pasaje, desde la maqueta nueva | **Vigentes.** Reemplazan a `maqueta/` |
| `ciudad-ecuador/` | **Las 24 vistas de Puerto Candela con material: 16 horizontales y 8 verticales** | **Vigentes.** Reemplazan a las 8 de bloques |

## Defectos que se ven en estas imágenes

Están apuntados para que no se repitan al regenerar:

- El plumaje de Gallín pierde consistencia en primeros planos.
- La nariz de Porfirio cambia entre imágenes.
- En `vistas-desde-maqueta/bar_ventana`, el taller salió de ladrillo: tiene que ser negro ónix.
- En `vistas-desde-maqueta/banco` y `puerta`, el generador agregó columnas de elevador que no
  están en el plano.


## Lo rehecho el 25 de septiembre

`planos-ecuador/` y `maqueta-ecuador/` salen de los scripts de `codigo/planos_diseno/`
y `codigo/remotion-src/`, ya en versión Ecuador y con las nueve zonas nuevas. Cuestan
0 créditos: se vuelven a generar corriendo los scripts.

Las carpetas viejas `planos/`, `maqueta/`, `escenarios/` y `vistas-desde-maqueta/` se
quedan como referencia de lo que había, pero **para generar imágenes manda lo nuevo.**

Defectos de la versión peruana que ya no aplican, porque se corrigieron en la maqueta:
la corona de la puerta roja estaba metida dentro de la hoja y no se veía, y la
desmontadora tapaba la puerta en la toma que avanza hacia ella.


## Lo rehecho el 25 de septiembre, por la tarde

`planos-ecuador/` suma las **cuatro caras del taller** y las **cuatro caras del bar**,
cada una con su planta de cubierta. Existen para que ningún plano de ningún episodio
tenga que inventar un lado, y traen la propuesta de materiales cara por cara.

`ciudad-ecuador/` es el barrio entero en 3D, de `codigo/remotion-src/Ciudad3D.tsx`.
La geometría sale tal cual del plano urbano, y las casas usan una **semilla fija**:
el mismo lote saca siempre la misma casa, del mismo alto y del mismo color. La ciudad
es reproducible entre capítulos. Cambiar la semilla cambia el barrio entero.


## Lo rehecho el 25 de septiembre, de noche

`ciudad-ecuador/` se reemplaza entero. Las ocho vistas de bloques grises se cambian por
**veinticuatro con material**: dieciséis horizontales y ocho verticales, que son las tomas
oficiales del pueblo. Salen de `codigo/remotion-src/Ciudad3D.tsx` sobre el motor nuevo
`realismo.tsx`, y cuestan 0 créditos: se vuelven a generar corriendo el render.

Qué cambió respecto de la maqueta de bloques:

- **Cielo físico** con el sol en su posición real y el cielo iluminando la escena, en vez
  de una lámpara inventada. Cuatro horas: mediodía, tarde, amanecer y noche.
- **Materiales**: enlucido con la humedad subiendo del pie del muro, zinc acanalado con su
  relieve y su óxido, adoquín, lastre con las dos huellas de las llantas, asfalto.
- **Techos a dos aguas**, que es lo que pide la biblia. Los de la maqueta vieja eran planos.
- Rejas en toda la planta baja, cables cruzando la calle, tanque de agua y antena en la
  azotea, y una de cada cinco casas de dos pisos con las varillas al aire.
- El pueblo entero, no solo el barrio: el Estero Candela, las camaroneras, los arrozales,
  el manglar, la Loma de la Cruz y los otros cuatro barrios.

`planos-ecuador/` suma tres: el **territorio**, las **secciones de las cuatro calles** y el
**diseño del Parque del Reloj**.

**No hay personas en ninguna vista, a propósito.** Una figura humana mal hecha en la imagen
de referencia se le contagia al video generado. Las personas entran después, en la
generación, con su hoja de personaje.

Estas vistas **todavía no son la imagen final**: son la referencia que obliga a la imagen
final a respetar la ciudad. Los prompts para convertirlas están escritos en
`codigo/vistas_ciudad.py` y cuestan unos 72 créditos las 24.
