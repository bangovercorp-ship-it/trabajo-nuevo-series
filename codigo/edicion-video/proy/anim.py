"""Insignias animadas (270x270, bucle). Vector + degradados + particulas, renderizadas a 3x y reducidas."""
import numpy as np, cv2, math, colorsys
from PIL import Image, ImageDraw, ImageFilter
S=270; SS=3; N=S*SS; FPS=30
AQ=(96,218,242); AQ2=(28,140,196); AMB=(255,196,70); BL=(255,255,255); RO=(255,92,84)

def sm(x): x=min(1,max(0,x)); return x*x*(3-2*x)
def clamp(x,a=0.0,b=1.0): return max(a,min(b,x))
def e_out(x): x=clamp(x); return 1-(1-x)**3
def e_back(x,s=1.8): x=clamp(x)-1; return 1+(s+1)*x**3+s*x**2
def e_io(x): x=clamp(x); return 4*x**3 if x<.5 else 1-(-2*x+2)**3/2
def lay(): return Image.new('RGBA',(N,N),(0,0,0,0))
def P(pts): return [(x*SS,y*SS) for x,y in pts]
def grad_img(c0,c1,vertical=True):
    t=np.linspace(0,1,N,dtype=np.float32); t=t[:,None] if vertical else t[None,:]
    a=np.array(c0,np.float32); b=np.array(c1,np.float32)
    g=np.broadcast_to((a*(1-t[...,None])+b*t[...,None]),(N,N,3)) if vertical else np.broadcast_to((a*(1-t[...,None])+b*t[...,None]),(N,N,3))
    return g.astype(np.uint8)
def fill_mask(mask,rgb_arr,alpha=1.0):
    """mask: PIL L (N,N); rgb_arr: (N,N,3) uint8 o tupla"""
    L=lay()
    if isinstance(rgb_arr,tuple): arr=np.zeros((N,N,3),np.uint8); arr[:]=rgb_arr
    else: arr=rgb_arr
    m=np.array(mask).astype(np.float32)*alpha
    rgba=np.dstack([arr,m.astype(np.uint8)]); return Image.fromarray(rgba,'RGBA')
def mk(): return Image.new('L',(N,N),0)
def glow(img,r,k=0.6):
    g=img.filter(ImageFilter.GaussianBlur(r*SS)); a=np.array(g); a[...,3]=np.clip(a[...,3]*k,0,255).astype(np.uint8); return Image.fromarray(a,'RGBA')
def over(a,b): return Image.alpha_composite(a,b)
def circ(d,cx,cy,r,fill): d.ellipse([(cx-r)*SS,(cy-r)*SS,(cx+r)*SS,(cy+r)*SS],fill=fill)

_PANEL=None
def panel():
    global _PANEL
    if _PANEL is not None: return _PANEL.copy()
    yy=np.linspace(0,1,N,dtype=np.float32)[:,None]; xx=np.linspace(0,1,N,dtype=np.float32)[None,:]
    top=np.array([40,47,64],np.float32); bot=np.array([10,12,19],np.float32)
    g=top*(1-yy[...,None])+bot*yy[...,None]
    rg=np.clip(1-np.sqrt((xx-0.25)**2+(yy-0.12)**2)/0.85,0,1)**2*26
    img=np.clip(g+rg[...,None],0,255).astype(np.uint8)
    m=mk(); ImageDraw.Draw(m).rounded_rectangle([2*SS,2*SS,(S-2)*SS,(S-2)*SS],radius=46*SS,fill=255)
    base=fill_mask(m,img,0.95)
    # borde con luz arriba-izquierda
    ring=mk(); d=ImageDraw.Draw(ring); d.rounded_rectangle([2*SS,2*SS,(S-2)*SS,(S-2)*SS],radius=46*SS,outline=255,width=int(2.2*SS))
    ga=np.clip(0.75*(1-(xx*0.6+yy*0.8))+0.14,0,1)
    ra=(np.array(ring).astype(np.float32)/255*ga*255).astype(np.uint8)
    edge=np.dstack([np.full((N,N,3),255,np.uint8),ra]); base=over(base,Image.fromarray(edge,'RGBA'))
    _PANEL=base; return base.copy()
def clip_panel(img):
    m=mk(); ImageDraw.Draw(m).rounded_rectangle([2*SS,2*SS,(S-2)*SS,(S-2)*SS],radius=46*SS,fill=255)
    a=np.array(img); a[...,3]=(a[...,3].astype(np.float32)*np.array(m)/255).astype(np.uint8); return Image.fromarray(a,'RGBA')
def final(layers):
    out=panel()
    for L in layers: out=over(out,L)
    return np.array(out.resize((S,S),Image.LANCZOS))

# ---------------------------------------------------------------- burbujas iridiscentes
def burbuja(layer,cx,cy,r,ph=0.0,op=1.0,sat=0.55):
    R=int(r*SS)+4; x0,y0=int(cx*SS)-R,int(cy*SS)-R; n=2*R
    yy,xx=np.mgrid[0:n,0:n].astype(np.float32); dx=(xx-R)/(r*SS); dy=(yy-R)/(r*SS); d=np.sqrt(dx*dx+dy*dy)
    ang=np.arctan2(dy,dx)
    edge=np.clip((d-0.70)/0.30,0,1)**1.4*(d<1.0)
    # pelicula fina: el matiz cambia con el angulo y la distancia
    hue=(ang/(2*np.pi)+d*0.9+ph)%1.0
    h6=hue*6; i=np.floor(h6).astype(int)%6; f=h6-np.floor(h6)
    v=np.ones_like(f); s=sat; p=v*(1-s); q=v*(1-s*f); t=v*(1-s*(1-f))
    r_=np.choose(i,[v,q,p,p,t,v]); g_=np.choose(i,[t,v,v,q,p,p]); b_=np.choose(i,[p,p,t,v,v,q])
    col=np.stack([r_,g_,b_],-1)*255
    a=(edge*0.85+(d<1.0)*0.06)
    # reflejos
    for (hx,hy,hr,ha) in ((-0.42,-0.46,0.20,0.95),(0.38,0.42,0.10,0.55)):
        hd=np.sqrt(((dx-hx)/hr)**2+((dy-hy)/(hr*0.65))**2); hl=np.clip(1-hd,0,1)**1.3
        col=col*(1-hl[...,None])+255*hl[...,None]; a=np.maximum(a,hl*ha)
    a=a*op*(d<1.04)
    spr=Image.fromarray(np.dstack([np.clip(col,0,255).astype(np.uint8),np.clip(a*255,0,255).astype(np.uint8)]),'RGBA')
    sub=Image.new('RGBA',(N,N),(0,0,0,0)); sub.paste(spr,(x0,y0)); return over(layer,sub)

def _gota_poly(cx,cy,r,st=1.0,tip=0.9):
    pts=[]
    for k in range(120):
        th=2*math.pi*k/120
        x=r*math.sin(th)*(math.sin(th/2)**tip)
        y=-r*math.cos(th)*st
        pts.append((cx+x,cy+y))
    return pts
# ---------------------------------------------------------------- utilidades de brillo
def estrella(layer,cx,cy,r,a,col=(255,248,225)):
    d=ImageDraw.Draw(layer)
    for (w,l) in ((1.3,r),(0.9,r*0.55)):
        d.polygon(P([(cx,cy-l),(cx+w*0.9,cy),(cx,cy+l),(cx-w*0.9,cy)]),fill=col+(int(a),))
        d.polygon(P([(cx-l,cy),(cx,cy-w*0.9),(cx+l,cy),(cx,cy+w*0.9)]),fill=col+(int(a),))
    return layer
def _fbm(seed,n=270):
    rng=np.random.default_rng(seed); out=np.zeros((n,n),np.float32); amp=1.0; tot=0
    for o in range(4):
        k=4*2**o; g=rng.random((k+1,k+1)).astype(np.float32); out+=amp*cv2.resize(g,(n,n),interpolation=cv2.INTER_CUBIC); tot+=amp; amp*=0.5
    return out/tot
_NZ=None
def noise_tile():
    global _NZ
    if _NZ is None: _NZ=np.tile(_fbm(4),(1,2))
    return _NZ
def grad_mask(m,c0,c1,vertical=True,alpha=1.0):
    return fill_mask(m,grad_img(c0,c1,vertical),alpha)
def rrmask(b,r):
    m=mk(); ImageDraw.Draw(m).rounded_rectangle([b[0]*SS,b[1]*SS,b[2]*SS,b[3]*SS],radius=r*SS,fill=255); return m

# ---------------------------------------------------------------- SPRAY DE PERFUME
def frasco():
    L=lay()
    halo=lay(); ImageDraw.Draw(halo).rounded_rectangle([38*SS,118*SS,114*SS,246*SS],radius=14*SS,fill=(120,150,200,60)); L=over(L,halo.filter(ImageFilter.GaussianBlur(10*SS)))
    body=grad_mask(rrmask((40,120,112,244),13),(96,112,142),(14,16,26)); L=over(L,body)
    inner=grad_mask(rrmask((44,124,108,240),11),(34,40,58),(6,7,12)); L=over(L,inner)
    refl=lay(); d=ImageDraw.Draw(refl)
    d.rounded_rectangle([47*SS,128*SS,56*SS,236*SS],radius=4*SS,fill=(255,255,255,170))
    d.rounded_rectangle([61*SS,134*SS,65*SS,214*SS],radius=2*SS,fill=(255,255,255,70))
    d.rounded_rectangle([99*SS,134*SS,105*SS,230*SS],radius=3*SS,fill=(190,215,255,90))
    d.arc([42*SS,122*SS,110*SS,150*SS],200,340,fill=(255,255,255,140),width=int(1.6*SS))
    L=over(L,refl)
    lab=grad_mask(rrmask((50,166,102,198),4),(255,226,150),(186,122,30)); L=over(L,lab)
    ln=lay(); ld=ImageDraw.Draw(ln); ld.rectangle([56*SS,177*SS,96*SS,178.6*SS],fill=(70,44,8,170)); ld.rectangle([56*SS,184*SS,84*SS,185.4*SS],fill=(70,44,8,120)); L=over(L,ln)
    neck=grad_mask(rrmask((62,104,90,124),4),(236,240,250),(120,126,144)); L=over(L,neck)
    cap=grad_mask(rrmask((52,66,100,108),9),(255,236,160),(182,116,26),vertical=False); L=over(L,glow(cap,7,0.45)); L=over(L,cap)
    cl=lay(); d=ImageDraw.Draw(cl)
    d.rounded_rectangle([57*SS,70*SS,63*SS,104*SS],radius=3*SS,fill=(255,253,232,230))
    d.rounded_rectangle([86*SS,72*SS,94*SS,104*SS],radius=3*SS,fill=(120,72,10,110)); L=over(L,cl)
    nz=grad_mask(rrmask((96,80,122,92),4),(255,232,150),(176,112,24)); L=over(L,nz)
    return L
_FR=None
def spray(u,L=2.8):
    global _FR
    t=u*L
    if _FR is None: _FR=frasco()
    rng=np.random.default_rng(21); noz=np.array([122.0,86.0])
    D=np.zeros((S,S),np.float32); warm=np.zeros((S,S),np.float32)
    yy,xx=np.mgrid[0:S,0:S].astype(np.float32); parts=[]
    for j in range(380):
        ts=0.10+rng.random()*1.20; tau=t-ts
        life=1.0+rng.random()*0.95
        if tau<0 or tau>life: continue
        ang=math.radians(-22+rng.normal(0,13)); sp=130+rng.random()*230; gam=2.2+rng.random()*0.9
        k=(1-math.exp(-gam*tau))/gam
        px=noz[0]+math.cos(ang)*sp*k+math.sin(tau*5.2+j)*3.4*tau
        py=noz[1]+math.sin(ang)*sp*k-16*tau*tau+math.cos(tau*4.1+j*1.7)*3.4*tau
        u2=tau/life; sg=2.2+7.5*math.sqrt(u2); a=(1-sm(u2))**1.15*(0.45+0.55*rng.random())*clamp(tau/0.045)
        parts.append((px,py,u2,a,j))
        x0,y0=int(px-3*sg),int(py-3*sg); x1,y1=int(px+3*sg)+1,int(py+3*sg)+1
        xa,ya=max(0,x0),max(0,y0); xb,yb=min(S,x1),min(S,y1)
        if xb<=xa or yb<=ya: continue
        g=np.exp(-(((xx[ya:yb,xa:xb]-px)**2+(yy[ya:yb,xa:xb]-py)**2)/(2*sg*sg)))*a
        D[ya:yb,xa:xb]+=g
        if tau<0.35: warm[ya:yb,xa:xb]+=g
    sh=int(t*34)%270; nz_=noise_tile()[:,sh:sh+S]
    cloud=np.clip(D*(0.30+0.95*nz_)*0.78,0,1.0)
    dist=np.clip(np.sqrt((xx-noz[0])**2+(yy-noz[1])**2)/170,0,1)
    col=np.zeros((S,S,3),np.float32); col[...,0]=255-12*dist; col[...,1]=252-6*dist-14*np.clip(warm,0,1); col[...,2]=252-2*dist-38*np.clip(warm,0,1)
    # luz de contorno: realce donde la densidad baja
    rim=np.clip(cv2.GaussianBlur(cloud,(0,0),3)-cloud,0,1)
    cloud_a=np.clip(cloud*0.62+rim*0.55,0,0.68)
    mist=np.dstack([np.clip(col,0,255).astype(np.uint8),(cloud_a*255).astype(np.uint8)])
    mist=cv2.resize(mist,(N,N),interpolation=cv2.INTER_CUBIC); mist_img=Image.fromarray(mist,'RGBA')
    # gotitas finas y destellos
    fine=lay(); fd=ImageDraw.Draw(fine)
    for (px,py,u2,a,j) in parts:
        circ(fd,px,py,0.8+0.9*((j*7)%5)/5,(255,248,236,int(235*a)))
    spk=lay()
    for (px,py,u2,a,j) in parts:
        if j%7==0 and a>0.25:
            tw=0.5+0.5*math.sin(t*14+j); estrella(spk,px,py,3+4*tw,200*a*tw)
    layers=[fine,glow(spk,3,0.8),spk]
    # cono de luz del disparo
    fl=math.exp(-((t-0.22)/0.12)**2)
    cone=lay()
    if fl>0.02:
        cd=ImageDraw.Draw(cone); cd.polygon(P([(noz[0],noz[1]-2),(noz[0]+130,noz[1]-70),(noz[0]+150,noz[1]+10)]),fill=(255,240,200,int(70*fl)))
        circ(cd,noz[0],noz[1],9,(255,244,214,int(210*fl))); cone=cone.filter(ImageFilter.GaussianBlur(8*SS))
    scene=over(over(lay(),_FR),cone); scene=over(scene,mist_img)
    for l in layers: scene=over(scene,l)
    # al "prohibir" todo el efecto se atenua
    p=sm((t-1.55)/0.45); dim=1-0.52*p*(1-sm((t-2.55)/0.25))
    a=np.array(scene).astype(np.float32); a[...,:3]*=dim; scene=Image.fromarray(a.clip(0,255).astype(np.uint8),'RGBA')
    out=[scene]
    ring=lay(); rd=ImageDraw.Draw(ring); c=(S/2+2,S/2+4); r=98; fade=1-sm((t-2.50)/0.30)
    pr=sm((t-1.45)/0.55)
    if pr>0:
        steps=int(140*pr); pts=[(c[0]+r*math.cos(-math.pi/2+2*math.pi*(k/140)),c[1]+r*math.sin(-math.pi/2+2*math.pi*(k/140))) for k in range(steps+1)]
        colr=(255,104,96,int(255*fade))
        if len(pts)>1: rd.line(P(pts),fill=colr,width=int(6*SS),joint='curve')
        q=sm((t-1.90)/0.34)
        if q>0:
            k=r*0.7071; a0=(c[0]-k,c[1]+k); a1=(c[0]-k+2*k*q,c[1]+k-2*k*q); rd.line(P([a0,a1]),fill=colr,width=int(6*SS))
        for (x,y) in (pts[0],pts[-1]): circ(rd,x,y,3.5,colr)
        out+=[glow(ring,7,0.7),ring]
    return final([clip_panel(l) for l in out])

# ---------------------------------------------------------------- JABON (espuma, gotas y burbujas)
def gotita(layer,x,y,r,a=255,trail=0.0):
    d=ImageDraw.Draw(layer)
    if trail>0:
        for k in range(6):
            f=k/6; d.ellipse([(x-r*(1-f*0.6))*SS,(y-trail*f-r*(1-f*0.6))*SS,(x+r*(1-f*0.6))*SS,(y-trail*f+r*(1-f*0.6))*SS],fill=AQ+(int(a*0.18*(1-f)),))
    pts=[(x+r*0.82*math.sin(th)*(math.sin(th/2)**0.9),y-r*1.15*math.cos(th)+r*0.2) for th in np.linspace(0,2*math.pi,40)]
    d.polygon(P(pts),fill=(70,190,235,a)); d.polygon(P([(x+(px-x)*0.80,y+(py-y)*0.80) for px,py in pts]),fill=(150,226,250,a))
    d.ellipse([(x-r*0.55)*SS,(y-r*0.45)*SS,(x-r*0.15)*SS,(y+r*0.15)*SS],fill=(255,255,255,int(a*0.9)))
    return layer
def jabon(u,L=2.4):
    t=u*L; out=[]
    # --- espuma: burbujas pequenas empaquetadas
    foam=lay(); rng=np.random.default_rng(9)
    pos=[(135+rng.normal(0,38),228+rng.normal(0,7),8+rng.random()*13) for _ in range(46)]
    pos.sort(key=lambda p:p[1]-p[2]*0.0)
    base=lay(); bd=ImageDraw.Draw(base)
    for j,(x,y,r) in enumerate(pos):
        rr=r*(1+0.045*math.sin(t*2.7+j)); circ(bd,x,y,rr*0.96,(232,240,255,92))
    foam=over(foam,glow(base,4,0.6)); foam=over(foam,base)
    for j,(x,y,r) in enumerate(pos):
        rr=r*(1+0.045*math.sin(t*2.7+j)); foam=burbuja(foam,x,y,rr,ph=j*0.11,op=0.80,sat=0.30)
    out.append(foam)
    # --- gotas que caen y golpean la espuma
    dr=lay(); sp=lay(); rng2=np.random.default_rng(14)
    for j in range(15):
        t0=rng2.random()*L; per=0.62+rng2.random()*0.40; ph=((t-t0)/per)%1.0
        x=40+rng2.random()*100; y=-10+ph*(212); r=2.8+rng2.random()*2.2
        if ph<0.96:
            gotita(dr,x+ph*8,y,r,a=235,trail=18)
        else:
            k=(ph-0.96)/0.04
    out.append(glow(dr,3,0.45)); out.append(dr)
    # --- burbujas que suben, brillan y estallan
    bb=lay(); rng3=np.random.default_rng(3)
    for j in range(11):
        t0=rng3.random()*L; per=2.0+rng3.random()*1.0; ph=((t-t0)/per)%1.0
        x0=70+rng3.random()*130; r=9+rng3.random()*14
        y=214-ph*182; x=x0+math.sin(ph*6.4+j)*11+ph*10
        op=clamp(ph/0.07)*(1-sm((ph-0.90)/0.10))
        bb=burbuja(bb,x,y,r*(0.5+0.5*sm(ph/0.25)),ph=j*0.13+ph*0.4,op=op)
        if ph>0.90:
            k=(ph-0.90)/0.10; rg=lay(); rdr=ImageDraw.Draw(rg); rr_=r*(1+1.3*k)
            rdr.ellipse([(x-rr_)*SS,(y-rr_)*SS,(x+rr_)*SS,(y+rr_)*SS],outline=(255,255,255,int(210*(1-k))),width=int(1.5*SS))
            for q in range(7):
                an=q*0.9+j; rdr.ellipse([(x+math.cos(an)*rr_*1.25-1.4)*SS,(y+math.sin(an)*rr_*1.25-1.4)*SS,(x+math.cos(an)*rr_*1.25+1.4)*SS,(y+math.sin(an)*rr_*1.25+1.4)*SS],fill=(255,255,255,int(200*(1-k))))
            bb=over(bb,rg)
    out.append(bb)
    # --- destellos de limpio
    st=lay()
    for j,(x,y,ph) in enumerate(((212,70,0.0),(60,96,0.4),(236,150,0.7),(36,170,0.2))):
        tw=max(0,math.sin(2*math.pi*((t/L*1.0+ph)%1.0)))**3; estrella(st,x,y,4+9*tw,235*tw)
    out+= [glow(st,3,0.8),st]
    return final([clip_panel(l) for l in out])

# ---------------------------------------------------------------- GOTA (brillante, con reflejo y corona)
def gota(u,L=2.4):
    t=u*L; out=[]; yw=190
    pres=(1-sm((t-0.80)/0.38)) if t<1.18 else 0.0
    halo=lay(); hd=ImageDraw.Draw(halo); circ(hd,135,78,70,(70,190,240,int(78*pres))); out.append(halo.filter(ImageFilter.GaussianBlur(24*SS)))
    water=lay(); wd=ImageDraw.Draw(water)
    wm=mk(); ImageDraw.Draw(wm).rectangle([0,yw*SS,N,N],fill=255)
    out.append(fill_mask(wm,grad_img((60,170,220),(14,70,120)),0.55) if False else grad_mask(wm,(70,176,226),(12,64,112),alpha=0.62))
    ln=lay(); ImageDraw.Draw(ln).rectangle([0,yw*SS,N,int((yw+2.2)*SS)],fill=(214,246,255,235)); out.append(glow(ln,2.5,0.6)); out.append(ln)
    tf,ti=0.86,1.18
    drop=lay(); refl=lay()
    def draw_drop(target,cx,cy,r,st,aa=255):
        pts=_gota_poly(cx,cy,r,st)
        m=mk(); ImageDraw.Draw(m).polygon(P(pts),fill=255)
        body=grad_mask(m,(190,242,255),(26,130,200),alpha=aa/255); target=over(target,glow(body,10,0.7)); target=over(target,body)
        hl=lay(); hd=ImageDraw.Draw(hl); hx,hy=cx-r*0.40,cy-r*0.06*st
        hd.ellipse([(hx-r*0.14)*SS,(hy-r*0.50*st)*SS,(hx+r*0.14)*SS,(hy+r*0.44*st)*SS],fill=(255,255,255,int(240*aa/255)))
        hd.ellipse([(cx+r*0.28)*SS,(cy+r*0.32*st)*SS,(cx+r*0.42)*SS,(cy+r*0.48*st)*SS],fill=(255,255,255,int(150*aa/255)))
        target=over(target,hl)
        ro=lay(); ImageDraw.Draw(ro).line(P(pts+[pts[0]]),fill=(226,250,255,int(180*aa/255)),width=int(1.4*SS)); return over(target,ro)
    if t<ti:
        if t<tf:
            g=e_back(t/tf,2.4); r=34*g; cx,cy=135,76+2.5*math.sin(t*8)*(1-t/tf); st=1.0+0.07*math.sin(t*9.5)
        else:
            f=(t-tf)/(ti-tf); cy=76+(yw-34-76)*f*f; r=34; cx=135; st=1.0+0.55*f
        drop=draw_drop(drop,cx,cy,r,st)
        # reflejo en el agua (espejo atenuado)
    out+=[refl,drop]
    if t>=ti:
        k=t-ti; rip=lay(); rd=ImageDraw.Draw(rip)
        for q in range(3):
            kk=k-q*0.15
            if kk<0: continue
            rx=14+kk*160; ry=rx*0.21; a=int(240*(1-sm(kk/1.0)))
            if a<=2: continue
            rd.ellipse([(135-rx)*SS,(yw+10-ry)*SS,(135+rx)*SS,(yw+10+ry)*SS],outline=(214,246,255,a),width=int((3.8-q*0.8)*SS))
        out+=[glow(rip,5,0.7),rip]
        spl=lay(); sd=ImageDraw.Draw(spl)
        for j in range(9):
            vx=(j-4)*22; vy=-(150+(j%3)*34); tt=k
            if tt>0.60: continue
            x=135+vx*tt; y=yw+vy*tt+540*tt*tt; r=5.2-3.0*(tt/0.60); a=int(250*(1-tt/0.60))
            circ(sd,x,y,max(1.6,r*1.15),(214,248,255,a)); circ(sd,x-r*0.3,y-r*0.3,max(0.8,r*0.4),(255,255,255,a))
        out+=[glow(spl,3,0.6),spl]
    return final([clip_panel(l) for l in out])

if __name__=='__main__':
    import sys
    fr={}
    for nm,fn,L in (('spray',spray,2.8),('jabon',jabon,2.4),('gota',gota,2.4)):
        us=[0.10,0.25,0.40,0.55,0.70,0.85]
        fr[nm]=np.hstack([fn(u,L) for u in us])
    sheet=np.vstack([fr[k] for k in ('spray','jabon','gota')])
    bg=np.full(sheet.shape[:2]+(3,),(70,50,90),np.uint8)
    a=sheet[...,3:4]/255.0; rgb=(sheet[...,:3]*a+bg*(1-a)).astype(np.uint8)
    cv2.imwrite('assets/_anim1.png',cv2.cvtColor(rgb,cv2.COLOR_RGB2BGR)); print('ok')
