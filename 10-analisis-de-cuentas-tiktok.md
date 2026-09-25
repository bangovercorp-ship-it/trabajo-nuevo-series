# Cómo trabajan las cuentas de series hechas con IA

Análisis del 25 de septiembre de 2026, sobre cuatro cuentas que el dueño del proyecto señaló, más una serie completa desarmada episodio por episodio. Sirve para el rol 10 del tablero, que estaba en cero.

## Cómo se obtuvo, y qué no se pudo obtener

Los datos salen del HTML que TikTok sirve a los buscadores, leído con el navegador sin ventana que ya está instalado en la máquina. **Nada está inventado ni estimado:** cada cifra de este documento viene de ese HTML.

Lo que quedó cerrado, y por qué: la grilla de publicaciones de un perfil pide resolver un captcha de deslizar, y los captchas no se resuelven. Y **desde el episodio 2 de una serie, TikTok exige iniciar sesión** — literalmente dice *«Log in to start watching»*. Así que de cada serie solo se puede leer el episodio 1 sin cuenta.

## Las cuatro cuentas

| Cuenta | Creada | Edad | Seguidores | Corazones | Corazones por seguidor |
| --- | --- | --- | --- | --- | --- |
| @ferriswheel_drama_mx | 6 jul 2026 | 81 días | 1.460 | 54.959 | 37,6 |
| @infinitedrama_mx | 11 jun 2026 | 106 días | 7.149 | 186.010 | 26,0 |
| @stardusttv_shxc | 22 feb 2021 | 5 años y medio | 593.219 | 7.022.870 | 11,8 |
| @stardusttv_hits | 1 sep 2026 | 24 días | 279.623 | 5.487.480 | 19,6 |

- **Es una red, no cuatro cuentas.** Las dos `stardusttv` son la misma marca: una de 2021 que sostiene y una de hace 24 días que multiplica. El sufijo `_mx` de las otras dos, con la biografía escrita en inglés, es una fábrica que saca una cuenta por mercado desde un solo catálogo.
- **Ninguna sigue a nadie** (cero seguidos; uno en un caso). Son emisores puros: no responden, no comentan, no construyen comunidad.
- **Mientras más chica la cuenta, más corazones por seguidor.** El contenido viaja y gusta, pero no convierte en seguidor.
- **El embudo está afuera.** `@stardusttv_shxc` manda a `link.stardust-tv.com`, y TikTok marca ese enlace con **riesgo 3** en sus propios datos. Las tres cuentas nuevas no tienen enlace en la biografía: la vieja carga el embudo, las nuevas juntan público.
- `@infinitedrama_mx` dice **«AI Anime Dramas»** en la biografía: no esconden que es IA.

## El hallazgo grande: no publican videos, publican series

El enlace que se analizó no es una publicación normal. Es el **formato oficial de series cortas de TikTok**, con su propia dirección: `tiktok.com/shortdrama/episode/<idSerie>/<numero>`. TikTok tiene producto propio para esto, con numeración de episodios, portada de serie, etiquetas de género de su propio catálogo y muro de inicio de sesión.

### La serie, por dentro

| Dato | Valor |
| --- | --- |
| Nombre maestro | *The Apocalypse Princess's Escort* |
| Título en español | *Escolta de la princesa letal* |
| Descripción traducida | *Misión Apocalipsis: El Escolta* |
| Episodios | **120** |
| Duración total | 7.608 s = **2 h 7 min** |
| Promedio por episodio | **63,4 s** |
| Vistas de la serie completa | 823.630 |
| Géneros que le puso TikTok | Adventure · Martial Arts · Contract Lovers |
| Publicada como | idioma `es`, país `MX` |
| Declarada como IA | **No.** El campo de contenido generado por IA va en falso |

Tres nombres distintos para la misma serie, y el maestro en inglés: es un catálogo traducido, no una serie escrita en español.

### El episodio 1 es un anzuelo de 31 segundos

Está marcado en los datos como **intro gratis** y **destacado**, mide 31 segundos —la mitad del promedio de la serie— y **está pautado**: el campo de anuncio va en verdadero. Las vistas del primer episodio son compradas.

| Episodio | Corazones | Comentarios | Guardados | Compartidos |
| --- | --- | --- | --- | --- |
| 1 (gratis, 31 s, pautado) | 4.723 | 12 | 2.438 | 360 |
| 2 (tras el muro) | 1.222 | 18 | 647 | 102 |
| 3 (tras el muro) | 950 | 7 | 299 | 27 |

El episodio 1 tuvo **79.100 vistas**. Sobre esa base: 6,0 % de corazones, 3,1 % de guardados, 0,46 % de compartidos y **0,015 % de comentarios**. Del episodio 1 al 2 se cae el 74 % de los corazones: ese es el precio del muro de inicio de sesión.

> Las cifras de los episodios 2 y 3 se leyeron de la página renderizada, en el orden en que TikTok las muestra. El orden se verificó contra el episodio 1, donde sí hay datos crudos.

## Qué de esto nos sirve, y qué no

**Lo que confirma que vamos bien.** El promedio de 63 segundos por episodio es exactamente el largo que ya tiene planeado *El Taller del Tío Gallín* (siete u ocho planos de 8 s). El formato no hay que discutirlo más: el mercado ya lo fijó ahí.

**Lo que hay que copiar.** El episodio 1 más corto que los demás, hecho para engancharse y no para contar. El nuestro dura lo mismo que los otros siete.

**Lo que no hay que copiar.** Su catálogo son 120 episodios; el nuestro son 40 en cinco temporadas. No es el mismo animal: ellos venden volumen de ficción, nosotros contamos una sola historia para una marca. Tampoco su embudo: mandan a una app de afuera, con un enlace que TikTok marca como riesgoso.

**La decisión que esto fuerza, y es del rol 10.** Este formato consigue guardados, no conversación: 3,1 % de guardados contra 0,015 % de comentarios. La meta que tiene escrita nuestra estrategia —más de 10 comentarios por cada 1.000 vistas, o sea 1 %— es **66 veces** lo que consigue este formato. Las dos cosas no caben juntas:

- **Publicación normal**, como está planeado: se puede jugar la contraseña en los comentarios, la pista escondida y las respuestas en personaje. Se gana conversación, no hay muro, y cada episodio pelea solo por su alcance.
- **Formato de series cortas de TikTok**: se gana el botón de episodio siguiente y la numeración nativa, y se pierde la conversación. Falta verificar si una marca puede publicar ahí o si está reservado a productoras registradas en su programa de series.

Recomendación: **publicación normal para la temporada 1**, porque las mecánicas de comentario son la única ventaja que tenemos sobre estas cuentas, y ellas no las usan. El formato de series se evalúa para la temporada 2, cuando ya haya público que quiera seguir de corrido.

## Lo que falta verificar

- Si el formato de series cortas de TikTok admite marcas o solo productoras de su programa.
- Cuántos episodios tiene cada cuenta y con qué frecuencia publican. Requiere la grilla, que está tras el captcha: se resuelve con la sesión de Chrome del dueño, si él lo autoriza.
- El lenguaje visual plano por plano. Eso no sale de los datos: hay que reproducir el episodio y capturar cuadros.
