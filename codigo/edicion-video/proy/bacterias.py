"""Renderiza bacterias con estetica de microscopio electronico (SEM) en falso color.
Mapa de alturas -> normales -> sombreado con realce de bordes + profundidad de campo + grano."""
import numpy as np, cv2

def fbm(h,w,seed,octs=5,base=6):
    rng=np.random.default_rng(seed); out=np.zeros((h,w),np.float32); amp=1.0; tot=0
    for o in range(octs):
        n=base*2**o; g=rng.random((n+2,int(n*w/h)+2)).astype(np.float32)
        out+=amp*cv2.resize(g,(w,h),interpolation=cv2.INTER_CUBIC); tot+=amp; amp*=0.5
    return out/tot

OBJS=[]
def put_capsule(H, cx, cy, ang, L, r, z0, club=0.0, tex=None, rec=True):
    if rec: OBJS.append((float(cx),float(cy),float(max(L/2,r))))
    h,w=H.shape; ext=int(L/2+r*2.2)
    x0,x1=max(0,int(cx-ext)),min(w,int(cx+ext)); y0,y1=max(0,int(cy-ext)),min(h,int(cy+ext))
    if x1<=x0 or y1<=y0: return
    yy,xx=np.mgrid[y0:y1,x0:x1].astype(np.float32)
    ca,sa=np.cos(ang),np.sin(ang)
    u=(xx-cx)*ca+(yy-cy)*sa      # a lo largo del eje
    v=-(xx-cx)*sa+(yy-cy)*ca     # perpendicular
    half=L/2
    t=np.clip(u,-half,half)
    s=(t+half)/L                 # 0..1 a lo largo
    rr=r*(1+club*np.clip((s-0.62)/0.38,0,1)**1.5)   # extremo en maza (Corynebacterium)
    d2=(u-t)**2+v**2
    inside=d2<rr**2
    hh=np.sqrt(np.clip(rr**2-d2,0,None))
    hh=hh+z0
    if tex is not None: hh=hh+tex[y0:y1,x0:x1]*r*0.10
    sub=H[y0:y1,x0:x1]; m=inside&(hh>sub); sub[m]=hh[m]

def put_sphere(H,cx,cy,r,z0,tex=None,rec=True):
    if rec: OBJS.append((float(cx),float(cy),float(r)))
    h,w=H.shape; ext=int(r*1.2)+2
    x0,x1=max(0,int(cx-ext)),min(w,int(cx+ext)); y0,y1=max(0,int(cy-ext)),min(h,int(cy+ext))
    if x1<=x0 or y1<=y0: return
    yy,xx=np.mgrid[y0:y1,x0:x1].astype(np.float32)
    d2=(xx-cx)**2+(yy-cy)**2; inside=d2<r*r
    hh=np.sqrt(np.clip(r*r-d2,0,None))+z0
    if tex is not None: hh=hh+tex[y0:y1,x0:x1]*r*0.08
    sub=H[y0:y1,x0:x1]; m=inside&(hh>sub); sub[m]=hh[m]

PALETAS={
 'ambar':[(0.00,(8,6,4)),(0.35,(70,38,10)),(0.65,(200,120,30)),(0.88,(250,200,110)),(1.0,(255,244,214))],
 'cian': [(0.00,(3,8,12)),(0.35,(8,52,66)),(0.65,(30,150,170)),(0.88,(150,225,225)),(1.0,(238,255,252))],
 'verde':[(0.00,(5,9,5)),(0.35,(20,56,22)),(0.65,(96,160,50)),(0.88,(200,230,130)),(1.0,(246,255,220))],
}
def colorizar(I,pal):
    stops=PALETAS[pal]; xs=np.array([s[0] for s in stops]); out=np.zeros(I.shape+(3,),np.float32)
    for c in range(3): out[...,c]=np.interp(I,xs,[s[1][c] for s in stops])
    return out

def render(w,h,kind='mixto',seed=1,escala=1.0,pal='ambar',densidad=1.0,fondo_seed=None,iluminacion=(-0.55,-0.65)):
    rng=np.random.default_rng(seed); S=escala; OBJS.clear()
    # fondo: piel/celulas, desenfocado y bajo
    bg=fbm(h,w,fondo_seed or seed+99,octs=6,base=4)
    H=(bg*18*S).astype(np.float32)
    # relieve de escamas de piel (celdas)
    pts=rng.random((int(90*densidad),2))*[w,h]
    for (px,py) in pts:
        put_sphere(H,px,py,rng.uniform(50,110)*S,0,rec=False)
    H=cv2.GaussianBlur(H*0.16,(0,0),10*S)           # piel: relieve bajo y suave
    tex=(fbm(h,w,seed+5,octs=5,base=40)-0.5).astype(np.float32)*2.0
    if kind in('bastones','mixto'):
        n=int(rng.integers(26,40)*densidad)
        # cumulos en "V" / empalizada, tipico de Corynebacterium
        for g in range(int(6*densidad)):
            gx,gy=rng.random()*w,rng.random()*h; base_ang=rng.uniform(0,np.pi)
            for k in range(rng.integers(2,5)):
                ang=base_ang+rng.normal(0,0.55)
                L=rng.uniform(230,380)*S; r=rng.uniform(30,40)*S
                ox,oy=rng.normal(0,70*S),rng.normal(0,70*S)
                put_capsule(H,gx+ox,gy+oy,ang,L,r,z0=rng.uniform(0,60)*S+30*S,club=rng.uniform(0.15,0.40),tex=tex)
    if kind in('cocos','mixto'):
        for g in range(int(4*densidad)):
            gx,gy=rng.random()*w,rng.random()*h; nn=rng.integers(9,20)
            for k in range(nn):
                a=rng.uniform(0,2*np.pi); rad=abs(rng.normal(0,95*S))
                r=rng.uniform(44,58)*S
                put_sphere(H,gx+np.cos(a)*rad,gy+np.sin(a)*rad,r,z0=rng.uniform(20,110)*S,tex=tex)
    # microtextura general
    H=H+tex*2.0*S
    # normales
    Hs=cv2.GaussianBlur(H,(0,0),1.2*S)
    gx=cv2.Sobel(Hs,cv2.CV_32F,1,0,ksize=3)/8.0; gy=cv2.Sobel(Hs,cv2.CV_32F,0,1,ksize=3)/8.0
    nz=1.0/np.sqrt(1+gx**2+gy**2); nx=-gx*nz; ny=-gy*nz
    lx,ly=iluminacion; lz=0.62; ln=np.sqrt(lx*lx+ly*ly+lz*lz); lx,ly,lz=lx/ln,ly/ln,lz/ln
    diff=np.clip(nx*lx+ny*ly+nz*lz,0,1)
    borde=(1-nz)**0.7                      # realce de bordes tipo SEM
    # oclusion ambiental barata
    ao=np.clip((cv2.GaussianBlur(H,(0,0),22*S)-H)/ (60*S),0,1)
    I=0.22+0.50*diff+0.55*borde-0.45*ao
    # altura -> mas brillo arriba (menos carga)
    hn=(H-H.min())/(H.max()-H.min()+1e-6); I=I*(0.75+0.5*hn)
    # profundidad de campo: lo bajo se desenfoca
    blur=cv2.GaussianBlur(I,(0,0),9*S)
    foco=np.clip((hn-0.12)/0.30,0,1)**0.8
    I=I*foco+blur*(1-foco)
    I=np.clip(I,0,1.0)**0.9
    # grano + lineas de barrido muy sutiles
    I=I+rng.normal(0,0.028,I.shape).astype(np.float32)
    I=np.clip(I,0,1)
    rgb=colorizar(I,pal)
    # viñeta
    yy,xx=np.mgrid[0:h,0:w].astype(np.float32); vg=1-0.55*(((xx-w/2)/(w/2))**2+((yy-h/2)/(h/2))**2)/2
    rgb*=np.clip(vg,0.25,1)[...,None]
    return np.clip(rgb,0,255).astype(np.uint8)

if __name__=='__main__':
    import sys
    a=render(1080,1920,'mixto',seed=7,escala=1.0,pal='ambar')
    cv2.imwrite('assets/_test_bact.png',cv2.cvtColor(a,cv2.COLOR_RGB2BGR))
    print('ok',a.shape)
