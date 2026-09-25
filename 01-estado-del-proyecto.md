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

**Copia en el repositorio.** Los scripts están copiados en `codigo\` y todo lo generado está en `referencias\`, en JPG liviano. Es lo que permite trabajar desde una sesión que no ve este disco. Si se cambia un script aquí, hay que volver a copiarlo allá.

### Identidad de marca

`C:\JUEGOS APP\bangover-identidad\` — el logo oficial es la gota con la llama: `png\gota\gota-insinua.png`. Va bordado en oro al pecho del polo negro del asesor.

### Fotos oficiales de producto

`C:\PLATAFORMA BANGOVER\plataforma-bangover\productos\` — se suben como referencia para que la IA no invente etiquetas.

## Lo que está terminado y aprobado

1. **Spot de Lázaro**, con sonidos reales, subtítulos y grado de color.
2. **Biblia de la serie** completa, con los 8 guiones.
3. **Planos y maqueta** del taller, el bar y el pasaje. Con un matiz que importa: **la geometría está aprobada, el dibujo no.** Las medidas y la maqueta 3D sirven; los planos dibujados y las imágenes son de la versión peruana y se rehacen (Bloque 1 de `03-pendientes.md`).
4. **Promocional del bar** (42,5 s, cortado sobre el pulso de la canción de referencia). Está ambientado en Lima: **hay que rehacerlo en Ecuador.**
5. **Expediente técnico** del taller y del barrio, ya en Ecuador.
6. **Biblia sociocultural** del habla y la vida de la costa del Guayas.

## Defectos conocidos, sin corregir

- El plumaje de Gallín pierde consistencia en primeros planos.
- La nariz de Porfirio cambia entre imágenes.
- En la vista del bar desde la ventana, el taller salió de ladrillo y tiene que ser negro ónix.
- En dos vistas de la maqueta, el generador agregó columnas de elevador que no están en el plano.
- Todas las imágenes de escenarios siguen siendo las de la versión peruana.

## Auditoría del 24 de septiembre, por la tarde

Se cruzó esta carpeta contra la biblia, documento por documento. Queda anotado para que
nadie vuelva a auditar lo mismo.

**Corregido en la biblia:**

- La pestaña *Escenarios* seguía llamando **La Capital** a la ciudad de los recuerdos, en
  seis lugares, y el nombre además era falso para Ecuador: Guayaquil no es la capital. Ahora
  dice Guayaquil, incluido el título de la sección.
- La misma pestaña seguía diciendo **jirón**, que es peruano, en las seis menciones de la
  calle de salida del taller. Ahora dice Calle Olmedo, que es el nombre que ya tenía en el
  plano del barrio.
- La pestaña *Personajes a fondo* decía que todas las voces hablan **español peruano de
  Lima**, y le ponía a Gallín el vocativo **causa**, que es limeño. Ahora dice español
  ecuatoriano de la costa, y el vocativo es *ñaño*.
- La pestaña *Estrategia y producción*, que no estaba listada en ninguna parte y por eso
  nadie había revisado, tenía cuatro datos viejos: pedía confirmar con **DIGESA**, que es
  peruana (ahora ARCSA); daba por confirmar el plan de ElevenLabs, que ya funciona;
  contaba 30.000 caracteres al mes en vez de los 23.736 disponibles; y decía que quedaban
  1.970 créditos en vez de 1.744. Y decía **"etiqueta al pata"**, que también es peruano.

**Verificado y sin problema:**

- La pestaña *Biblia* está limpia: ni un rastro peruano.
- Las seis skills de `05-habilidades.md` sí están instaladas en esta máquina. Lo que pasa es
  que una sesión en la nube no ve el disco y por eso no las encuentra.

**Queda sin corregir, y es menor:** el texto alternativo de una imagen del pasaje todavía
dice *Jr. Los Mecánicos*. Es un atributo de la imagen, no del documento, y se arregla cuando
esa imagen se regenere.
