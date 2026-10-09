"""Compositor: persona + tarjetas + pantallas completas + texto animado + impactos. Cuadro a cuadro."""
import numpy as np, cv2, json, math, sys, subprocess
from PIL import Image, ImageDraw, ImageFont
from cues import nuevo as N, DUR
W,H,FPS=1080,1920,30
SC='/tmp/claude-0/-home-user-trabajo-nuevo-series/104282c1-dffc-5635-b048-3b906326b912/scratchpad'
ANTON=f'{SC}/fuentes/1Ptgg87LROyAm0K0.ttf'; MONT=f'{SC}/fuentes/JTUHjIg1_i6t8kCHKm4532VJOt5-QNFgpCvr70w-.ttf'
A='assets/'
def clamp(x,a=0.0,b=1.0): return max(a,min(b,x))
def prog(t,a,b): return clamp((t-a)/(b-a)) if b>a else 1.0
def e_out3(x): return 1-(1-x)**3
def e_io3(x): return 4*x**3 if x<.5 else 1-(-2*x+2)**3/2
def e_back(x,s=1.70158): x=x-1; return 1+(s+1)*x**3+s*x**2
def lerp(a,b,u): return a+(b-a)*u

AMB=(255,193,64); BLA=(255,255,255); ROJ=(255,92,80); CIA=(96,226,232); VER=(150,225,90); LIM=(196,238,70)

# ---------------------------------------------------------------- sprites
def spr_from_rgba(arr_rgba):
    bgra=cv2.cvtColor(arr_rgba,cv2.COLOR_RGBA2BGRA)
    return {'rgb':bgra[...,:3].copy(),'a':bgra[...,3].astype(np.float32)/255.0}

def draw_sprite(fr,sp,cx,cy,scale=1.0,rot=0.0,op=1.0,shadow=0.0,add=False):
    if op<=0.004 or scale<=0.01: return
    h,w=sp['a'].shape
    M=cv2.getRotationMatrix2D((w/2,h/2),rot,scale); M[0,2]+=cx-w/2; M[1,2]+=cy-h/2
    cs=np.array([[0,0,1],[w,0,1],[w,h,1],[0,h,1]],np.float32)@M.T
    m=int(shadow*0.9+4)
    x0,y0=int(max(0,cs[:,0].min()-m)),int(max(0,cs[:,1].min()-m)); x1,y1=int(min(W,cs[:,0].max()+m)),int(min(H,cs[:,1].max()+m+shadow*0.7))
    if x1-x0<2 or y1-y0<2: return
    Ml=M.copy(); Ml[0,2]-=x0; Ml[1,2]-=y0
    sz=(x1-x0,y1-y0)
    a=cv2.warpAffine(sp['a'],Ml,sz,flags=cv2.INTER_LINEAR,borderValue=0)*op
    reg=fr[y0:y1,x0:x1].astype(np.float32)
    if shadow>0:
        sh=cv2.GaussianBlur(a,(0,0),shadow*0.55); Ms=np.float32([[1,0,0],[0,1,shadow*0.45]]); sh=cv2.warpAffine(sh,Ms,sz)
        reg*= (1-0.55*sh)[...,None]
    rgb=cv2.warpAffine(sp['rgb'],Ml,sz,flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
    if add: reg+=rgb*a[...,None]
    else: reg=reg*(1-a[...,None])+rgb*a[...,None]
    fr[y0:y1,x0:x1]=np.clip(reg,0,255).astype(np.uint8)

_FC={}
def font(p,s):
    k=(p,s)
    if k not in _FC: _FC[k]=ImageFont.truetype(p,s)
    return _FC[k]

def texto_sprite(txt,color=BLA,maxw=840,size=170,stroke=11,upto=None,glow=True):
    """Texto Anton con borde negro y sombra. 'upto' = cuantas letras mostrar (alineado igual que el texto completo)."""
    s=size
    while s>56 and font(ANTON,s).getlength(txt)>maxw: s-=4
    f=font(ANTON,s); bb=f.getbbox(txt); tw,th=bb[2]-bb[0],bb[3]-bb[1]; pad=stroke*2+30
    im=Image.new('RGBA',(tw+2*pad,th+2*pad),(0,0,0,0)); d=ImageDraw.Draw(im)
    shown=txt if upto is None else txt[:upto]
    if shown:
        if glow:
            g=Image.new('RGBA',im.size,(0,0,0,0)); gd=ImageDraw.Draw(g)
            gd.text((pad-bb[0],pad-bb[1]),shown,font=f,fill=color+(255,),stroke_width=stroke+4,stroke_fill=color+(255,))
            g=g.filter(__import__('PIL.ImageFilter',fromlist=['ImageFilter']).GaussianBlur(14)); 
            ga=np.array(g); ga[...,3]=(ga[...,3]*0.38).astype(np.uint8); im=Image.alpha_composite(im,Image.fromarray(ga))
        sh=Image.new('RGBA',im.size,(0,0,0,0)); sd=ImageDraw.Draw(sh)
        sd.text((pad-bb[0],pad-bb[1]+10),shown,font=f,fill=(0,0,0,235),stroke_width=stroke,stroke_fill=(0,0,0,235))
        sh=sh.filter(__import__('PIL.ImageFilter',fromlist=['ImageFilter']).GaussianBlur(7)); im=Image.alpha_composite(im,sh)
        d=ImageDraw.Draw(im)
        d.text((pad-bb[0],pad-bb[1]),shown,font=f,fill=color+(255,),stroke_width=stroke,stroke_fill=(10,10,10,255))
    return spr_from_rgba(np.array(im))

# ---------------------------------------------------------------- assets
def leer(n): return cv2.imread(A+n+'.png')
def tarjeta(n,w=880,h=495,etiqueta=True):
    im=cv2.resize(leer(n),(w,h),interpolation=cv2.INTER_AREA)
    ss=4; m=np.zeros((h*ss,w*ss),np.uint8); cv2.rectangle(m,(0,0),(w*ss-1,h*ss-1),255,-1)
    mk=np.zeros_like(m); r=30*ss
    cv2.rectangle(mk,(r,0),(w*ss-r,h*ss),255,-1); cv2.rectangle(mk,(0,r),(w*ss,h*ss-r),255,-1)
    for cx_,cy_ in ((r,r),(w*ss-r,r),(r,h*ss-r),(w*ss-r,h*ss-r)): cv2.circle(mk,(cx_,cy_),r,255,-1,cv2.LINE_AA)
    a=cv2.resize(mk,(w,h),interpolation=cv2.INTER_AREA).astype(np.float32)/255
    er=cv2.erode(mk,np.ones((3*ss,3*ss),np.uint8)); borde=cv2.resize(mk-er,(w,h),interpolation=cv2.INTER_AREA).astype(np.float32)/255
    im=im.astype(np.float32); im=im*(1-0.32*borde[...,None])+255*0.32*borde[...,None]
    if etiqueta:
        pil=Image.fromarray(cv2.cvtColor(np.clip(im,0,255).astype(np.uint8),cv2.COLOR_BGR2RGB)); d=ImageDraw.Draw(pil,'RGBA')
        f=font(MONT,17); t='ILUSTRACIÓN'; d.text((w-30-f.getlength(t),h-34),t,font=f,fill=(255,255,255,150))
        im=cv2.cvtColor(np.array(pil),cv2.COLOR_RGB2BGR).astype(np.float32)
    return {'rgb':np.clip(im,0,255).astype(np.uint8),'a':a}

IM={}; CARDS_SPR={}; ANIMF={}; TXT={}; PEACH=None; PERS=None; CARA=None; VIG=None; GRAIN=None; OBJS=None
def cargar():
    global PEACH,PERS,CARA,VIG,GRAIN,OBJS
    for k in ('bact_amplio','bact_bastones','bact_cocos','bact_comen','adn_vert'): IM[k]=leer(k)
    IM['bact_amplio_f']=cv2.flip(IM['bact_amplio'],1)
    for k in ('gota','sal','sinolor','cuerpo_axilas','cuerpo_ingle','cuerpo_pies','glandula','gente','igual','spray','jabon','toalla','adn','micro'):
        arr=np.load(A+f'anim_{k}.npy'); ANIMF[k]=(np.ascontiguousarray(arr[...,:3][...,::-1]),(arr[...,3].astype(np.float32)/255.0))
    p=cv2.imread(A+'duraznito.png',cv2.IMREAD_UNCHANGED); p=cv2.resize(p,(400,400),interpolation=cv2.INTER_AREA)
    PEACH={'rgb':p[...,:3].copy(),'a':p[...,3].astype(np.float32)/255}
    PERS=np.load('persona_stab.npy',mmap_mode='r'); CARA=np.load('persona_cara.npy')
    yy,xx=np.mgrid[0:H,0:W].astype(np.float32); v=1-0.34*(((xx-W/2)/(W/2))**2*0.7+((yy-H/2)/(H/2))**2)
    v=np.clip(v,0.45,1); VIG=np.repeat((v*255).astype(np.uint8)[...,None],3,2)
    rng=np.random.default_rng(5); GRAIN=[]
    for _ in range(6):
        n=(rng.normal(0,2.4,(H,W))).astype(np.float32); pos=np.clip(n,0,255).astype(np.uint8); neg=np.clip(-n,0,255).astype(np.uint8)
        GRAIN.append((np.repeat(pos[...,None],3,2),np.repeat(neg[...,None],3,2)))
    OBJS=json.load(open(A+'bact_comen_objs.json'))
def spr_txt(key,**kw):
    if key not in TXT: TXT[key]=texto_sprite(key[0],**kw)
    return TXT[key]

# ---------------------------------------------------------------- guion visual v4 (todo desde plan4: palabras reales)
import plan4 as P4
_SFX=json.load(open('sfx_times.json')); _BO=[t for t,k in _SFX if k in('boom','thud')]
def B(t):
    nt=N(t); j=min(_BO,key=lambda x:abs(x-nt)); return j if abs(j-nt)<0.10 else nt
_IMP=set(round(t,3) for t in P4.HITS_T)
def _m(t): return B(t) if round(t,3) in _IMP else N(t)
NP=N(P4.P_END)                                    # la persona solo vive hasta aqui
CENT={'bact_amplio':(675,1200),'bact_bastones':(675,1100),'bact_amplio_f':(675,1250),'bact_cocos':(675,1200),'bact_comen':(675,1200),'adn_vert':(675,1200)}
TAKE=[]
for a_,b_,mat,z0,z1,ex in P4.SCENES:
    cx,cy=CENT.get(mat,(540,960))
    if mat=='bact_comen' and ex=='vapor': cx,cy=560,1050
    TAKE.append((_m(a_),(N(b_) if b_ is not None else DUR+0.2),mat,z0,z1,cx,cy,ex))
CARDS=[(N(t),k) for t,k in P4.CARDS]
SPLIT=[(N(a_),(N(b_) if b_ is not None else DUR+0.2)) for a_,b_ in P4.GRUPOS]
CAPS=[(_m(d['a']),N(d['b']),d['txt'],d['col'],d['sz']) for d in P4.CAPS]
ABC=[(N(t),ch) for t,ch in P4.ABC]
ABC_T=(_m(P4.T_GEN),N(P4.O(93)-0.02))
HITS_P=[(P4.T_POTO,0.16,0.34,12,0.20),(P4.T_BACT1,0.0,0.1,14,0.30),(P4.T_PUNTO,0.10,0.30,9,0.18),(P4.T_BACT2,0.0,0.1,12,0.26),(P4.T_APESTA,0.0,0.1,16,0.30),(P4.T_GEN,0.0,0.1,12,0.26)]
HITS=[(B(t),a,b,c,d) for t,a,b,c,d in HITS_P]
PEACH_T=(B(P4.T_POTO),N(P4.ons(10))-0.06)
FLASHES=[(B(h[0]),h[4]) for h in HITS_P]

def take_at(t):
    for k in TAKE:
        if k[0]<=t<k[1]: return k
    return None

def hit_fx(t):
    z=0.0; sx=sy=0.0
    for th,az,tau,ash,_ in HITS:
        d=t-th
        if d>=0:
            z+=az*math.exp(-d/tau)*clamp(d/0.05)
            if ash>0:
                amp=ash*math.exp(-d/0.12); sx+=amp*math.sin(2*math.pi*23*d); sy+=amp*math.sin(2*math.pi*31*d+1.0)
    return z,sx,sy
def flash_at(t):
    f=0.0
    for th,a in FLASHES:
        d=t-th
        if d>=0: f+=a*math.exp(-d/0.07)
    return f

_DIS=None; _FLC={}
def _flujos(i):
    global _DIS
    if _DIS is None: _DIS=cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
    if i in _FLC: return _FLC[i]
    a=np.asarray(PERS[i]); b=np.asarray(PERS[i+1])
    ga=cv2.cvtColor(cv2.resize(a,(540,960),interpolation=cv2.INTER_AREA),cv2.COLOR_BGR2GRAY); gb=cv2.cvtColor(cv2.resize(b,(540,960),interpolation=cv2.INTER_AREA),cv2.COLOR_BGR2GRAY)
    f01=_DIS.calc(ga,gb,None); f10=_DIS.calc(gb,ga,None)
    f01=cv2.resize(f01,(W,H),interpolation=cv2.INTER_LINEAR)*2.0; f10=cv2.resize(f10,(W,H),interpolation=cv2.INTER_LINEAR)*2.0
    if len(_FLC)>4: _FLC.clear()
    _FLC[i]=(f01,f10); return _FLC[i]
_GX=_GY=None
def pframe(src):
    global _GX,_GY
    src=clamp(src,0,len(PERS)-1.001); i=int(src); fr=src-i
    a=np.asarray(PERS[i])
    if fr<0.04: return a
    b=np.asarray(PERS[i+1]); f01,f10=_flujos(i)
    if _GX is None: _GY,_GX=np.mgrid[0:H,0:W].astype(np.float32)
    ma=(_GX+fr*f10[...,0],_GY+fr*f10[...,1]); mb=(_GX+(1-fr)*f01[...,0],_GY+(1-fr)*f01[...,1])
    wa=cv2.remap(a,ma[0],ma[1],cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT101); wb=cv2.remap(b,mb[0],mb[1],cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT101)
    return cv2.addWeighted(wa,1-fr,wb,fr,0)

SRC0=1.15                                         # el clip arranca aqui, velocidad normal (sin camara lenta)
def escena_persona(t):
    fr=np.asarray(PERS[int(clamp(SRC0*FPS+t*FPS,0,len(PERS)-1))])
    u=prog(t,0,NP); z=1.0+0.05*e_io3(u)
    hz,sx,sy=hit_fx(t)
    s=z+hz
    M=np.float32([[s,0,540-s*540+sx],[0,s,420+28-s*420+sy]])
    per=cv2.warpAffine(fr,M,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
    return cv2.addWeighted(per,1.32,cv2.GaussianBlur(per,(0,0),1.7),-0.32,0)

# ---- fondos procedurales (SOLO mientras no haya fotos/videos libres): bokeh con paralaje
PAL={'calor':((22,34,78),(30,70,170),[(70,170,255),(50,110,245),(130,210,255)]),
     'agua':((62,44,14),(120,86,22),[(235,205,95),(205,165,60),(255,232,165)]),
     'cuerpo':((58,28,66),(110,44,128),[(185,115,255),(150,85,235),(210,170,255)]),
     'violeta':((66,26,52),(120,38,96),[(235,115,175),(205,95,155),(250,170,215)])}
_BK={}
def _capa(pal,seed,n,rmin,rmax,blur,alpha):
    rng=np.random.default_rng(seed); cv=np.zeros((2*H,W,3),np.float32); cols=PAL[pal][2]
    for _ in range(n):
        x=rng.random()*W; y=rng.random()*H; r=rmin+rng.random()**1.6*(rmax-rmin); c=np.array(cols[int(rng.integers(0,3))],np.float32)
        al=alpha*(0.5+rng.random()*0.7)
        for yy in (y,y+H):
            y0,y1=int(max(0,yy-r-4)),int(min(2*H,yy+r+5)); x0,x1=int(max(0,x-r-4)),int(min(W,x+r+5))
            if y1<=y0 or x1<=x0: continue
            sub=np.zeros((y1-y0,x1-x0),np.float32); cv2.circle(sub,(int(x-x0),int(yy-y0)),int(r),1.0,-1,cv2.LINE_AA)
            ring=np.zeros_like(sub); cv2.circle(ring,(int(x-x0),int(yy-y0)),int(r),1.0,max(2,int(r*0.07)),cv2.LINE_AA)
            m=(sub*0.55+ring*0.55)[...,None]*al
            cv[y0:y1,x0:x1]+=m*c
    cv=cv2.GaussianBlur(cv,(0,0),blur)
    return np.clip(cv,0,255).astype(np.uint8)
def _bokeh_cache(pal):
    if pal not in _BK:
        base=np.zeros((H,W,3),np.float32); top=np.array(PAL[pal][0],np.float32); mid=np.array(PAL[pal][1],np.float32)
        yy=np.linspace(0,1,H,dtype=np.float32)[:,None,None]; g=np.clip(1-np.abs(yy-0.52)*2.0,0,1)**1.4
        base=top*(1-g)+mid*g; base=np.repeat(base,W,1)
        xx=np.linspace(-1,1,W,dtype=np.float32)[None,:,None]; base=base*(1-0.28*xx**2)
        _BK[pal]=(base.astype(np.uint8),[_capa(pal,11,26,50,150,13,0.50),_capa(pal,12,20,28,95,6,0.60),_capa(pal,13,30,8,30,2.2,0.80)])
    return _BK[pal]
def escena_bokeh(pal,t,a,b,z0,z1):
    base,caps=_bokeh_cache(pal); fr=base.copy()
    for k,(cp,sp) in enumerate(zip(caps,(34,70,125))):
        off=int((t*sp+k*377)%H); lay=cp[off:off+H]
        sway=int(18*math.sin(t*0.9+k*2.1)); lay=np.roll(lay,sway,1)
        fr=cv2.add(fr,lay)
    u=prog(t,a,b); z=lerp(z0,z1,e_io3(u)); hz,sx,sy=hit_fx(t); sc=z*(1+hz*0.5)
    M=np.float32([[sc,0,540-sc*540+sx],[0,sc,960-sc*960+sy]])
    return cv2.warpAffine(fr,M,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)

def escena_take(k,t):
    a,b,key,z0,z1,cx,cy,extra=k
    if key.startswith('bokeh:'): return escena_bokeh(key[6:],t,a,b,z0,z1),None,1.0
    img=IM[key]; u=prog(t,a,b); z=lerp(z0,z1,e_io3(u)*0.9+0.1*u)
    punch=1+0.30*(1-e_out3(prog(t,a,a+0.24)))
    hz,sx,sy=hit_fx(t)
    sc=0.8*z*punch*(1+hz*0.5)
    M=np.float32([[sc,0,540-sc*cx+sx],[0,sc,960-sc*cy+sy]])
    fr=cv2.warpAffine(img,M,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT101)
    return fr,M,sc

def aditivo(fr,ov,k=1.0):
    return cv2.add(fr,(ov.astype(np.float32)*k).clip(0,255).astype(np.uint8))

def capa_comen(fr,M,t,a,b):
    ov=np.zeros((H,W,3),np.uint8); rng=np.random.default_rng(11)
    objs=np.array(OBJS,np.float32); P=np.stack([objs[:,0]*M[0,0]+M[0,2],objs[:,1]*M[1,1]+M[1,2],objs[:,2]*M[0,0]],1)
    vis=P[(P[:,0]>40)&(P[:,0]<W-40)&(P[:,1]>120)&(P[:,1]<H-300)]
    if len(vis)==0: return fr
    for k in range(150):
        ts=a+0.05+rng.random()*(b-a-0.5); dur=0.55+rng.random()*0.6; u=(t-ts)/dur
        if u<0 or u>1: continue
        tgt=vis[int(rng.integers(0,len(vis)))]; ang=rng.random()*2*math.pi; dist=260+rng.random()*340
        st=(tgt[0]+math.cos(ang)*dist,tgt[1]+math.sin(ang)*dist)
        e=u**2.2; x=lerp(st[0],tgt[0],e); y=lerp(st[1],tgt[1],e)
        r=max(2,int(18*(1-e)+4)); cv2.circle(ov,(int(x),int(y)),r,(60,190,255),-1,cv2.LINE_AA); cv2.circle(ov,(int(x),int(y)),max(1,r//2),(210,240,255),-1,cv2.LINE_AA)
    ov=cv2.GaussianBlur(ov,(0,0),5)+ov
    return aditivo(fr,ov,1.0)

def capa_vapor(fr,M,t,a,b):
    ov=np.zeros((H,W,3),np.uint8); rng=np.random.default_rng(3)
    objs=np.array(OBJS,np.float32); P=np.stack([objs[:,0]*M[0,0]+M[0,2],objs[:,1]*M[1,1]+M[1,2]],1)
    vis=P[(P[:,0]>60)&(P[:,0]<W-60)&(P[:,1]>400)&(P[:,1]<H-250)]
    k=min(len(vis),16); rng.shuffle(vis); u=prog(t,a,b)
    for j in range(k):
        x0,y0=vis[j]; ph=rng.random()*6.28; sp=0.8+rng.random()*0.6
        pts=[]
        for q in np.linspace(0,1,26):
            yy=y0-q*(230+160*u)*(0.7+0.5*((j*37)%5)/5); xx=x0+math.sin(q*7+ph+t*3.4*sp)*(16+26*q)
            pts.append((int(xx),int(yy)))
        al=clamp(0.25+u*0.9)
        cv2.polylines(ov,[np.array(pts,np.int32)],False,(int(70*al),int(220*al),int(140*al)),int(9+9*u),cv2.LINE_AA)
    ov=cv2.GaussianBlur(ov,(0,0),9)
    fr=aditivo(fr,ov,0.85)
    # tinte verdoso creciente hacia "apesta"
    tint=np.zeros_like(fr); tint[...,1]=18; tint[...,2]=-8 if False else 0
    return cv2.add(fr,(tint.astype(np.float32)*u*1.5).clip(0,255).astype(np.uint8))

SLOT_X=(190.0,508.0,826.0); ROW_Y=300; BADGE=1.12; PITCH=318.0
_SHEEN=None
def _sheen(p):
    global _SHEEN
    if _SHEEN is None:
        yy,xx=np.mgrid[0:270,0:270].astype(np.float32); _SHEEN=(xx*0.8+yy*0.6)
    return np.clip(1-np.abs(_SHEEN-p*420+60)/46,0,1)**2
def dibujar_insignias(fr,t):
    for a,b in SPLIT:
        if not (a<=t<=b+0.05): continue
        cs=[(ti,k) for ti,k in CARDS if a-0.01<=ti<b]
        if not cs: continue
        ex=prog(t,b-0.30,b)
        shift=sum(e_io3(prog(t-tj,0,0.34)) for i,(tj,_) in enumerate(cs) if i>=3 and t>=tj)
        for i,(ti,k) in enumerate(cs):
            if t<ti: continue
            age=t-ti; pos=min(i-shift,2.0)
            if pos<-1.0: continue
            x=SLOT_X[0]+PITCH*pos
            rgbF,aF=ANIMF[k]; f=int(age*30)%len(rgbF)
            rgb=rgbF[f]; al=aF[f]
            if age<0.55:
                bnd=_sheen(prog(age,0,0.55))*0.42
                rgb=np.clip(rgb.astype(np.float32)+255*bnd[...,None]*(al[...,None]>0.5),0,255).astype(np.uint8)
            sg=1 if i%2==0 else -1
            sc=BADGE*lerp(0.62,1.0,e_back(prog(age,0,0.36),2.2))*(1-0.10*ex)
            op=clamp(age/0.16)*(1-ex)*clamp(1+pos)
            yo=lerp(46,0,e_out3(prog(age,0,0.34)))-62*ex
            rot=sg*lerp(-5.0,0.0,e_out3(prog(age,0,0.34)))
            if pos<0: sc*=1+0.2*pos
            draw_sprite(fr,{'rgb':rgb,'a':al},x,ROW_Y+yo,sc,rot,op,shadow=30)

_LS={}
def letras(txt,color,maxw,size,stroke):
    key=(txt,color,maxw,size,stroke)
    if key in _LS: return _LS[key]
    from PIL import ImageFilter as IF
    s_=size
    while s_>56 and font(ANTON,s_).getlength(txt)>maxw: s_-=4
    f=font(ANTON,s_); asc,desc=f.getmetrics(); pad=stroke*2+26; total=f.getlength(txt); items=[]
    for i,ch in enumerate(txt):
        if ch==' ': continue
        xl=f.getlength(txt[:i]); adv=f.getlength(ch); w=int(adv)+2*pad; h=asc+desc+2*pad
        im=Image.new('RGBA',(w,h),(0,0,0,0))
        g=Image.new('RGBA',(w,h),(0,0,0,0)); ImageDraw.Draw(g).text((pad,pad),ch,font=f,fill=color+(255,),stroke_width=stroke+4,stroke_fill=color+(255,))
        g=g.filter(IF.GaussianBlur(14)); ga=np.array(g); ga[...,3]=(ga[...,3]*0.36).astype(np.uint8); im=Image.alpha_composite(im,Image.fromarray(ga))
        sh=Image.new('RGBA',(w,h),(0,0,0,0)); ImageDraw.Draw(sh).text((pad,pad+10),ch,font=f,fill=(0,0,0,235),stroke_width=stroke,stroke_fill=(0,0,0,235))
        sh=sh.filter(IF.GaussianBlur(7)); im=Image.alpha_composite(im,sh)
        ImageDraw.Draw(im).text((pad,pad),ch,font=f,fill=color+(255,),stroke_width=stroke,stroke_fill=(10,10,10,255))
        items.append((i,spr_from_rgba(np.array(im)),xl+adv/2-total/2))
    _LS[key]=(items,asc,desc,pad); return _LS[key]

def dibujar_textos(fr,t,modo):
    ycap={'FULL':1150,'SPLIT':1370,'TAKE':1240}[modo]
    for a,b,txt,col,sz in CAPS:
        if t<a or t>b+0.06: continue
        if txt=='ABCC11': continue
        age=t-a; out=prog(t,b,b+0.05)
        size={'big':240,'n':170,'small':120}[sz]
        items,asc,desc,pad=letras(txt,col,860,size,14 if sz=='big' else 11)
        step=0.016 if sz=='big' else 0.024
        yy=ycap+((60 if modo=='FULL' else -120) if sz=='big' and modo!='TAKE' else 0)
        wsc=1.0+0.03*prog(age,0.25,1.6)
        # centro vertical del texto: mitad de (asc+desc)
        cyoff=(asc+desc)/2
        for (i,spr,dx) in items:
            ai=age-i*step
            if ai<0: continue
            pop=e_back(prog(ai,0,0.22),2.5)
            sc=lerp(0.35,1.0,pop)*wsc*(1-0.10*out)
            if sz=='big': sc*=lerp(1.25,1.0,e_out3(prog(ai,0,0.18)))
            op=clamp(ai/0.07)*(1-out)
            yo=lerp(52,0,e_out3(prog(ai,0,0.24)))-14*out
            rot=lerp(-9,0,e_out3(prog(ai,0,0.22)))*(1 if i%2==0 else -1)
            draw_sprite(fr,spr,520+dx*wsc,yy+yo+0*cyoff,sc,rot,op)

def dibujar_abcc(fr,t):
    a,b=ABC_T
    if not(a<=t<=b+0.1): return
    items,asc,desc,pad=letras('ABCC11',AMB,900,300,16); out=prog(t,b-0.05,b+0.1)
    for k,(i,spr,dx) in enumerate(items):
        ti=ABC[k][0]
        if t<ti: continue
        age=t-ti; sc=lerp(1.45,1.0,e_out3(prog(age,0,0.16)))
        draw_sprite(fr,spr,520+dx,1020+lerp(-30,0,e_out3(prog(age,0,0.16))),sc,0,clamp(age/0.05)*(1-out))

def post(fr,t,i):
    fl=flash_at(t)
    if fl>0.01: fr=cv2.convertScaleAbs(fr,alpha=1+fl,beta=255*fl*0.25)
    # aberracion cromatica breve en los impactos
    for th,_,_,ash,_ in HITS:
        d=t-th
        if 0<=d<0.20 and ash>0:
            k=int(round(9*math.exp(-d/0.06)))
            if k>=1:
                b,g,r=cv2.split(fr)
                r=cv2.warpAffine(r,np.float32([[1,0,k],[0,1,0]]),(W,H),borderMode=cv2.BORDER_REPLICATE)
                b=cv2.warpAffine(b,np.float32([[1,0,-k],[0,1,0]]),(W,H),borderMode=cv2.BORDER_REPLICATE)
                fr=cv2.merge([b,g,r])
    fr=cv2.multiply(fr,VIG,scale=1/255.)
    pos,neg=GRAIN[i%6]; fr=cv2.subtract(cv2.add(fr,pos),neg)
    # fundido final
    f=prog(t,DUR-0.85,DUR)
    if f>0: fr=cv2.convertScaleAbs(fr,alpha=1-f)
    return fr

def cuadro(i):
    t=i/FPS
    k=take_at(t)
    if k is None:
        fr=escena_persona(t); modo='FULL'
        a,b=PEACH_T                                   # duraznito ARRIBA, el texto POTO debajo
        if a<=t<=b+0.25:
            age=t-a; out=prog(t,b,b+0.22)
            sc=lerp(0.1,1.0,e_back(prog(age,0,0.34),2.2))*(1-0.8*out)
            rot=6*math.sin(2*math.pi*1.7*age)*(1-out)
            draw_sprite(fr,PEACH,872,285-34*out,sc*0.62,rot,1-out,shadow=24)
    else:
        fr,M,sc=escena_take(k,t); modo='TAKE'
        ag=t-k[0]
        if ag<0.26 and k[0]>NP+0.1:
            sg_=9.0*(1-e_out3(ag/0.26))
            if sg_>0.5: fr=cv2.GaussianBlur(fr,(0,0),sg_)
        if k[7]=='desenfoque': fr=cv2.GaussianBlur(fr,(0,0),lerp(17,8,e_io3(prog(t,k[0],k[1]))))
        if k[7]=='comen': fr=capa_comen(fr,M,t,k[0],k[1])
        elif k[7]=='vapor': fr=capa_vapor(fr,M,t,k[0],k[1])
        # degradados: abajo (texto) y arriba (insignias)
        yy_=np.clip((np.arange(H,dtype=np.float32)-850)/950,0,1); yy_=yy_*yy_*(3-2*yy_)
        tt_=np.clip(1-np.arange(H,dtype=np.float32)/560,0,1); tt_=tt_*tt_*(3-2*tt_)
        g=((1-0.55*yy_)*(1-0.30*tt_))[:,None,None]
        fr=(fr.astype(np.float32)*g).clip(0,255).astype(np.uint8)
        if not k[2].startswith('bokeh:'): cv2.putText(fr,'ILUSTRACION',(54,1500),cv2.FONT_HERSHEY_SIMPLEX,0.62,(235,235,235),1,cv2.LINE_AA)
        dibujar_insignias(fr,t)
    dibujar_textos(fr,t,modo)
    dibujar_abcc(fr,t)
    return post(fr,t,i)

def render(out,i0=0,i1=None):
    n=int(round(DUR*FPS)); i1=i1 or n
    cmd=['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i','mezcla_master.wav',
         '-map','0:v','-map','1:a','-c:v','libx264','-preset','slow','-crf','19','-maxrate','30M','-bufsize','60M','-pix_fmt','yuv420p','-profile:v','high','-level','4.2',
         '-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart','-shortest',out]
    pr=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for i in range(i0,i1):
        pr.stdin.write(cuadro(i).tobytes())
        if i%150==0: print(f'  cuadro {i}/{n}',flush=True)
    pr.stdin.close(); pr.wait()

if __name__=='__main__':
    cargar()
    if sys.argv[1]=='prev':
        ts=[float(x) for x in sys.argv[2:]]
        ims=[cv2.resize(cuadro(int(round(t*FPS))),(360,640),interpolation=cv2.INTER_AREA) for t in ts]
        for r in range(0,len(ims),6):
            row=ims[r:r+6]; row+= [np.zeros_like(ims[0])]*(6-len(row))
            cv2.imwrite(f'prev_{r//6}.png',np.hstack(row))
        print('prev listo',len(ims))
    elif sys.argv[1]=='full':
        render(sys.argv[2])
