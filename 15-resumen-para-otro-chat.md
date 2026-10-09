# Resumen para pasar a otro chat — contenido de perfumes, nivel de edición y camino

## 1. Quién es y qué quiere
- Marca **Bangover** (Ecuador / Perú): línea masculina de salud y perfumería. Perfumes **Prime (solo 10 ml)**, **Climax** y **Zeus** (de 5 ml a 100 ml).
- La persona es **principiante en desarrollo de plataformas**: responder en español sencillo, directo, sin rodeos. Se impacienta con respuestas largas ("tanto te demoras") y con sustitutos hechos sin avisar.
- Quiere que Claude actúe como **editor audiovisual senior** y que **aprenda de cada corrección** para las siguientes tareas.

## 2. Camino del contenido (perfumes)
1. **Investigación base (hecha):** tres documentos (*Perfumería_Digital*, *Neuroperfumería_Molecular*, *El_Misterio_Olfativo*). Ideas principales ya extraídas. La "base científica" consolidada como archivo **aún no está escrita** (pendiente).
2. **Dos líneas de contenido:**
   - **Marca:** 3 guiones por perfume (Climax, Zeus, Prime), con las tallas reales.
   - **General educativo (sin marca):** datos curiosos sobre sudor, olor, olfato. Atrae audiencia amplia; la marca se ve solo en lo que el usuario decida. Sin tarjeta final de "Bangover".
3. **Serie del sudor/olor:** Guion 1 *"El sudor no huele mal… lo que huele mal son las bacterias"* (producido, 51 s). Guion 2 *"La nariz que se acostumbra"* (texto final en `13-guion-2-nariz-y-olor.md`). Faltan guiones 3–5.
4. **Fórmula de guion que le gusta:** gancho disruptivo en los primeros 2 s (pregunta incómoda/dato raro) → desarrollo con datos reales → remate corto → pregunta para comentarios. Se permite **controversia** para generar comentarios.
5. **Regla de contenido:** los datos de ciencia deben tener respaldo; las **afirmaciones de experiencia que el autor decide** (p. ej. "quien vive entre malos olores disfruta MÁS un baño, un jabón, un perfume") van **tal cual, sin convertirlas en pregunta ni añadir "nadie lo ha medido"**; solo no se atribuyen a "un estudio".

## 3. Nivel audiovisual que exige
- Pulido de estudio: **gancho con zoom de impacto + golpe de sonido**, transiciones limpias, **efectos de sonido profesionales** (preferir **reales CC0 de Freesound**, banco en `estudio-edicion/sonidos`; no solo sintetizados), música con **ducking suave** (baja sin golpe cuando habla), mezcla **−14 LUFS / −1 dB de pico real**.
- **Texto en pantalla: máximo 2 palabras** (1 si es larga), letra por letra, fuera de las zonas que tapa la interfaz de TikTok.
- **Animaciones pequeñas, a un costado/arriba, ordenadas y estéticas** (spray de perfume, burbujas de jabón, ADN 3D…), nunca básicas.
- **Material de apoyo a pantalla completa y LITERAL a lo que dice la voz** (se dice "secarse los pies" → se ve eso; "axilas", "bañarse", "toalla"): **fotos/videos libres de uso comercial**, o generados con su cuenta de **SnapGen/Veo**. La persona real solo sale **al inicio** (gancho), a **velocidad normal, sin cámara lenta**; el resto es material de apoyo + animaciones arriba.
- Todo **sincronizado a la palabra exacta** (ver lección 1). Sin tarjeta final de marca.
- Quiere **crítica de director con 30 años de experiencia** (letras, sonido, voz, efectos, transiciones) al entregar.

## 4. Lo hecho en esta sesión
- **Video del sudor (v4, 51 s, 1080×1920, −14 LUFS):** gancho con la persona, zoom de impacto y durazno arriba; después pantalla completa con ilustraciones propias + fondos de luces + insignias animadas arriba. **El usuario NO quedó conforme** porque no tenía los clips reales pedidos (secándose los pies, toalla, axilas, ducha).
- **Sincronía corregida:** se descubrió que los tiempos estaban estimados a ojo (hasta 4 s de error). Ahora salen de transcripción real.
- **Guion 2** reescrito con datos respaldados + afirmación directa del autor + cierre para comentarios.
- **Pipeline de edición guardado en el repo:** `codigo/edicion-video/` (transcripción, línea de tiempo, sonido, mezcla, compositor, animaciones, plan por palabra).
- **`codigo/guion2_planos.py`:** genera 13 clips verticales con Veo 3.1 Fast (52 créditos) ligados a cada frase del guion 2; corre en la PC del usuario, que tiene la clave de SnapGen.
- Revisados `skill-editar-video`, `estudio-edicion` (banco Freesound, planos Veo) y **MoneyPrinterTurbo** (busca stock en Pexels/Pixabay/Coverr con claves gratuitas; trae 29 músicas sin licencia verificada).

## 5. Bloqueos reales (decir antes de construir, no después)
- La sesión en la nube **solo llega a PyPI, GitHub y Google Fonts**. Pexels, Pixabay, Unsplash, Wikimedia, Openverse, Archive.org, Freesound, SnapGen y ElevenLabs **no responden** (aunque el usuario los permitió, puede aplicar solo a sesiones nuevas). Sin Chrome/navegador conectado.
- Pendiente del usuario: **claves API de Pexels/Pixabay** (en trámite), decidir **voz** (la graba él o voz sintética), **confirmar licencia de la música** (la del video del sudor venía de TikTok).
- Trucos que sí funcionan en la nube: modelos de reconocimiento de voz bajados de **GitHub Releases** (k2-fsa/sherpa-onnx, tag `asr-models`): `sherpa-onnx-whisper-small` (texto) y `sherpa-onnx-nemo-fast-conformer-ctc-es-1424-int8` (marcas de tiempo por sílaba).

## 6. Lecciones (el usuario pidió "apunta y aprende")
1. Tiempos **siempre** de la transcripción + picos de sílaba; nunca a ojo.
2. Material de apoyo literal a la voz; ilustraciones propias solo como último recurso y **avisando antes**.
3. Si algo bloquea, **decirlo primero y pedir lo que falta**, no construir con sustitutos.
4. Respetar la estructura pedida (persona solo al inicio, sin cámara lenta, animaciones arriba, ≤2 palabras).
5. Respeto a las afirmaciones editoriales del autor.
6. Respuestas cortas y en pasos.

## 7. Qué sigue (orden recomendado)
1. El usuario corre `python guion2_planos.py costo` y luego genera los 13 clips con su SnapGen y sube la carpeta `guion2`. (O conecta Chrome/permite dominios y trae las claves de Pexels/Pixabay.)
2. Definir voz (grabada o sintética) y licencia de música.
3. Montar el **Guion 2** con `codigo/edicion-video` (adaptar `plan4.py` a las palabras de su voz; sin persona; clips a pantalla completa; animaciones arriba: perilla de volumen, contador 0→400, ruta nariz→cerebro, jabón con burbujas, frasco con niebla; sonido real de Freesound).
4. Escribir y guardar la **base científica** y las **estructuras de guion**; producir guiones 3–5 de la serie y los 3 de marca (Climax/Zeus/Prime).
5. Convertir el pipeline en **skill persistente** (`skill-editar-video`) con las lecciones de arriba.
6. Pendiente aparte: el análisis del disco local (el usuario enviará `INVENTARIO.md` tras correr `inventario.ps1`; no borrar nada sin su aprobación; **Tiria se queda**).
