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
