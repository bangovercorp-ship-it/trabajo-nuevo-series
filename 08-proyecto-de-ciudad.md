# Proyecto de ciudad · Puerto Candela

Esto es lo que faltaba. La biblia describe el taller lote por lote y del pueblo dice cuatro cosas: llanura aluvial del Guayas, quince kilómetros del mar, lluvia de enero a abril, salitre. Con eso no se puede abrir un capítulo con la ciudad, porque cada toma la inventa distinta.

Aquí está el pueblo entero: qué hay alrededor, cómo es cada calle, cómo es el parque, de qué color es todo y desde dónde se mira.

**Regla de certeza, igual que en las oficinas técnicas.** Todo va etiquetado:

| Etiqueta | Qué significa |
| --- | --- |
| **DATO** | Está escrito en la biblia o es geografía general verificable de la costa del Guayas |
| **PROPUESTA** | Lo decide este proyecto. Es coherente con el dato y no lo contradice |
| **HIPÓTESIS** | Hay que validarlo con alguien de la costa antes de darlo por cierto |

---

## 1 · El territorio

**El problema:** la biblia no dice qué hay más allá del barrio. ¿Cerros? ¿Bosque? ¿Desierto? Sin respuesta, la primera toma aérea inventa un paisaje y la segunda inventa otro.

**Lo que sí está fijado (DATO):** llanura aluvial, suelo blando, 23 a 34 °C, húmedo todo el año, estación lluviosa de enero a abril y seca el resto, riesgo de inundación en años de El Niño, zona sísmica alta, salitre a 15 km del mar, sol duro de 11 a 15 h y cielo blanco.

**Lo que se propone, y por qué.**

### El Estero Candela

Es la pieza que ordena todo lo demás. Un estero de marea al sureste del pueblo, que sale al Golfo de Guayaquil.

Resuelve cuatro cosas de una vez:

1. Explica por qué el pueblo se llama **Puerto** Candela sin necesidad de playa.
2. Explica la **Calle El Puerto**, que ya estaba en el plano urbano y hasta ahora no iba a ninguna parte. Ahora baja al muelle.
3. Explica el salitre a 15 km del mar: entra por el estero.
4. Explica de qué vive la gente. Camarón y arroz.

Etiqueta: **PROPUESTA**. La biblia no lo nombra, pero nada de lo que dice lo contradice, y sin algo así el nombre del pueblo queda sin explicación.

### Lo demás del paisaje

| Pieza | Etiqueta | Qué es | Por qué |
| --- | --- | --- | --- |
| Bosque seco tropical | DATO | Pasto seco, rastrojo, matorral, ceibos sueltos | Es lo que hay en la llanura del Guayas. **Ni desierto ni selva** |
| Camaroneras | PROPUESTA | Damero de piscinas a los dos lados del estero | Es el paisaje real del Guayas bajo, y desde el aire es inconfundible |
| Arrozales | PROPUESTA | Damero verde al norte y al oeste | Regadío: verdes también en verano |
| Manglar | PROPUESTA | Franja oscura en las dos orillas del estero | Va con el estero |
| Loma de la Cruz, +96 m | **HIPÓTESIS** | Elevación aislada al noroeste, con asentamiento en la ladera | En la llanura hay lomas aisladas, pero **la biblia dice llanura y no nombra ninguna**. Sirve para abrir capítulos con el pueblo visto desde arriba. **Si se cae, hay que buscar otro punto alto** |
| Carretera | PROPUESTA | La Av. El Cruce sale al este y se vuelve carretera | La gasolinera El Último ya estaba «donde empieza la carretera» |

### Las dos estaciones, y cuál se rueda

Esto cambia el color de la ciudad entera, así que es una decisión, no un detalle.

- **Verano, mayo a diciembre.** Seco. Todo ocre, el ceibo del campo sin una hoja, polvo en las calles sin asfaltar, sol duro y cielo blanco.
- **Invierno, enero a abril.** Llueve de tarde. El monte se pone verde en seis semanas, las calles de lastre se vuelven barro, el estero sube.

**Se rueda en verano**, porque es la luz que la biblia ya fijó: sol duro de 11 a 15 h y cielo blanco. El invierno queda guardado para un capítulo de aguacero, que además es mejor si es la excepción. En el código es un parámetro: `est: 'seca' | 'lluviosa'`.

Una excepción que importa: **el arbolado de calle está regado y no pierde la hoja.** Solo el ceibo del campo se queda pelado. Sin esa distinción, la avenida en verano es una fila de postes grises y no se puede grabar nada ahí.

---

## 2 · Los barrios

Puerto Candela tiene **unos 12.000 habitantes** (HIPÓTESIS, ya estaba en la biblia). En el casco modelado caben unos 8.000; el resto vive en recintos dispersos de la parroquia, que es como funciona de verdad un pueblo rural de la costa.

| Barrio | Qué es | Cómo se ve |
| --- | --- | --- |
| **El Cruce** | El centro. 2.232 hab, 25 manzanas, 496 lotes | Es el que ve la cámara. Comercio en los dos frentes de la avenida, vivienda detrás |
| **Nuevo Amanecer** | Al norte. El pueblo que crece | Misma traza, peor acabado: más bloque sin enlucir, más varillas al aire, ninguna calle asfaltada |
| **Los Almendros** | Al oeste. El barrio viejo | Lotes más grandes, más patio, más árbol |
| **El Muelle** | Al sureste, camino al estero | Pescadores, bodegas, oficinas de camaronera |
| **La Loma** | En la ladera (HIPÓTESIS) | Asentamiento informal, casas apoyadas en la pendiente |
| **Zona industrial** | Al sur de la Calle Juan Montalvo | Naves sueltas de zinc, no una losa continua |

---

## 3 · Propuesta de cada calle

El plano urbano dice dónde va cada calle y cuánto mide de ancho. No decía cómo es por dentro. Ahora sí. Dibujo: `10-secciones-viales.png`.

**La decisión de fondo: en un pueblo de 12.000 habitantes no está todo asfaltado.** Eso no es un descuido, es lo que hay. Y además da dos climas de imagen: polvo en verano, barro de enero a abril.

| Vía | Ancho | Pavimento | Árbol | Alumbrado |
| --- | --- | --- | --- | --- |
| **Av. El Cruce** | 40,00 m | Asfalto. Doble calzada de 9,00 + 2,00 de estacionamiento, parterre central de 4,00, veredas de 7,00 | **Ceibo** en el parterre, cada 22 m | Doble, sobre poste de 9,20 m |
| **Calle Olmedo** | 20,00 m | **Adoquín**. Calzada 12,00, veredas 4,00 | **Almendro** cada 17 m, alternado | Simple, poste de 7,60 m |
| **Calles locales** | 12,00 m | **Lastre compactado**. Calzada 7,00, veredas 2,50 | **Mango**, solo en las esquinas | En el poste de la luz, cada 60 m |
| **Pasaje La Esperanza** | 5,00 m | Adoquín de vereda a vereda, sin bordillo | Ninguno | Tres faroles, y **solo funciona el de la puerta gris** |

**Por qué adoquín en Olmedo y no asfalto:** el adoquín se levanta y se vuelve a poner. En la calle de los mecánicos se abren zanjas todo el tiempo.

**Por qué el mango va solo en las esquinas:** en 2,50 m de vereda, un árbol cada 20 m no deja pasar a nadie.

**Dos huecos a propósito en el arbolado.** No se planta en el cruce de Olmedo con la avenida, ni delante del toldo del taller. En los dos sitios el árbol tapaba la toma. Lo descubrí renderizando: un almendro se plantó justo delante de la cámara nocturna.

---

## 4 · El Parque del Reloj

La biblia decía «Parque del Reloj, con su torre que atrasa». Nada más. Una manzana verde con una torre no es un diseño: es un hueco donde cada toma pone lo que quiere. Dibujo: `11-parque-del-reloj.png`.

**Manzana G, 100,00 × 44,00 m.** Se organiza como se organiza una plaza de pueblo costeño:

- Banda dura de 3,00 m en todo el perímetro, que es por donde camina la gente.
- Dos diagonales de esquina a esquina que cruzan en una rotonda de Ø 16,00 m.
- Cuatro cuadrantes de césped entre las diagonales.
- **Torre del reloj** de 2,50 × 2,50 y 12,20 m en el cruce. Se ve desde las cuatro esquinas y desde la avenida: es la referencia que necesita una toma de la ciudad para saber dónde está.

Los usos, repartidos para que no se estorben:

| Dónde | Qué | Por qué ahí |
| --- | --- | --- |
| Oeste | Cancha de **ecuavóley** 18 × 20, red a 2,85 m | Hace ruido y junta gente de pie. Lejos de la concha y de los juegos |
| Este | **Juegos infantiles** sobre arena | A la vista desde las bancas, con tres mangos grandes dando sombra encima |
| Este, al fondo | **Concha acústica**, tarima 16,00 × 6,00 | Mira hacia adentro: el público se para en el césped. Aquí se hace la fiesta patronal |
| Oeste | Busto y astabandera | El remate del eje corto |

**Vegetación:** 5 mangos (la sombra de verdad), 4 almendros en el perímetro, 4 guayacanes uno en cada entrada —florecen amarillo en verano— y 2 palmas flanqueando la torre, y solo ahí.

**Mobiliario:** 24 bancas de hormigón de 1,80 m, 8 faroles de 4,20 m, 6 basureros. **Sin cerramiento**: el parque no se cierra con reja, se cruza.

**Pavimento:** adoquín en dos tonos, el claro en las diagonales y el oscuro en la banda perimetral, para que el cruce se lea desde el aire.

---

## 5 · Propuesta de color de la ciudad

**La regla que lo sostiene todo, y no se toca:**

> En todo Puerto Candela **no hay otro edificio negro ónix ni otro verde botella**. El taller y el bar son los únicos. Por eso se reconocen desde cualquier ángulo y a cualquier hora, y por eso los dos neones se leen de lejos.

Lo demás:

| Qué | Color | Por qué |
| --- | --- | --- |
| Vivienda | Bloque enlucido y pintado en colores fuertes pero gastados por el sol y el salitre | Lo fija la biblia. Nada saturado: todo con tiza |
| Zócalo | Un tono más oscuro que el muro, 0,40 m | Se pinta así para que el barro no se note |
| Medianeras | Ciegas. Los lotes se pegan | Es como funciona un lote entre medianeras |
| Traseras | Bloque sin enlucir en una de cada tres | La cara que nadie mira |
| Equipamiento | Blanco y azul del Estado | Deliberadamente distinto de las casas: desde el aire se lee al instante dónde está la escuela y dónde el UPC |
| Cubiertas | Zinc en tres tonos: nuevo, viejo y oxidado | Con un solo tono el barrio se ve de cartón |
| Comercio | Banda de rótulo de color plano sobre la persiana | Las letras las pone la imagen final, no la maqueta |

**Detalles que hacen que sea Ecuador y no un pueblo genérico:** rejas en todas las ventanas de planta baja; cables cruzando la calle; tanque de agua y antena en la azotea; una de cada cinco casas de dos pisos con la loza sin terminar y las varillas al aire esperando el otro piso; portales sobre la vereda para la sombra. Todo eso lo pedía la biblia y no estaba en la maqueta vieja.

**No hay personas en la maqueta, a propósito.** Una figura humana mal hecha en la imagen de referencia se le contagia al video generado. Las personas entran después, en la generación, con sus hojas de personaje.

---

## 6 · Las tomas oficiales del pueblo

Si un capítulo abre con la ciudad, abre desde una de estas y no desde otra. Están todas en `codigo/remotion-src/Ciudad3D.tsx`, con su cámara, su lente y su hora.

### Horizontales · 2560 × 1440

| # | Toma | Hora | Para qué |
| --- | --- | --- | --- |
| 1 | `territorio` | Tarde | El pueblo en la llanura: estero, camaroneras, arrozales, la loma |
| 2 | `ciudad_aerea` | Tarde | **La de abrir temporada** |
| 3 | `ciudad_cenital` | Mediodía | Se lee la traza entera: la avenida, el parque, el mercado |
| 4 | `ciudad_sur` | Tarde | El pueblo con el estero detrás |
| 5 | `la_cuadra` | Tarde | La manzana del taller |
| 6 | `la_esquina` | Tarde | El taller y el bar enfrentados por la avenida |
| 7 | `avenida` | Mediodía | Teleobjetivo: comprime la calle y el taller queda al fondo |
| 8 | `olmedo` | Tarde | La calle de los mecánicos |
| 9 | `parque` | Tarde | El Parque del Reloj |
| 10 | `mercado` | Mediodía | El mercado y la fila de la avenida |
| 11 | `esquina_noche` | Noche | **Los dos neones. Es la firma visual de la serie** |
| 12 | `ciudad_noche` | Noche | El pueblo encendido desde el aire |
| 13 | `estero` | Tarde | El muelle: de qué vive el pueblo |
| 14 | `loma` | Amanecer | El pueblo desde arriba con bruma |
| 15 | `carretera` | Tarde | Entrando al pueblo, pasando la gasolinera |
| 16 | `nuevo_amanecer` | Mediodía | El pueblo que crece sin asfalto |

### Verticales · 1440 × 2560

La serie es vertical. **Una toma pensada en horizontal no sirve recortada:** hay que acercar y subir la cámara. Por eso hay ocho reencuadres propios, no recortes: `v_ciudad`, `v_avenida`, `v_taller`, `v_esquina`, `v_parque`, `v_esquina_noche`, `v_loma`, `v_estero`.

### Las cuatro horas

| Hora | Sol | Cómo se ve | Para qué sirve |
| --- | --- | --- | --- |
| `mediodia` | 76° | Cielo blanco, sombra corta y dura | **Es la luz de la serie**, la que fijó la biblia |
| `tarde` | 20° | Sombra larga, color caliente | Las tomas de apertura |
| `amanecer` | 9° | Bruma sobre la llanura, azul frío | El pueblo desde la loma |
| `noche` | −2° | Hora azul, no negro cerrado | Mandan los neones y el alumbrado |

**Por qué la noche no es negra:** en negro absoluto la imagen no le sirve al generador de video, que necesita ver la forma. Queda cielo azul profundo con resto de luz en el horizonte, y mandan las dos luces de la serie.

Ecuador está sobre la línea: **el sol sale a las 6:15 y se pone a las 18:20 todo el año, y al mediodía cae casi vertical.** El atardecer es corto y hay que rodarlo rápido.

---

## 7 · Cómo está hecho

Nada de esto usa un solo archivo de imagen. Todo es procedural y determinista.

- **Semilla fija** (`SEMILLA = 20260925`). El mismo lote saca siempre la misma casa, del mismo color, con el mismo techo y el mismo óxido en el zinc. **La ciudad es reproducible entre capítulos.** Cambiar la semilla cambia el pueblo entero, así que no se toca.
- **Cielo físico** (modelo de Preetham) con el sol en su posición real, e **iluminación por imagen**: el cielo ilumina la escena, no una lámpara inventada.
- **Texturas generadas por código**: enlucido con humedad en el pie del muro, zinc acanalado con su mapa de relieve y su óxido, adoquín, lastre con las dos huellas de las llantas, asfalto, arrozal, camaronera.
- **Techos a dos aguas**, como manda la biblia. La maqueta anterior los tenía planos.

Motor: `codigo/remotion-src/realismo.tsx`. Ciudad: `codigo/remotion-src/Ciudad3D.tsx`.

Render: `npx remotion render src/index.ts Ciudad3D salida --sequence --image-format=png --gl=swangle`. Unos 50 segundos por toma. **Cero créditos: es todo código.**

---

## 8 · Lo que falta validar

| Qué | Por qué importa |
| --- | --- |
| **La Loma de la Cruz** | La biblia dice llanura y no nombra ninguna elevación. Si se cae, hay que buscar otro punto alto para las tomas de apertura |
| **El estero y el muelle** | Toda la economía del pueblo cuelga de esto |
| **El peso del camarón frente al arroz** | Cambia quién es el cliente típico del taller |
| **La advocación de la iglesia** | La biblia ya la marcaba como VALIDAR. De ahí sale la fecha de la fiesta patronal |
| **Anchos mínimos de vereda y retiro frontal** | Los fija la ordenanza del cantón, que no se ha consultado |
| **La distancia exacta a Guayaquil** | Importa para la temporada 2 |

## 9 · Una contradicción encontrada en la biblia

En la pestaña *Ecuador · taller y barrio*, el párrafo de población sigue diciendo **«Puerto Palmar: unos 12.000 habitantes»**, mientras que el resto de la pestaña ya dice **Puerto Candela**. Es un resto del cambio de nombre. Hay que corregirlo: el pueblo se llama Puerto Candela.
