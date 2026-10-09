"""Estabiliza la toma (quita el temblor de mano siguiendo la cara) y deja los cuadros en un memmap."""
import cv2, numpy as np
from scipy.ndimage import gaussian_filter1d, median_filter
SC='/tmp/claude-0/-home-user-trabajo-nuevo-series/104282c1-dffc-5635-b048-3b906326b912/scratchpad'
cap=cv2.VideoCapture(f'{SC}/in/persona30.mp4'); N=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fc=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
frames=np.lib.format.open_memmap('persona_raw.npy',mode='w+',dtype=np.uint8,shape=(N,1920,1080,3))
C=np.full((N,3),np.nan)
for i in range(N):
    ok,f=cap.read()
    if not ok: N=i; break
    frames[i]=f
    g=cv2.cvtColor(cv2.resize(f,(270,480)),cv2.COLOR_BGR2GRAY)
    r=fc.detectMultiScale(g,1.1,4,minSize=(70,70))
    if len(r):
        x,y,w,h=max(r,key=lambda b:b[2]*b[3]); C[i]=((x+w/2)*4,(y+h/2)*4,w*4)
cap.release(); frames.flush()
ok=~np.isnan(C[:,0]); print(f"cuadros {N}  con cara detectada {ok.sum()} ({100*ok.mean():.0f}%)")
idx=np.arange(N)
for c in range(3): C[:,c]=np.interp(idx,idx[ok],C[ok,c])
for c in range(3): C[:,c]=median_filter(C[:,c],size=7,mode='nearest')
low=np.stack([gaussian_filter1d(C[:,c],sigma=14,mode='nearest') for c in range(3)],1)
ESC=1.14; mx=(ESC-1)/2*1080; my=(ESC-1)/2*1920
dx=np.clip(low[:,0]-C[:,0],-mx*0.9,mx*0.9); dy=np.clip(low[:,1]-C[:,1],-my*0.9,my*0.9)
out=np.lib.format.open_memmap('persona_stab.npy',mode='w+',dtype=np.uint8,shape=(N,1920,1080,3))
cara=np.zeros((N,3),np.float32)
for i in range(N):
    M=np.array([[ESC,0,(1-ESC)*540+dx[i]],[0,ESC,(1-ESC)*960+dy[i]]],np.float32)
    out[i]=cv2.warpAffine(np.asarray(frames[i]),M,(1080,1920),flags=cv2.INTER_LANCZOS4,borderMode=cv2.BORDER_REPLICATE)
    cara[i]=(ESC*(C[i,0]-540)+540+dx[i], ESC*(C[i,1]-960)+960+dy[i], ESC*C[i,2])
out.flush(); np.save('persona_cara.npy',cara)
jit_antes=np.abs(np.diff(C[:,:2],axis=0)).mean(); jit_desp=np.abs(np.diff(cara[:,:2],axis=0)).mean()
print(f"temblor medio de la cara: antes {jit_antes:.2f}px/cuadro -> despues {jit_desp:.2f}px/cuadro")
print("cara estabilizada (mediana x,y,w):",np.median(cara,0).round(0))
