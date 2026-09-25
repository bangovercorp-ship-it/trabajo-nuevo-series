# El código que ya existe

Copia fiel de los scripts que viven en `C:\pesonajes para videos\`. Están aquí para que
cualquier sesión, incluso una que corre en la nube sin acceso al disco, pueda **leer los
prompts ya afinados y corregirlos, en vez de escribirlos de nuevo.**

Dos advertencias antes de tocar nada:

- **Las rutas son de Windows y absolutas.** Fuera de esa máquina no corren tal cual: sirven
  como fuente de los prompts y de la lógica, no como programa portable.
- **Ninguna clave está aquí.** Todos los clientes leen su clave de `C:\JUEGOS APP\.secretos\`.
  Verificado archivo por archivo antes de subir.

## Clientes de API

| Archivo | Qué es |
| --- | --- |
| `snapgen.py` | Cliente de SnapGen: imagen con Nano Banana Pro, video con Veo 3.1 Fast. Lo usan casi todos los demás |
| `voz.py` | Cliente de ElevenLabs: `cuenta`, `voces`, `di <voice_id> salida.mp3 "texto"` |
| `freesound.py` | Baja efectos reales, solo CC0 |

## La serie · lo que hay que rehacer para Ecuador

| Archivo | Qué contiene | Estado |
| --- | --- | --- |
| `personajes.py` | Los prompts de las hojas de personaje del elenco | Falta Yadira y Kevin |
| `laminas.py` | Láminas de expresiones y de poses | Hecho para el elenco viejo |
| `escenarios.py` | Arte de concepto de los escenarios | **Todo es versión Perú** |
| `vistas_reales.py` | Convierte cada vista de la maqueta en foto realista | Sirve tal cual |
| `planos_diseno/comun.py` | Fuentes, salida, paleta y la clase de elevación compartida | Portable |
| `planos_diseno/plano_urbano.py` | El plano del barrio | Ecuador, verificado: 496 lotes, 25 mz, 2.232 hab |
| `planos_diseno/plano_taller.py` | Planta y fachada del taller, con las 9 zonas y el +0,40 | Ecuador |
| `planos_diseno/plano_taller_caras.py` | Las cuatro caras del taller y su cubierta, con materiales | Ecuador |
| `planos_diseno/plano_bar_pasaje.py` | Planta del bar y del pasaje | Ecuador |
| `planos_diseno/plano_bar_caras.py` | Las cuatro caras del bar y su cubierta | Ecuador |
| `planos_diseno/plano_territorio.py` | **Puerto Candela en su territorio: estero, camaroneras, arrozales, la loma** | Nuevo |
| `planos_diseno/plano_secciones_viales.py` | **Las cuatro calles en sección, con su pavimento y su árbol** | Nuevo |
| `planos_diseno/plano_parque.py` | **El diseño del Parque del Reloj** | Nuevo |
| `remotion-src/realismo.tsx` | **El motor de render: cielo físico, texturas por código, techos a dos aguas, árboles, cables** | Nuevo |
| `remotion-src/Ciudad3D.tsx` | **La ciudad entera, con 16 tomas horizontales y 8 verticales** | Nuevo |
| `remotion-src/Taller3D.tsx` | La maqueta 3D del taller en three.js | **Aquí está la geometría ya depurada** |
| `remotion-src/Escenas3D.tsx` | Las escenas del bar y del pasaje, con las cámaras oficiales | Igual |
| `remotion-src/Root.tsx` | Registra las composiciones | — |

En `Taller3D.tsx` está el hallazgo que costó encontrar: la estantería de llantas chocaba
con el almacén al correrse. Se achicó el almacén y se dejó 1 m libre para el riel. Si la
maqueta se escribe de cero, ese error vuelve.

## El promocional del bar

| Archivo | Qué contiene |
| --- | --- |
| `promo.py` | Hojas de personaje y los 9 cuadros clave, con los prompts ya corregidos |
| `clips_promo.py` | Los prompts de movimiento para Veo, con el bloque `COMUN` que arregló el logo en la ropa |
| `montar_promo.py` | El montaje sobre la grilla de golpes: `golpe n = 0,267 + n × 0,46445 s` |

Los tres sirven tal cual para la versión Ecuador: **solo cambian los prompts.**

## El spot de Lázaro, ya terminado

`maestros.py`, `cuadros.py`, `clips.py`, `plano.py`, `ingredientes.py`, `montar.py`,
`sonido.py`, `sonido_real.py`, `subtitulos.py`.

Están como referencia de acabado. Los cuatro primeros son de la época de Kie.ai y buscan un
cliente en `C:\JUEGOS APP\bangover-identidad\scripts`, que no está en este repositorio.
`sonido_real.py`, `subtitulos.py` y `montar.py` sí son el estándar vigente.

## Cómo se renderiza la maqueta

```bash
npx remotion render src/index.ts Taller3D "<carpeta absoluta>" --sequence --image-format=png --gl=angle
```

Se instaló con `--legacy-peer-deps`. `--sequence` no acepta rutas con `..`.

La ciudad es más pesada y necesita dos cosas más: subir el plazo por cuadro y bajar la
concurrencia, porque una toma aérea tarda unos 50 segundos en armarse.

```bash
npx remotion render src/index.ts Ciudad3D "<carpeta>" --sequence --image-format=png \
  --gl=swangle --timeout=400000 --concurrency=1
npx remotion render src/index.ts CiudadVertical "<carpeta>" --sequence --image-format=png \
  --gl=swangle --timeout=400000 --concurrency=1
```

En Linux sin GPU, `--gl=angle` no arranca: va `--gl=swangle`. Y si Remotion intenta bajarse
su propio Chromium desde `remotion.media` y la red no lo permite, se le pasa el que ya está
instalado con `--browser-executable=/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell`.

Las dos composiciones se renderizan al doble de tamaño (2560 × 1440 y 1440 × 2560) y se bajan
a 1920 × 1080 y 1080 × 1920 con PIL. Así los bordes quedan limpios sin depender del antialias
del GL por software.
