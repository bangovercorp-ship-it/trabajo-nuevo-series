# Estado del proyecto

## Decisiones cerradas, no se vuelven a discutir

- La serie es **ecuatoriana**: Puerto Candela (Guayas) en la temporada 1, Guayaquil en la 2. Todo lo peruano quedó fuera.
- El elenco son **híbridos fotorrealistas con cara humana obligatoria** (por la sincronía de labios). Nada de cabeza de animal, nada de disfraz.
- **El carro siempre está roto de verdad** y el arreglo se ve en cámara. El consejo ocurre mientras el taller trabaja, nunca en lugar de trabajar.
- Método de escenarios, ya probado: **primero el plano con medidas, después la maqueta 3D, y solo entonces la imagen realista**, generada usando la vista de la maqueta como referencia. Así se acabaron las incoherencias.
- En Veo, las tomas con movimiento se generan con **cuadro inicial y final**, si no, el personaje cambia de ropa a mitad del clip.
- Producto: Lázaro toda la temporada 1. **Nunca se promete que cure nada. Se recomienda, no se receta.**

## El elenco

| Personaje | Animal | Qué hace en el taller |
| --- | --- | --- |
| Tío Gallín (Máximo Gallardo) | Gallo | Maestro y dueño. Diagnostica y firma las salidas |
| Porfirio | Chancho | Caja y recepción. Fue el Cliente Cero |
| Toribio | Toro | Eléctrico y electrónico |
| Renzo | Zorro | Asesor de servicio: cotiza, explica, consigue repuestos |
| **Yadira, la Garza** (nueva) | Garza | Técnica de motos y tricimotos |
| **Kevin, el Pelado** (nuevo) | Mono | Aprendiz. Graba todo con el celular |
| Doña Micaela | Gata | Dueña del bar de enfrente. Manda clientes |
| Aurora | Coneja | El interés amoroso de la temporada 1 |
| Fausto Pavón | Pavo real | El antagonista, de Guayaquil |

Los dos nuevos **todavía no tienen hoja de personaje generada**. Es de lo primero que hay que hacer.

## Qué existe ya, y dónde

### Carpeta `C:\pesonajes para videos\`

| Qué | Dónde |
| --- | --- |
| Hojas de personaje del elenco viejo | `gallin\03-hoja-tio-gallin.png` y siguientes |
| Láminas de expresiones y poses | `gallin\laminas\` |
| Planos por código (barrio, taller, bar, pasaje) | `planos_diseno\plano_urbano.py`, `plano_taller.py`, `plano_bar_pasaje.py` |
| Maqueta 3D en Remotion + three.js | `remotion\src\Taller3D.tsx` y `Escenas3D.tsx` |
| Vistas realistas generadas desde la maqueta | `gallin\escenarios\desde-maqueta\` |
| Prueba de escena del episodio 1 | `gallin\prueba-escena\` |
| Spot de Lázaro terminado | `lazaro-spot.mp4` |
| Promocional del bar terminado | `promo-bar\bangover-bar-tiktok.mp4` (mudo) y `-previa.mp4` (con música) |
| Pruebas de voz de Gallín | `voces\` |

**Ojo con el nombre de la carpeta:** es `pesonajes`, sin la r. Está así desde el principio.

### Identidad de marca

`C:\JUEGOS APP\bangover-identidad\` — el logo oficial es la gota con la llama: `png\gota\gota-insinua.png`. Va bordado en oro al pecho del polo negro del asesor.

### Fotos oficiales de producto

`C:\PLATAFORMA BANGOVER\plataforma-bangover\productos\` — se suben como referencia para que la IA no invente etiquetas.

## Lo que está terminado y aprobado

1. **Spot de Lázaro**, con sonidos reales, subtítulos y grado de color.
2. **Biblia de la serie** completa, con los 8 guiones.
3. **Planos y maqueta** del taller, el bar y el pasaje.
4. **Promocional del bar** (42,5 s, cortado sobre el pulso de la canción de referencia). Está ambientado en Lima: **hay que rehacerlo en Ecuador.**
5. **Expediente técnico** del taller y del barrio, ya en Ecuador.
6. **Biblia sociocultural** del habla y la vida de la costa del Guayas.

## Defectos conocidos, sin corregir

- El plumaje de Gallín pierde consistencia en primeros planos.
- La nariz de Porfirio cambia entre imágenes.
- En la vista del bar desde la ventana, el taller salió de ladrillo y tiene que ser negro ónix.
- En dos vistas de la maqueta, el generador agregó columnas de elevador que no están en el plano.
- Todas las imágenes de escenarios siguen siendo las de la versión peruana.
