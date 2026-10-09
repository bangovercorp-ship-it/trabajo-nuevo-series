"""Fuente unica de verdad: marcas en TIEMPO ORIGINAL de la locucion. nuevo() las pasa al montaje."""
import json
_L=json.load(open('/tmp/claude-0/-home-user-trabajo-nuevo-series/104282c1-dffc-5635-b048-3b906326b912/scratchpad/proy/linea.json'))
SEG=_L['seg']; DUR=_L['dur']
def nuevo(t):
    for o0,o1,n0 in SEG:
        if o0<=t<=o1: return n0+(t-o0)
    best=None
    for o0,o1,n0 in SEG:
        for o,n in ((o0,n0),(o1,n0+o1-o0)):
            if best is None or abs(o-t)<best[0]: best=(abs(o-t),n)
    return best[1]

# ---- SONIDO: ahora se define en plan4.py (todo cuelga de palabras reales) ----
from plan4 import SFX
