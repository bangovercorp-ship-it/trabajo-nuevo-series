# Lecciones de edición (para no repetir errores)

1. **Todo tiempo sale de la transcripción, nunca de estimaciones.** En el video del sudor, texto y animaciones salieron hasta ~4 s antes
   de la palabra porque los tiempos eran a ojo. Método que funciona en este entorno:
   - `pip install sherpa-onnx`
   - modelos desde GitHub Releases (k2-fsa/sherpa-onnx, tag `asr-models`): `sherpa-onnx-whisper-small` (texto) y
     `sherpa-onnx-nemo-fast-conformer-ctc-es-1424-int8` (marcas de tiempo por sílaba, Español).
   - Se afinan con los picos de sílaba del audio (error típico < 0,1 s). Se verifica con hojas de contactos y números.
2. **Material de apoyo = lo que dice la voz, literal.** Si la voz dice "secarse los pies", se ve alguien secándose los pies; si dice "axilas",
   axilas; si dice "bañarse", una ducha. Ilustraciones propias solo como último recurso y avisando antes, no después.
3. **Si algo bloquea el trabajo, decirlo ANTES de construir con sustitutos.** El entorno bloquea Pexels, Pixabay, Unsplash, Wikimedia,
   Openverse, Archive.org, Huggingface (solo permite PyPI, GitHub y Google Fonts). Se probó dos veces. Pedir al usuario que permita los dominios
   (Pexels/Pixabay necesitan además clave gratuita de API) o que descargue los clips de la lista de búsqueda.
4. **Respetar el pedido de estructura.** Persona solo al inicio si se pide; sin cámara lenta; animaciones pequeñas arriba; texto máx. 2 palabras.
5. **Datos curiosos, pero ciertos.** Una hipótesis no es un hecho: se presenta como pregunta abierta.
6. **Responder claro y corto**, en español sencillo (la persona es principiante). Entregar en pasos, no en bloques enormes.
