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
| `planos_diseno/plano_urbano.py` | Dibuja el plano del barrio con PIL | **Nombres de Perú** |
| `planos_diseno/plano_taller.py` | Planta y fachada del taller | Faltan las 9 zonas nuevas y el +0,40 m |
| `planos_diseno/plano_bar_pasaje.py` | Planta del bar y del pasaje | Sirve; el bar cambia por dentro |
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
