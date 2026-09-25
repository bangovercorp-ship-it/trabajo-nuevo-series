# Episodio 1 · El Cliente Cero · lista de planos

Desglose del 25 de septiembre de 2026. Sale del guion tal como está en la biblia, pestaña *Temporada 1: guiones*, y aplica la gramática de cámara de la pestaña *Estrategia y producción* y las correcciones de la auditoría.

**Nueve elementos: ocho clips y un cuadro fijo. Duración 60 s.**

## Las reglas que se aplicaron

- **Ningún clip pasa de 8 segundos**, que es lo que da Veo 3.1 Fast.
- **El primer cuadro no es un plano general.** La auditoría dejó esa regla para toda la serie y solo corrigió los episodios 2, 5 y 7. El episodio 1 también abría en plano general: corregido en la toma 1.
- **Toda toma con movimiento de cámara se genera con cuadro inicial y cuadro final**, si no el personaje cambia de ropa a mitad del clip. Aquí son las tomas 1 y 7.
- **La pista escondida no se anima.** Es un cuadro fijo con empuje lento hecho en ffmpeg: sale gratis y no deforma nada.
- Cada cuadro se genera **con la vista de la maqueta y la hoja de personaje como referencia**, nunca solo con texto.
- Nunca la palabra *TikTok* en un prompt de Veo.

## La lista

### Toma 1 · 0,0 – 3,0 s · 3 s · clip con cuadro inicial y final

**Qué se ve.** Primerísimo plano de las manos de Beto apretando el puño del manubrio, con el agua corriéndole por los dedos. La cámara retrocede y en el segundo 2 aparece el plano general: el burro empujando la moto muerta por la carretera de tierra mojada, hacia el único foco prendido, a contraluz.

**Movimiento.** Retroceso desde el detalle al general. Cuadro inicial: las manos. Cuadro final: el plano general a contraluz.

**Sonido.** Viento, lluvia que acaba de parar, pasos en el barro, respiración agitada. Sin música.

**Subtítulo.** Ninguno. Los tres primeros segundos se ganan con imagen y sonido.

**Referencias.** Hoja de Beto *(diseñada, sin generar: `personajes.py`, clave `beto`)* · `referencias/planos-ecuador/03-fachada-taller` · una vista nocturna de la vía.

---

### Toma 2 · 3,0 – 11,0 s · 8 s · clip

**Qué se ve.** Porfirio abre el portón metálico y lo recibe, feliz, con el taller encendido detrás. Luz de trabajo neutra al fondo, la calle en azul. Al borde del cuadro, **Kevin grabando con el celular** — ahí queda presentado sin una línea de diálogo.

**Diálogo.** Porfirio: «¡Bienvenido, bienvenido! Yo llegué igualito, ñaño, empujando mi moto.»

**Sonido.** Cortina metálica subiendo, lluvia goteando del alero, el compresor al fondo.

**Subtítulo.** Palabra en oro: **igualito**.

**Referencias.** `personajes/04-hoja-porfirio` · hoja de Kevin *(no existe todavía)* · `vistas-desde-maqueta/entrada` · `maqueta-ecuador/taller-1-entrada`.

---

### Toma 3 · 11,0 – 17,0 s · 6 s · clip

**Qué se ve.** El recuerdo. El chancho del spot de Lázaro empujando su moto, en gris frío desaturado, con lluvia, cámara en mano y más grano que el resto del episodio. Es el plano que convierte el spot en el origen de la serie.

**Sonido.** Un latido y viento. Nada más.

**Subtítulo.** Ninguno. El recuerdo no habla.

**Referencias.** Los cuadros del spot de Lázaro ya generados · `personajes/04-hoja-porfirio` para que sea reconociblemente él.

---

### Toma 4 · 17,0 – 25,0 s · 8 s · clip

**Qué se ve.** Gallín se agacha junto a la moto y cierra los ojos. No mira: escucha. Cámara a la altura de la moto, él ocupando el alto del cuadro.

**Diálogo.** Gallín: «A ver, arráncalo.» Y la patada que tose y se apaga.

**Sonido.** La patada, el motor que tose dos veces y muere. El detalle técnico que sostiene el episodio: está oyendo si hay chispa.

**Subtítulo.** Palabra en oro: **arráncalo**.

**Referencias.** `personajes/03-hoja-tio-gallin` · `vistas-desde-maqueta/entrada`.

---

### Toma 5 · 25,0 – 33,0 s · 8 s · clip

**Qué se ve.** El diagnóstico, con la gramática fija de la serie: primer plano de Gallín con lente largo y fondo desenfocado, y él casi sin moverse. Mira a Beto, no a la moto.

**Diálogo.** Gallín: «¿Dormiste anoche?» · Beto: «Tres horas.» · Gallín: «Eso no es el motor.»

**Sonido.** Ambiente del taller y las dos lámparas zumbando. Silencio donde va el golpe de la frase.

**Subtítulo.** Palabra en oro: **no es el motor**.

**Referencias.** `personajes/03-hoja-tio-gallin` · hoja de Beto · `vistas-desde-maqueta/banco`.

---

### Toma 6 · 33,0 – 41,0 s · 8 s · clip

**Qué se ve.** La contraseña, con su gramática: plano y contraplano cerrados, la cámara acercándose despacio mientras hablan. Beto duda y baja la voz.

**Diálogo.** Beto: «Vengo por el afinamiento completo.» · Gallín: «¿Y el carro?» · Beto: «El carro está bien.»

**Sonido.** Solo las voces y el goteo. Aquí no hay ningún efecto que distraiga: es la frase que da nombre al club.

**Subtítulo.** Palabra en oro: **EL CARRO ESTÁ BIEN**.

**Referencias.** `personajes/03-hoja-tio-gallin` · hoja de Beto · `vistas-desde-maqueta/banco`.

---

### Toma 7 · 41,0 – 49,0 s · 8 s · clip con cuadro inicial y final

**Qué se ve.** La primera vez que vemos la puerta roja, desde lejos, entre las llantas de la estantería, con la corona dorada en el centro. La gramática de la puerta es siempre la misma: **avance lento hacia la corona**.

**Movimiento.** Avance lento. Cuadro inicial: la puerta lejana entre las llantas. Cuadro final: la corona dorada en el centro del cuadro.

**Sonido.** Braam grave — la firma sonora de la serie — y una cerradura.

**Subtítulo.** Ninguno. Este plano no se explica.

**Referencias.** `vistas-desde-maqueta/estanteria` · `vistas-desde-maqueta/puerta` · `maqueta-ecuador/taller-4-estanteria`.

---

### Toma 8 · 49,0 – 56,0 s · 7 s · clip

**Qué se ve.** Porfirio se ajusta el cinturón un hueco más. Cámara baja, él erguido, luz cálida: es la gramática de la salida, aunque nadie salga todavía. El gesto cuenta el arco de Porfirio sin una palabra.

**Diálogo.** Gallín: «Aquí no se juzga. Se afina.»

**Sonido.** La hebilla del cinturón, clarísima. Es el sonido del episodio.

**Subtítulo.** Palabra en oro: **se afina**.

**Referencias.** `personajes/04-hoja-porfirio` · `personajes/03-hoja-tio-gallin` · `vistas-desde-maqueta/banco`.

---

### Toma 9 · 56,0 – 60,0 s · 4 s · cuadro fijo, sin clip

**Qué se ve.** Macro del calendario en la pared, con un día marcado en rojo: el aniversario de la noche en que Gallín se fue de Guayaquil. Empuje lento hecho en ffmpeg. **Último cuadro del episodio: la pista, nunca una pantalla de marca.**

**Sonido.** Ambiente que se apaga. Sin efecto especial: la pista tiene que poder perderse.

**Subtítulo.** «Si entendiste, comenta EL CARRO ESTÁ BIEN.» Es la mecánica de comentario que le tocó al episodio 1: **contraseña**.

**Referencias.** `vistas-desde-maqueta/banco` para la pared y la luz.

## Continuidad: lo que no puede cambiar entre tomas

Es la lista que hay que pegar en cada prompt, porque es donde Veo se desvía.

| Qué | Cómo está fijado |
| --- | --- |
| Beto | Mojado de arriba abajo en las tomas 1 a 8. La ropa no se seca dentro del episodio |
| La moto | La misma, muerta, sin arrancar nunca. El chupón de bujía partido |
| El piso | Barro y charcos afuera, piso de resina gris claro con líneas amarillas adentro |
| La hora | Noche cerrada de principio a fin. La lluvia acaba de parar, no está lloviendo |
| La luz | Taller con luz de trabajo neutra, y solo sobre el banco las dos lámparas ámbar |
| El gallo del letrero | Un solo objeto, siempre en el mismo lugar, con el neón prendido porque es de noche |
| Porfirio | El cinturón se ajusta **una sola vez**, en la toma 8. Antes va flojo |
| Kevin | Solo en la toma 2, al borde del cuadro, grabando. No habla |
| Yadira | No aparece: ya se fue, y eso es lo que obliga a Gallín a meterse con la moto |

## Lo que cuesta

| Concepto | Cantidad | Créditos |
| --- | --- | --- |
| Cuadros iniciales | 9 | 27 |
| Cuadros finales de las tomas con movimiento | 2 | 6 |
| Clips de video | 8 | 32 |
| **Firme** | | **65** |
| Repeticiones, calculando un 50 % | | hasta 33 |
| **Techo realista** | | **98** |

El cuadro fijo de la toma 9 no gasta video, y el empuje lo hace ffmpeg gratis.

## Lo que falta antes de generar el primer cuadro

**Beto Chóez ya está diseñado** — ficha completa en la pestaña *Personajes a fondo* de la biblia, y el prompt cargado en `codigo/personajes.py` con la clave `beto`. Falta **generarlo**: tres créditos. Sale en seis de las nueve tomas, así que sin hoja es un burro distinto en cada plano.

**Y una regla que salió de diseñarlo:** la hoja se genera **seco**. El agua es condición del episodio 1 y va en el prompt de cada cuadro. Una hoja mojada contamina todos los episodios en que Beto vuelva.

Y esto no es solo del episodio 1: **cada episodio tiene su cliente invitado** —Don Ramiro el carnero, Chito el colibrí, y los demás— y ninguno tiene hoja. Son ocho hojas más, 24 créditos, que no están en ningún bloque del plan. Conviene generarlas todas juntas, con el mismo estilo, antes de empezar la temporada.

**Falta la hoja de Kevin**, que ya estaba en el plan, porque aparece en la toma 2.

**Y falta resolver los dos defectos que se arrastran:** el plumaje de Gallín en primeros planos, que aquí importa mucho porque las tomas 4, 5 y 6 son primeros planos suyos, y la nariz de Porfirio, que sale en las tomas 2, 3 y 8.

## Una decisión de formato, a tu criterio

El análisis de mercado dice que en este formato el episodio 1 de una serie es **la mitad de largo** que los demás: es anzuelo, no capítulo. El nuestro mide igual que los otros siete.

Si quisieras la versión corta, de **44 segundos**, se cae la toma 3 —el recuerdo del chancho— y se acortan las tomas 2, 5 y 8. No lo hice por mi cuenta porque el recuerdo es lo que amarra el spot de Lázaro con la serie, y eso no es un detalle de ritmo: es la puerta de entrada de toda la ficción. La decisión es tuya.

## El paso siguiente

Con Beto y Kevin definidos, escribir los **once prompts de cuadro** y los **ocho prompts de movimiento**, con el bloque de continuidad pegado en cada uno. Eso tampoco cuesta créditos: el gasto empieza cuando se manda a generar.
