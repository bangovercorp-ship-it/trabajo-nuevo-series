# Qué falta para pasar a producción

Auditoría del 25 de septiembre de 2026, contra el repositorio y las ocho pestañas de la biblia. No repite el tablero: lo usa para responder una sola pregunta, **qué falta para producir**, y distingue dos cosas que hasta ahora estaban mezcladas: lo que falta para **producir** un episodio y lo que falta para **publicarlo**.

## Lo primero, porque cambia el plan y ahorra créditos

El plan de trabajo tiene el orden invertido. Hoy dice: Bloque 2, generar 99 créditos de imágenes de escenarios; y después, Bloque 5, desglosar el episodio 1 en tomas.

Eso genera por catálogo antes de saber qué pide la historia. El episodio 1 pasa **dentro del taller**: no necesita las cuatro caras del bar, ni los exteriores del pueblo, ni la aérea de la ciudad. Y del otro lado, `codigo/vistas_ciudad.py` propone 24 vistas de ciudad por 72 créditos, que tampoco entran en el episodio 1.

**Corrección: la lista de planos va antes que las imágenes.** Primero el rol 7 dice qué ocho planos tiene el episodio 1; después se generan solo esas referencias. Las demás se generan cuando el episodio que las necesita entre en producción. Cuesta cero hacer el cambio y evita gastar créditos en imágenes que van a esperar semanas, con el riesgo de que para entonces la hoja de personaje haya cambiado y haya que rehacerlas.

## Lo que está terminado

**En papel, y es la mayor parte del trabajo.** La biblia tiene ocho pestañas. Los 40 episodios de las cinco temporadas están escritos, con el final definido y el villano sembrado. La temporada 1 está auditada: ocho no conformidades encontradas y corregidas. El expediente técnico del taller tiene sus 26 zonas, su capacidad real y su organigrama. La biblia sociocultural está escrita con fuentes ecuatorianas y con sistema de certeza. El pueblo entero está proyectado: territorio, cinco barrios, sección de cada calle, Parque del Reloj, color y paisajismo. Y el reparto de productos quedó decidido, uno por temporada.

**En código, 37 archivos.** Los planos se dibujan solos, la maqueta 3D del taller y del bar tiene la geometría depurada, hay motor de render realista con cielo físico y materiales por código, y los prompts de generación y de montaje ya están afinados a costa de créditos gastados.

**En referencias, 117 imágenes** en JPG liviano, con su vigencia y sus defectos anotados una por una.

**En estándares.** El acabado de cine, el corte sobre la grilla de golpes probado en el promocional, el método plano → maqueta → imagen, y las trampas de Veo aprendidas: nunca la palabra TikTok en un prompt, cuadro inicial y final en toda toma con movimiento, y *EXACTLY THREE* cuando se piden tres cosas.

**Y desde hoy, datos de mercado reales**, no suposiciones: cuatro cuentas de series con IA desarmadas y una serie completa medida por dentro. Está en `10-analisis-de-cuentas-tiktok.md`.

## Lo que se corrigió, que es la parte que no se ve

| Qué estaba mal | Cómo quedó |
| --- | --- |
| La serie era peruana | Migrada entera a la costa de Ecuador, incluidos los restos: *La Capital*, *jirón*, «voces de Lima», *causa*, DIGESA y «etiqueta al pata» |
| Los clientes llegaban por un problema personal, no por el carro — y entonces los empleados sobraban | El vehículo **siempre** está roto de verdad y el trabajo se ve en cámara |
| Yadira y Kevin no tenían episodio | El 5 pasa a ser de Yadira sin tocar el humor, y a Kevin se le propuso herida |
| El villano entraba en el último minuto de la temporada | Dos siembras que no cuestan un guion |
| Ningún cliente volvía | Desde el episodio 2 vuelven al fondo; en el 8 están los cinco |
| El producto se veía una vez en ocho episodios | La misma bolsa, sin abrir y sin explicar, desde el episodio 4 |
| Una llanta pinchada se cambia en seis minutos y el episodio necesitaba que tardara | Tuerca de seguridad y la llave en la caja, sin abrir |
| Tres episodios abrían con plano general, muerto en vertical | Reencuadre vertical propio para las ocho tomas |
| Todas las invitaciones a comentar eran «etiqueta a» | Cinco mecánicas rotando |
| El campo salió de arena en el primer render | Bosque seco tropical: pasto seco, rastrojo, ceibos |
| Los techos estaban planos | A dos aguas, como pedía la biblia |
| La pestaña *Estrategia y producción* no estaba listada en ninguna parte, y por eso nadie la actualizó | Listada, y sus cuatro datos viejos corregidos |
| Los planos figuraban «aprobados» y «por rehacer» a la vez | La geometría está aprobada, el dibujo se rehizo |
| El trabajo de la nube estaba solo en una rama | Consolidado en `main` |

## Para producir el episodio 1

Tres cosas, y ninguna depende de nadie de afuera.

**1 · La lista de planos del episodio 1.** No existe. Es del rol 7, cuesta cero créditos y se puede hacer hoy con lo que ya hay. Es lo que define todo lo demás.

**2 · Dos defectos que se arrastran a cada imagen nueva.** El plumaje de Gallín pierde consistencia en primeros planos y la nariz de Porfirio cambia entre imágenes. Hay que resolverlos en una prueba corta, de pocos créditos, **antes** de gastar el bloque grande: si no, se pagan dos veces.

**3 · Las referencias que pida esa lista, y solo esas.** Con el episodio 1 dentro del taller, son las vistas del taller desde la maqueta y las dos hojas de personaje que faltan, Yadira y Kevin. Del bloque de 99 créditos, el episodio 1 necesita una fracción.

**Costo de tener el episodio 1 en la mano:** unos 85 créditos de generación —8 cuadros, 8 clips y un 50 % extra de repeticiones— más las referencias que pida la lista de planos. De los 1.744 disponibles, sobra de más.

**Y dos decisiones tuyas que sí bloquean.** La Bahía 0 —dentro del pasillo o bajo el toldo— cambia la planta del taller, y la planta es la referencia de toda imagen del taller. Y el origen de Gallín cambia cómo lo trata el pueblo, que es tono de actuación. Las dos están en el tablero con recomendación.

## Para publicarlo, que es otra cosa

Aquí está el problema de verdad, y no lo resuelve esta máquina.

**Cumplimiento ante la ARCSA: sin empezar.** Cambió el país y cambió la autoridad. Nadie ha verificado qué se puede afirmar en una pieza publicitaria en Ecuador, qué registro sanitario debe tener cada producto, ni qué exige TikTok para el rubro de salud masculina. Y ahora no es un producto, son cinco: cada uno que se abra en el gabinete arrastra su propia revisión. **Mientras esto no esté revisado, se puede producir todo y publicar nada.** Lo tiene que contestar la empresa con su asesor, no un chat.

**Validación del habla: la mitad.** La biblia sociocultural está escrita y con fuentes, pero hay seis puntos que necesitan que una persona de la costa los lea: el sector de Guayaquil del Centro Gallardo, la migración a España e Italia —que es la herida de Kevin—, las gasolinas Extra y Súper del episodio 3, cómo es un velorio en la costa, qué vende de verdad un bar de pueblo, y los precios en dólares de cada arreglo que se nombre. Más el vocativo *ñaño*. Un acento falso se detecta en tres palabras.

**Estrategia de publicación: a medias desde hoy.** Ya hay datos de mercado y una recomendación de formato. Falta lo administrativo: la cuenta, el nombre de la serie en Ecuador, la frecuencia, el orden de estreno, y decidir entre publicación normal y el formato de series cortas de TikTok.

**Voces: a medias.** La clave funciona y hay 23.736 caracteres hasta el 25 de octubre, pero el reparto está sin elegir y las cuatro pruebas hechas son de acento neutro. Conviene elegir las voces antes de producir, porque la voz cambia el ritmo del montaje. Y conviene no grabar las definitivas antes de la validación del habla.

## El cuello de botella, dicho sin vueltas

Todo lo que depende de esta máquina se puede terminar en días y con créditos de sobra. **Lo que no depende de esta máquina son dos cosas, y las dos están sin arrancar:** el cumplimiento ante la ARCSA y la persona de la costa que lea el habla.

Si esas dos no se empiezan ahora, va a llegar el momento de tener la temporada entera producida, guardada y sin poder publicarse. Ninguna de las dos cuesta créditos. Las dos cuestan conseguir a una persona.

## El orden que recomiendo

1. **Hoy, gratis:** contestar las dos decisiones del tablero y las cinco del plan de temporadas. Y pedirle a la empresa el cumplimiento y a un conocido de la costa que lea el habla.
2. **Sin créditos:** la lista de planos del episodio 1.
3. **Pocos créditos:** la prueba que arregla el plumaje y la nariz.
4. **Unos 85 créditos más las referencias del episodio 1:** producir el episodio 1 completo, con sonido real y subtítulos.
5. **Con el episodio 1 en la mano:** decidir si el resto se produce de corrido o se ajusta. Recién ahí gastar el resto del bloque de imágenes.
6. **En paralelo todo el tiempo:** las voces costeñas.
