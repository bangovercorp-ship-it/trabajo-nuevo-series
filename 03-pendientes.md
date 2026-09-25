# Lo que falta, en orden

> El estado por rol está en `06-tablero-de-control.md`. Ahí se ve de un vistazo qué está cerrado y qué no. Este archivo es el plan de trabajo.

> Los scripts que se nombran abajo están copiados en `codigo/` de este repositorio, con su índice. Las imágenes que hay que comparar están en `referencias/`.

El trabajo en papel está hecho. **Lo que sigue es visual**, y es el motivo de abrir el chat nuevo: rehacer el pueblo y el taller con lo que dictó la oficina técnica, ahora en Ecuador.

## Bloque 1 · Planos y maqueta (0 créditos, todo por código)

1. **Plano urbano de El Cruce, versión Ecuador.** Nombres nuevos de calles, la vulcanizadora, la tercena, la picantería, la UPC, la gasolinera. Script a modificar: `planos_diseno\plano_urbano.py`.
2. **Planta del taller con las nueve zonas que faltaban.** Bahía 0 de recepción, puesto de diagnóstico, área de residuos peligrosos, canaleta con trampa de grasas, extracción de gases, aire acondicionado, toldo de espera, zona limpia de electrónica, control de calidad. Más el piso a +0,40 m con rampa por la inundación. Script: `plano_taller.py`.
3. **Fachada costeña.** Bloque enlucido, cubierta de zinc, turbinas de extracción girando en el techo, portones abiertos. El gallo del letrero no se toca.
4. **Maqueta 3D actualizada** sobre la planta nueva: `remotion\src\Taller3D.tsx`.

Todo esto está especificado zona por zona en la pestaña **Ecuador · taller y barrio** de la biblia.

## Bloque 2 · Imágenes (unos 42 créditos)

| Qué | Cuántas | Créditos |
| --- | --- | --- |
| Vistas realistas del taller desde la maqueta | 6 | 18 |
| Fachada de día y de noche | 2 | 6 |
| Hojas de personaje de Yadira (garza) y Kevin (mono) | 2 | 6 |
| Exteriores del pueblo: la vía, la calle de los mecánicos, el mercado, el malecón | 4 | 12 |

Regla que no se salta: **cada imagen se genera con la vista de la maqueta o el plano como referencia.**

## Bloque 3 · El promocional del bar, en Ecuador (unos 100 créditos)

El que está entregado es de Lima. Hay que rehacerlo en la costa ecuatoriana: bar costeño, calor, gente de allá, y el asesor con el polo negro y la gota bordada. Los archivos y el montaje ya existen y sirven tal cual (`promo.py`, `clips_promo.py`, `montar_promo.py`): solo cambian los prompts y se vuelven a generar los 9 cuadros y los 9 clips. El corte sobre el pulso de 129,2 bpm se mantiene.

## Bloque 4 · Voces

Elegir el reparto completo en ElevenLabs, con **acento costeño ecuatoriano**, no neutro latino. Gallín, Porfirio, Toribio, Renzo, Micaela, Aurora, Fausto, Yadira y Kevin.

## Bloque 5 · Producir el episodio 1

Con todo lo anterior listo: desglosar el guion en tomas, generar cuadros, generar clips con cuadro inicial y final, montar con sonido real y subtítulos.

## Lo que no se puede resolver aquí

**Que un ecuatoriano de la costa lea la parte del habla**, sobre todo los términos del taller (cloche, cabezote, bocines) y las groserías con su intensidad. Entra aquí el vocativo **ñaño**, que se puso el 24 de septiembre donde antes decía *causa*: es ecuatoriano y está documentado, pero hay que oír si un hombre mayor de la costa le dice así a un cliente más joven, o si diría *mijo*, *pelado* o *compadre*. Está todo marcado en la biblia sociocultural como pendiente de validar. Es el mayor riesgo del proyecto: un acento falso se detecta en tres palabras y tumba todo lo demás.

## Defectos que conviene arreglar de paso

- El plumaje de Gallín en primeros planos.
- La nariz de Porfirio.
- El taller de ladrillo en la vista desde la ventana del bar: tiene que ser negro ónix.
- Las columnas de elevador inventadas en dos vistas de la maqueta.
