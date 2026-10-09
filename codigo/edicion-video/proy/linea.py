"""Linea de tiempo: recorta pausas de la locucion respetando los silencios dramaticos
y traduce las marcas (tiempo original -> tiempo nuevo)."""
import numpy as np, json, subprocess, soundfile as sf

SC='/tmp/claude-0/-home-user-trabajo-nuevo-series/104282c1-dffc-5635-b048-3b906326b912/scratchpad'
tr = np.load(f'{SC}/tramos.npy')          # 26 tramos de habla (s, tiempo original)
# --- politica de pausas: objetivo (s) por hueco; el resto de huecos usa 0.28 ---
HUECO = {1:0.62,   # tras la pregunta del gancho: el "medio segundo" de vacio
         4:0.50,   # antes del "Punto."
         12:0.34, 16:0.31, 17:0.40, 19:0.30, 20:0.32}
DEF = 0.28
PRE, POST = 0.12, 0.45          # aire antes del primer tramo y despues del ultimo

# intervalos que se conservan: (orig_ini, orig_fin, nuevo_ini)
seg=[]; t_new=0.0
a0 = tr[0][0]-PRE
cur_o = a0
for k in range(len(tr)):
    a,b = tr[k]
    if k < len(tr)-1:
        gap = tr[k+1][0]-b
        tgt = min(gap, HUECO.get(k+1, DEF))
        # conservamos tgt/2 de cola y tgt/2 de entrada del siguiente
        keep_end = b + tgt/2
        seg.append([cur_o, keep_end, t_new]); t_new += keep_end-cur_o
        cur_o = tr[k+1][0] - tgt/2
    else:
        keep_end = b + POST
        seg.append([cur_o, keep_end, t_new]); t_new += keep_end-cur_o
DUR = t_new
print(f"duracion nueva: {DUR:.2f}s  (original 63.81s)")

def nuevo(t):
    """tiempo original -> nuevo (si cae en un tramo recortado, ajusta al borde)."""
    for o0,o1,n0 in seg:
        if o0 <= t <= o1: return n0 + (t-o0)
    # dentro de un hueco recortado: borde mas cercano
    best=None
    for o0,o1,n0 in seg:
        for o,n in ((o0,n0),(o1,n0+o1-o0)):
            if best is None or abs(o-t)<best[0]: best=(abs(o-t),n)
    return best[1]

# --- audio: montar, limpiar ---
subprocess.run(['ffmpeg','-y','-v','error','-i',f'{SC}/in/voz.m4a','-ac','1','-ar','48000','-c:a','pcm_f32le','voz48.wav'],check=True)
x,sr = sf.read('voz48.wav'); x = x.astype(np.float64)
XF = int(0.012*sr)
out = np.zeros(int(round(DUR*sr))+sr)
for o0,o1,n0 in seg:
    i0,i1 = max(0,int(o0*sr)), min(len(x),int(o1*sr)); j0=int(round(n0*sr))
    s = x[i0:i1].copy()
    f = min(XF, len(s)//2)
    ramp = np.linspace(0,1,f)
    s[:f]*=np.sin(ramp*np.pi/2); s[-f:]*=np.cos(ramp*np.pi/2)
    out[j0:j0+len(s)] += s
out = out[:int(round(DUR*sr))]
sf.write('voz_cortada.wav', out.astype(np.float32), sr, subtype='FLOAT')

json.dump({'seg':seg,'dur':DUR}, open('linea.json','w'))
print("segmentos:", len(seg))
