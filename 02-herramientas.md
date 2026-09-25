# Herramientas, con sus comandos

Todas las claves viven en `C:\JUEGOS APP\.secretos\` y **nunca se escriben en el chat ni se imprimen en pantalla**. Cada cliente las lee solo.

| Archivo | Para qué |
| --- | --- |
| `snapgen.env` | Imágenes y video (el principal) |
| `elevenlabs.env` | Voces |
| `freesound.env` | Sonidos reales, CC0 |
| `kie.env` | Imágenes y video, alternativa, casi sin saldo |

## SnapGen · imágenes y video

Cliente: `C:\pesonajes para videos\snapgen.py`

- **Imagen** con Nano Banana Pro: **3 créditos**. Acepta imágenes de referencia, que es como se mantiene la consistencia.
- **Video** con Veo 3.1 Fast: **4 créditos** por 8 segundos, vertical 1080p, con audio.
- Quedan unos **1.744 créditos**.

```python
import snapgen as sg
sg.creditos()
r = sg.imagen("prompt", aspecto="9:16", resolucion="2K", imagenes=["ref1.png", "ref2.png"])
e = sg.esperar(r["uuid"], limite=600, cada=6)
sg.descargar(sg.url_imagen(e), "salida.png")

r = sg.video("prompt de movimiento", imagenes=["cuadro-inicial.png"])
e = sg.esperar(r["uuid"], limite=1200, cada=10)
sg.descargar(sg.url_video(e), "salida.mp4")
```

Scripts que ya usan esto: `personajes.py` (hojas de personaje), `vistas_reales.py` (vistas desde la maqueta), `promo.py` y `clips_promo.py` (el promocional).

**Dos trampas aprendidas:**
1. Nunca escribir la palabra *TikTok* en un prompt de Veo: le pone el logo de TikTok a la ropa.
2. Veo agrega objetos de más. Si se piden tres gomitas, hay que escribir *EXACTLY THREE* y usar solo el primer segundo del clip.

## ElevenLabs · voces

Cliente: `C:\pesonajes para videos\voz.py`

```bash
python voz.py cuenta    # plan y caracteres disponibles
python voz.py voces     # lista las voces
python voz.py di <voice_id> salida.mp3 "el texto"
```

Plan de pago por uso, **23.736 caracteres** disponibles, unos 23 minutos de voz, se reinicia el 25 de octubre de 2026. Modelo `eleven_multilingual_v2`.

**Falta elegir las voces.** Se probaron cuatro latinas para Gallín (Miro, que es peruana pero de acento neutro; Draku; Axel; Fer). **Para Ecuador hay que buscar voces de acento costeño** en la biblioteca compartida (`/shared-voices` con `search`), y antes de usar una hay que agregarla a la cuenta.

## Freesound · sonidos reales

Cliente: `freesound.py`, más `sonido_real.py` para colocarlos en la línea de tiempo. Todos CC0. Los sonidos ya descargados están en `sonidos\`.

## Remotion + three.js · la maqueta 3D

```bash
npx remotion render src/index.ts Taller3D "<carpeta absoluta>" --sequence --image-format=png --gl=angle
```

- Se instaló con `--legacy-peer-deps`.
- `--sequence` no acepta rutas con `..`: hay que dar la ruta absoluta.
- Composiciones registradas en `remotion\src\Root.tsx`.

## ffmpeg · el montaje

Está en la versión 9, que tiene sus manías:

- No existe `-filter_complex_script`: se pasa `-vf` directo.
- `zoompan` cuenta cuadros de entrada: hay que poner `fps=30` **antes** del zoom, y `-framerate 30` para imágenes en bucle.
- Para cortar al ritmo, las duraciones se miden en cuadros enteros desde el inicio, si no, cincuenta cortes se corren solos.

Montajes de referencia: `montar.py` (el spot) y `montar_promo.py` (el promocional del bar, cortado sobre 129,2 bpm).

## Otros

- **Subtítulos:** `subtitulos.py` genera ASS con la fuente Anton. Las marcas de tiempo salen de whisper (`--model base --language es --fp16 False`).
- **Planos y diagramas:** se dibujan con PIL desde Python. No hay renderizador de SVG en la máquina.
- **La biblia** se edita con el conector de documentos de claude.ai, no con archivos locales.
- **La laptop no tiene NVIDIA** (Ryzen 7 con Radeon integrada): toda la IA pesada va por la nube.
