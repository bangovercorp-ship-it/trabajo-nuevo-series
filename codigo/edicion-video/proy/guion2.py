"""Guion v4: TODAS las marcas salen de la voz (transcripcion CTC + picos de silaba), no de estimaciones.
Tiempos en segundos ORIGINALES de la locucion; cues.nuevo() los lleva a la linea de tiempo recortada."""
import json, numpy as np
SC='/tmp/claude-0/-home-user-trabajo-nuevo-series/104282c1-dffc-5635-b048-3b906326b912/scratchpad'
_PICOS=np.load(f'{SC}/picos.npy')
_CT=json.load(open(f'{SC}/proy/ctc_tramos.json'))

def _palabras():
    W=[]
    for c in _CT:
        cur=None
        for tk,t in zip(c['tokens'],c['ts']):
            if tk.startswith(' ') or cur is None:
                if cur and cur['w'].strip(): W.append(cur)
                cur={'w':'','tv':None,'t0':t}
            cur['w']+=tk.strip()
            if cur['tv'] is None and any(ch in 'aeiouáéíóúAEIOUÁÉÍÓÚ' for ch in tk): cur['tv']=t
        if cur and cur['w'].strip(): W.append(cur)
    return W
WORDS=_palabras()
def ons(i,lead=0.06):
    """inicio audible de la palabra i: pico de silaba mas cercano al primer vocal (+-0.12) menos el ataque de la consonante"""
    w=WORDS[i]; tv=w['tv'] if w['tv'] is not None else w['t0']
    j=int(np.argmin(abs(_PICOS-tv))); p=float(_PICOS[j]) if abs(_PICOS[j]-tv)<=0.12 else tv
    return round(p-lead,3)
def fin(i,tope=0.55):
    """fin razonable de la palabra i (hasta la siguiente o tope)"""
    nxt=ons(i+1)-0.03 if i+1<len(WORDS) else ons(i)+tope
    return min(nxt,ons(i)+tope)

if __name__=='__main__':
    for i,w in enumerate(WORDS): print(i,w['w'],ons(i),round(fin(i),2))
