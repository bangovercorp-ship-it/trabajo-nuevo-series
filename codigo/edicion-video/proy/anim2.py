from anim import *
from anim import _gota_poly
import math
# ------------------------------------------------------------ SAL: cristales 3D que giran y destellan
_CARAS=[((0,0,1),[(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]),((0,0,-1),[(-1,-1,-1),(-1,1,-1),(1,1,-1),(1,-1,-1)]),
        ((1,0,0),[(1,-1,-1),(1,1,-1),(1,1,1),(1,-1,1)]),((-1,0,0),[(-1,-1,-1),(-1,-1,1),(-1,1,1),(-1,1,-1)]),
        ((0,1,0),[(-1,1,-1),(-1,1,1),(1,1,1),(1,1,-1)]),((0,-1,0),[(-1,-1,-1),(1,-1,-1),(1,-1,1),(-1,-1,1)])]
def cubo(layer,cx,cy,s,ang,tilt=0.62):
    ca,sa,ct,st=math.cos(ang),math.sin(ang),math.cos(tilt),math.sin(tilt)
    def rot(p):
        x,y,z=p; x2=x*ca+z*sa; z2=-x*sa+z*ca; y2=y*ct-z2*st; z3=y*st+z2*ct; return x2,y2,z3
    L=np.array([-0.45,-0.72,0.55]); L/=np.linalg.norm(L); d=ImageDraw.Draw(layer)
    vis=[]
    for n,vs in _CARAS:
        nx,ny,nz=rot(n)
        if nz>0.02:
            lum=clamp(nx*L[0]+ny*L[1]+nz*L[2],0,1); pts=[(cx+rot(v)[0]*s*0.5,cy+rot(v)[1]*s*0.5) for v in vs]; vis.append((nz,lum,pts))
    for nz,lum,pts in sorted(vis,key=lambda v:v[0]):
        c=(int(150+95*lum),int(166+86*lum),int(196+58*lum)); d.polygon(P(pts),fill=c+(255,))
        d.line(P(pts+[pts[0]]),fill=(255,255,255,int(170+60*lum)),width=int(1.3*SS))
    return layer
def sal(u,L=3.0):
    t=u*L; out=[]; cubes=[(92,128,52,0.2,1),(176,96,38,1.1,-1),(184,176,44,2.0,1),(78,200,30,0.7,-2),(138,56,24,1.6,2)]
    bg=lay(); bd=ImageDraw.Draw(bg); circ(bd,135,135,92,(70,110,190,60)); out.append(bg.filter(ImageFilter.GaussianBlur(26*SS)))
    cl=lay(); sp=lay(); rng=np.random.default_rng(2)
    for i,(x,y,s,ph,k) in enumerate(cubes):
        ang=ph+k*math.pi/2*u; bob=4*math.sin(2*math.pi*(u+ph/6.28)); cubo(cl,x,y+bob,s,ang,tilt=0.55+0.1*math.sin(2*math.pi*u*(1 if k>0 else 2)))
        tw=max(0,math.sin(2*math.pi*(u*1+ph*0.31)))**4; estrella(sp,x+s*0.38,y+bob-s*0.38,3+10*tw,240*tw)
    out+=[glow(cl,6,0.40),cl,glow(sp,3,0.8),sp]
    return final([clip_panel(l) for l in out])

# ------------------------------------------------------------ SIN OLOR: aromas que se disipan y aro que se dibuja
def aro(layer_list,t,t0,col=(255,255,255),r=86,c=(135,135),width=6.0):
    pr=sm((t-t0)/0.55); ring=lay(); rd=ImageDraw.Draw(ring)
    if pr<=0: return
    steps=int(140*pr); pts=[(c[0]+r*math.cos(-math.pi/2+2*math.pi*(k/140)),c[1]+r*math.sin(-math.pi/2+2*math.pi*(k/140))) for k in range(steps+1)]
    cc=col+(255,)
    if len(pts)>1: rd.line(P(pts),fill=cc,width=int(width*SS),joint='curve')
    q=sm((t-t0-0.40)/0.34)
    if q>0:
        k=r*0.7071; a0=(c[0]-k,c[1]+k); a1=(c[0]-k+2*k*q,c[1]+k-2*k*q); rd.line(P([a0,a1]),fill=cc,width=int(width*SS))
    for (x,y) in (pts[0],pts[-1]): circ(rd,x,y,width/2,cc)
    layer_list+= [glow(ring,7,0.7),ring]
def sinolor(u,L=2.4):
    t=u*L; out=[]; p=sm((t-0.35)/0.7); fade=1-sm((t-2.05)/0.3)
    w=lay(); wd=ImageDraw.Draw(w)
    for i,cx in enumerate((98,135,172)):
        pts=[]; 
        for k in range(60):
            q=k/59; y=218-q*170; x=cx+math.sin(q*7.2-2*math.pi*u*2+i*1.9)*(9+16*q)*(1-0.0)
            pts.append((x,y))
        for k in range(59):
            q=k/59; a=int(255*(1-q)**0.8*(1-0.65*p)*fade)
            wd.line(P([pts[k],pts[k+1]]),fill=AMB+(a,),width=int((9-5*q)*SS))
    out+=[glow(w,6,0.7),w]
    ring=[]; aro(ring,t,0.40,col=(255,255,255)); 
    if fade<1:
        pass
    # el aro se desvanece al final
    for l in ring:
        a=np.array(l); a[...,3]=(a[...,3]*fade).astype(np.uint8); out.append(Image.fromarray(a,'RGBA'))
    return final([clip_panel(l) for l in out])

# ------------------------------------------------------------ CUERPO: silueta suave con zona que late
_BM=None
def silueta():
    global _BM
    if _BM is not None: return _BM
    m=mk(); d=ImageDraw.Draw(m); cx=135
    d.ellipse([(cx-19)*SS,26*SS,(cx+19)*SS,64*SS],fill=255)
    d.rectangle([(cx-8)*SS,58*SS,(cx+8)*SS,76*SS],fill=255)
    d.polygon(P([(cx-46,78),(cx+46,78),(cx+30,150),(cx+36,172),(cx-36,172),(cx-30,150)]),fill=255)
    for sg in (-1,1):
        d.line(P([(cx+sg*44,86),(cx+sg*80,124),(cx+sg*96,160)]),fill=255,width=int(17*SS),joint='curve')
        d.ellipse([(cx+sg*96-9)*SS,(160-9)*SS,(cx+sg*96+9)*SS,(160+9)*SS],fill=255)
        d.line(P([(cx+sg*17,166),(cx+sg*20,236)]),fill=255,width=int(26*SS))
        d.ellipse([(cx+sg*20-14)*SS,226*SS,(cx+sg*20+(14+8*sg if sg>0 else 14))*SS if False else (cx+sg*20+14)*SS,246*SS],fill=255)
    a=np.array(m).astype(np.float32)/255; a=cv2.GaussianBlur(a,(0,0),6*SS); a=np.clip((a-0.38)/0.22,0,1); a=a*a*(3-2*a)
    _BM=Image.fromarray((a*255).astype(np.uint8),'L'); return _BM
def cuerpo(zona,u,L=2.0):
    t=u*L; out=[]; m=silueta(); arr=np.array(m).astype(np.float32)/255
    body=fill_mask(m,grad_img((104,122,152),(34,42,60)),1.0); out+=[glow(body,8,0.25),body]
    er=cv2.erode(np.array(m),np.ones((int(4*SS),int(4*SS)),np.uint8)); edge=cv2.GaussianBlur((np.array(m)-er).astype(np.float32),(0,0),2*SS/2)/255
    yy,xx=np.mgrid[0:N,0:N].astype(np.float32)/N; lg=np.clip(1.15-(xx*0.8+yy*0.5),0,1)
    rim=np.dstack([np.full((N,N),200,np.uint8),np.full((N,N),224,np.uint8),np.full((N,N),255,np.uint8),(np.clip(edge*1.6,0,1)*lg*235).astype(np.uint8)]); out.append(Image.fromarray(rim,'RGBA'))
    pts={'axilas':[(135-37,100),(135+37,100)],'ingle':[(135,170)],'pies':[(135-20,238),(135+20,238)]}[zona]
    hl=lay(); hd=ImageDraw.Draw(hl); ring=lay(); rd=ImageDraw.Draw(ring)
    for (x,y) in pts:
        pulse=0.5+0.5*math.sin(2*math.pi*u*2)
        circ(hd,x,y,7+2*pulse,(255,214,120,255)); 
        for q in range(2):
            ph=((u*2+q*0.5)%1.0); r=6+34*ph; a=int(235*(1-ph)**1.4)
            rd.ellipse([(x-r)*SS,(y-r)*SS,(x+r)*SS,(y+r)*SS],outline=(255,206,100,a),width=int(2.6*SS))
    out+=[glow(hl,12,0.9),glow(ring,4,0.6),ring,hl]
    return final([clip_panel(l) for l in out])

# ------------------------------------------------------------ GLANDULA: gotas viajando por el conducto
def bez(p0,p1,p2,p3,q):
    a=(1-q)**3; b=3*q*(1-q)**2; c=3*q*q*(1-q); d=q**3
    return (a*p0[0]+b*p1[0]+c*p2[0]+d*p3[0], a*p0[1]+b*p1[1]+c*p2[1]+d*p3[1])
def tubo(layer,pts,w,c_out,c_in,c_hi):
    d=ImageDraw.Draw(layer)
    d.line(P(pts),fill=c_out+(255,),width=int(w*1.35*SS),joint='curve'); d.line(P(pts),fill=c_in+(255,),width=int(w*SS),joint='curve')
    d.line(P([(x-w*0.16,y-w*0.18) for x,y in pts]),fill=c_hi+(235,),width=int(w*0.34*SS),joint='curve')
    for (x,y) in (pts[0],pts[-1]): circ(d,x,y,w*0.68,c_in+(255,))
def glandula(u,L=2.6):
    t=u*L; out=[]
    yy=np.linspace(0,1,N,dtype=np.float32)[:,None]
    epi=np.array([238,168,150],np.float32); der=np.array([214,134,118],np.float32); der2=np.array([186,104,98],np.float32); hip=np.array([240,206,130],np.float32)
    col=np.where(yy<0.17,epi,np.where(yy<0.72,der*(1-(yy-0.17)/0.55*0.5)+der2*((yy-0.17)/0.55*0.5),hip)); col=np.broadcast_to(col[:,None,:] if col.ndim==2 else col,(N,N,3)) if False else None
    bg=np.zeros((N,N,3),np.float32)
    for y in range(N):
        v=y/N
        bg[y,:,:]=epi if v<0.17 else (der*(1-(v-0.17)/0.55)+der2*((v-0.17)/0.55) if v<0.72 else hip)
    # frontera ondulada epidermis/dermis
    xx=np.arange(N)/N; wob=0.17+0.018*np.sin(xx*18)
    for x in range(0,N): 
        y0=int(wob[x]*N); bg[y0-4:y0+4,x,:]*=0.88
    out.append(Image.fromarray(np.dstack([np.clip(bg,0,255).astype(np.uint8),np.full((N,N),255,np.uint8)]),'RGBA'))
    tex=lay(); td=ImageDraw.Draw(tex); rng=np.random.default_rng(3)
    for _ in range(26): circ(td,rng.uniform(10,260),rng.uniform(205,262),rng.uniform(7,14),(255,226,150,70))
    out.append(tex)
    # foliculo + pelo
    fol=lay(); tubo(fol,[(78,6),(88,60),(96,120),(98,150)],20,(70,38,34),(112,66,58),(166,112,98))
    hr=ImageDraw.Draw(fol); hr.line(P([(78,8),(70,-14)]),fill=(26,20,18,255),width=int(4*SS))
    out+=[glow(fol,4,0.2),fol]
    # conducto + glandula enrollada
    p0,p1,p2,p3=(176,196),(176,150),(212,110),(186,36)
    pts=[bez(p0,p1,p2,p3,q/60) for q in range(61)]
    coil=[]
    for k in range(150):
        a=k/150*math.pi*2*3.2; r=8+k/150*24; coil.append((176+math.cos(a)*r*1.25,226+math.sin(a)*r*0.7))
    cl=lay(); tubo(cl,coil,8.5,(150,92,20),(244,184,64),(255,236,170)); tubo(cl,pts,6.5,(150,92,20),(244,184,64),(255,236,170))
    out+=[glow(cl,5,0.28),cl]
    dr=lay(); dd=ImageDraw.Draw(dr)
    for i in range(3):
        q=((u*1.0+i/3)%1.0); x,y=bez(p0,p1,p2,p3,q); r=4.6+1.2*math.sin(q*math.pi); a=int(255*clamp(q*8)*(1-sm((q-0.9)/0.1)))
        circ(dd,x,y,r,(110,214,244,a)); circ(dd,x-r*0.3,y-r*0.3,r*0.38,(255,255,255,a))
    out+=[glow(dr,5,0.9),dr]
    # perla de sudor en el poro
    bd=lay(); bdd=ImageDraw.Draw(bd); g=sm(((u+0.15)%1.0)/0.8)*(1-sm((((u+0.15)%1.0)-0.85)/0.15)); r=2+8*g
    circ(bdd,186,32,r,(120,220,248,int(240*g))); circ(bdd,186-r*0.3,32-r*0.3,r*0.36,(255,255,255,int(255*g))); out+=[glow(bd,5,0.7),bd]
    return final([clip_panel(l) for l in out])

# ------------------------------------------------------------ SUDOR != OLOR
def drop_icon(layer,cx,cy,r,aa=255):
    pts=_gota_poly(cx,cy,r,1.0); m=mk(); ImageDraw.Draw(m).polygon(P(pts),fill=255)
    body=grad_mask(m,(190,242,255),(26,130,200),alpha=aa/255); layer=over(layer,glow(body,8,0.6)); layer=over(layer,body)
    hl=lay(); hd=ImageDraw.Draw(hl); hd.ellipse([(cx-r*0.46)*SS,(cy-r*0.52)*SS,(cx-r*0.2)*SS,(cy+r*0.30)*SS],fill=(255,255,255,int(235*aa/255))); return over(layer,hl)
def igual(u,L=2.6):
    t=u*L; out=[]; fade=1-sm((t-2.3)/0.25)
    dl=lay(); sc=e_back(t/0.45,2.2); 
    if sc>0.01: dl=drop_icon(dl,60,138,38*sc)
    out.append(dl)
    bars=lay(); bd=ImageDraw.Draw(bars); s1=e_out((t-0.25)/0.35)
    for yy in (112,152):
        x0=104+ (1-s1)*-30; bd.rounded_rectangle([x0*SS,yy*SS,(x0+62)*SS,(yy+14)*SS],radius=6*SS,fill=(255,255,255,int(255*s1*fade)))
    out+=[glow(bars,5,0.5),bars]
    sl=lay(); q=sm((t-0.75)/0.34)
    if q>0:
        sd=ImageDraw.Draw(sl); a0=(120,184); a1=(120+30*q,184-84*q); sd.line(P([a0,a1]),fill=RO+(int(255*fade),),width=int(10*SS)); circ(sd,*a0,5,RO+(int(255*fade),))
        if q>0.98: circ(sd,*a1,5,RO+(int(255*fade),))
    out+=[glow(sl,6,0.8),sl]
    w=lay(); wd=ImageDraw.Draw(w); appear=sm((t-0.55)/0.4)
    for i,cx in enumerate((214,234,254)):
        cx=cx-12
        pts=[(cx+math.sin(k/59*7-2*math.pi*u*2+i*1.9)*(5+8*k/59),208-k/59*108) for k in range(60)]
        for k in range(59):
            qq=k/59; a=int(255*(1-qq)**0.8*appear*fade); wd.line(P([pts[k],pts[k+1]]),fill=AMB+(a,),width=int((7-4*qq)*SS))
    out+=[glow(w,5,0.7),w]
    return final([clip_panel(l) for l in out])

# ------------------------------------------------------------ GENTE: la mayoria huele, algunos casi nada
def persona(layer,cx,cy,r,col,a=255):
    d=ImageDraw.Draw(layer); d.ellipse([(cx-r)*SS,(cy-r*1.9)*SS,(cx+r)*SS,(cy-r*0.15)*SS],fill=col+(a,))
    d.pieslice([(cx-r*1.75)*SS,(cy+r*0.15)*SS,(cx+r*1.75)*SS,(cy+r*3.6)*SS],180,360,fill=col+(a,))
def gente(u,L=2.4):
    t=u*L; out=[]; xs=(40,87,135,183,230); raros=(1,3)
    pl=lay(); wl=lay(); wd=ImageDraw.Draw(wl); sp=lay()
    for i,x in enumerate(xs):
        bob=1.8*math.sin(2*math.pi*(u+i*0.17)); raro=i in raros
        col=(96,226,232) if raro else (168,174,190)
        pa=lay(); persona(pa,x,168+bob,13.5,col); pl=over(pl,pa)
        if not raro:
            for dxo in (-6,6):
                pts=[(x+dxo+math.sin(k/29*6-2*math.pi*u*2+i+dxo)*(2.5+5*k/29),128+bob-k/29*62) for k in range(30)]
                for k in range(29):
                    q=k/29; a=int(240*(1-q)**0.8); wd.line(P([pts[k],pts[k+1]]),fill=AMB+(a,),width=int((5-3*q)*SS))
        else:
            tw=max(0,math.sin(2*math.pi*(u*1+i*0.23)))**3; estrella(sp,x,100+bob,4+10*tw,240*tw,col=(180,250,255))
    out+=[glow(pl,5,0.3),pl,glow(wl,5,0.7),wl,glow(sp,3,0.9),sp]
    return final([clip_panel(l) for l in out])

# ------------------------------------------------------------ ADN 3D giratorio
def adn(u,L=3.0):
    t=u*L; out=[]; layer=lay(); d=ImageDraw.Draw(layer); n=24; items=[]
    for i in range(n):
        q=i/(n-1); y=34+q*204; ph=q*2*math.pi*1.55+2*math.pi*u; x1=135+46*math.sin(ph); z1=math.cos(ph); x2=135-46*math.sin(ph); z2=-z1
        gen=8<=i<=14; items+= [(z1,'a',x1,y,gen),(z2,'b',x2,y,gen),(0,'r',(x1,x2),y,gen)]
    pts_a=[(x,y) for z,k,x,y,g in items if k=='a']; pts_b=[(x,y) for z,k,x,y,g in items if k=='b']
    d.line(P(pts_a),fill=(70,120,160,255),width=int(3.4*SS),joint='curve'); d.line(P(pts_b),fill=(60,100,150,255),width=int(3.4*SS),joint='curve')
    for z,k,x,y,g in sorted(items,key=lambda it:it[0]):
        if k=='r':
            c=(255,196,70) if g else (80,150,200); d.line(P([(x[0],y),(x[1],y)]),fill=c+(255,),width=int(2.6*SS))
        else:
            r=6.2+2.4*z; base=(255,205,100) if g else ((96,222,244) if k=='a' else (70,140,240)); sh=0.62+0.38*(z*0.5+0.5)
            c=tuple(int(v*sh) for v in base); circ(d,x,y,r,c+(255,)); circ(d,x-r*0.3,y-r*0.32,r*0.38,(255,255,255,int(170+60*z)))
    out+=[glow(layer,7,0.55),layer]
    return final([clip_panel(l) for l in out])

# ------------------------------------------------------------ TOALLA (pila limpia con destellos)
def toalla(u,L=2.4):
    t=u*L; out=[]
    sh=lay(); ImageDraw.Draw(sh).rounded_rectangle([54*SS,152*SS,226*SS,222*SS],radius=20*SS,fill=(0,0,0,170)); out.append(sh.filter(ImageFilter.GaussianBlur(12*SS)))
    rng=np.random.default_rng(5)
    def toall(box,c0,c1,bob,franja=True):
        l=lay(); x0,y0,x1,y1=box; y0+=bob; y1+=bob
        m=rrmask((x0,y0,x1,y1),15); base=grad_mask(m,c0,c1); l=over(l,base)
        top=lay(); ImageDraw.Draw(top).rounded_rectangle([(x0+3)*SS,(y0+2)*SS,(x1-3)*SS,(y0+9)*SS],radius=6*SS,fill=(255,255,255,120)); l=over(l,top)
        ma=np.array(m)
        if franja:
            st=lay(); sd=ImageDraw.Draw(st)
            for (a_,b_) in ((x0+14,x0+19),(x0+25,x0+29),(x1-19,x1-14),(x1-29,x1-25)): sd.rectangle([a_*SS,y0*SS,b_*SS,y1*SS],fill=(246,170,52,255))
            sa=np.array(st); sa[...,3]=(sa[...,3].astype(np.float32)*ma/255).astype(np.uint8); l=over(l,Image.fromarray(sa,'RGBA'))
        fl=lay(); fd=ImageDraw.Draw(fl)
        for _ in range(140):
            x=rng.uniform(x0+8,x1-8); y=rng.uniform(y0+8,y1-6); fd.line([(x*SS,y*SS),((x+rng.uniform(-1.5,1.5))*SS,(y+rng.uniform(2,4))*SS)],fill=(190,176,150,90),width=int(1.1*SS))
        fa=np.array(fl); fa[...,3]=(fa[...,3].astype(np.float32)*ma/255).astype(np.uint8); return over(l,Image.fromarray(fa,'RGBA'))
    b1=1.6*math.sin(2*math.pi*(u+0.0)); b2=2.0*math.sin(2*math.pi*(u+0.18)); b3=2.4*math.sin(2*math.pi*(u+0.36))
    out.append(toall((50,168,220,212),(236,230,218),(196,188,170),b1,False))
    out.append(toall((56,128,214,176),(250,246,236),(214,206,190),b2,True))
    out.append(toall((62,86,208,134),(255,252,244),(224,216,200),b3,True))
    ev=lay(); ed=ImageDraw.Draw(ev); rng2=np.random.default_rng(8)
    for j in range(8):
        ph=((u*1.0+rng2.random())%1.0); x=70+rng2.random()*130+math.sin(ph*6+j)*5; y=84-ph*62; r=3.4*(1-0.5*ph); a=int(235*sm(ph/0.15)*(1-sm((ph-0.55)/0.45)))
        circ(ed,x,y,r,(130,220,248,a)); circ(ed,x-r*0.3,y-r*0.3,r*0.4,(255,255,255,a))
    sp=lay()
    for j,(x,y,ph) in enumerate(((52,92,0.0),(214,100,0.4),(226,176,0.7),(40,166,0.2),(135,70,0.55))):
        tw_=max(0,math.sin(2*math.pi*((u+ph)%1.0)))**3; estrella(sp,x,y,4+10*tw_,240*tw_)
    out+=[glow(ev,3,0.6),ev,glow(sp,3,0.9),sp]
    return final([clip_panel(l) for l in out])

# ------------------------------------------------------------ MICROSCOPIO (lente con bacterias a la deriva)
def varilla(layer,x,y,L_,w,ang,col,hi):
    d=ImageDraw.Draw(layer); dx,dy=math.cos(ang)*L_/2,math.sin(ang)*L_/2
    d.line(P([(x-dx,y-dy),(x+dx,y+dy)]),fill=col+(255,),width=int(w*SS)); 
    for e in (-1,1): circ(d,x+e*dx,y+e*dy,w/2,col+(255,))
    d.line(P([(x-dx*0.8-w*0.18,y-dy*0.8-w*0.2),(x+dx*0.8-w*0.18,y+dy*0.8-w*0.2)]),fill=hi+(235,),width=int(w*0.3*SS))
def micro(u,L=4.0):
    t=u*L; out=[]; cx,cy,R=135,135,112
    lens=mk(); ImageDraw.Draw(lens).ellipse([(cx-R)*SS,(cy-R)*SS,(cx+R)*SS,(cy+R)*SS],fill=255)
    yy,xx=np.mgrid[0:N,0:N].astype(np.float32); rr=np.sqrt((xx-cx*SS)**2+(yy-cy*SS)**2)/(R*SS)
    bgc=np.zeros((N,N,3),np.float32); bgc[...]=np.array([6,52,64],np.float32)+np.clip(1-rr,0,1)[...,None]*np.array([20,60,66],np.float32)
    inner=fill_mask(lens,np.clip(bgc,0,255).astype(np.uint8),1.0)
    rng=np.random.default_rng(11); back=lay(); front=lay()
    for i in range(7):
        x0,y0=rng.uniform(40,230),rng.uniform(40,230); ph=rng.random(); ang0=rng.uniform(0,3.14); Lr=rng.uniform(46,70); w=rng.uniform(11,15)
        x=x0+14*math.sin(2*math.pi*(u+ph)); y=y0+10*math.cos(2*math.pi*(u*1+ph*2)); an=ang0+0.35*math.sin(2*math.pi*(u+ph))
        varilla(back if i<3 else front,x,y,Lr,w,an,(30,126,150) if i<3 else (92,200,222),(140,222,238) if i<3 else (222,252,255))
    back=back.filter(ImageFilter.GaussianBlur(2.2*SS))
    coc=lay()
    for i in range(3):
        bx,by=rng.uniform(70,200),rng.uniform(70,200)
        for k in range(7):
            a=rng.uniform(0,6.28); rd=rng.uniform(0,16); x=bx+math.cos(a)*rd+6*math.sin(2*math.pi*(u+i*0.3)); y=by+math.sin(a)*rd+5*math.cos(2*math.pi*(u+i*0.3)); r=9+rng.random()*2
            circ(ImageDraw.Draw(coc),x,y,r,(118,226,150,255)); circ(ImageDraw.Draw(coc),x-r*0.3,y-r*0.32,r*0.36,(226,255,232,255))
    scene=over(over(inner,back),over(front,coc))
    sa=np.array(scene); sa[...,3]=(sa[...,3].astype(np.float32)*np.array(lens)/255).astype(np.uint8)
    vg=np.clip(1-0.55*np.clip((rr-0.55)/0.45,0,1)**1.5,0,1); sa[...,:3]=(sa[...,:3].astype(np.float32)*vg[...,None]).astype(np.uint8)
    scene=Image.fromarray(sa,'RGBA'); out.append(scene)
    ring=lay(); rd=ImageDraw.Draw(ring)
    rd.ellipse([(cx-R-6)*SS,(cy-R-6)*SS,(cx+R+6)*SS,(cy+R+6)*SS],outline=(206,214,228,255),width=int(7*SS)); rd.ellipse([(cx-R+1)*SS,(cy-R+1)*SS,(cx+R-1)*SS,(cy+R-1)*SS],outline=(60,68,86,255),width=int(3*SS))
    rd.arc([(cx-R-4)*SS,(cy-R-4)*SS,(cx+R+4)*SS,(cy+R+4)*SS],200,290,fill=(255,255,255,230),width=int(3*SS))
    for ang in range(0,360,90):
        a=math.radians(ang); rd.line(P([(cx+math.cos(a)*(R-14),cy+math.sin(a)*(R-14)),(cx+math.cos(a)*(R-4),cy+math.sin(a)*(R-4))]),fill=(255,255,255,200),width=int(2*SS))
    gl=lay(); gd=ImageDraw.Draw(gl); gd.pieslice([(cx-R*0.9)*SS,(cy-R*0.9)*SS,(cx+R*0.9)*SS,(cy+R*0.9)*SS],205,260,fill=(255,255,255,46))
    out+=[glow(ring,4,0.4),ring,gl.filter(ImageFilter.GaussianBlur(5*SS))]
    return final([l for l in out])

ANIMS={'spray':(spray,2.8),'jabon':(jabon,2.4),'gota':(gota,2.4),'sal':(sal,3.0),'sinolor':(sinolor,2.4),
 'cuerpo_axilas':(lambda u,L=2.0:cuerpo('axilas',u,L),2.0),'cuerpo_ingle':(lambda u,L=2.0:cuerpo('ingle',u,L),2.0),'cuerpo_pies':(lambda u,L=2.0:cuerpo('pies',u,L),2.0),
 'glandula':(glandula,2.6),'igual':(igual,2.6),'gente':(gente,2.4),'adn':(adn,3.0),'toalla':(toalla,2.4),'micro':(micro,4.0)}

def _job(args):
    nm,i,F=args; fn,L=ANIMS[nm]; return nm,i,fn(i/F,L)
def render_all():
    from multiprocessing import Pool
    jobs=[]
    for nm,(fn,L) in ANIMS.items():
        F=int(round(L*30)); jobs+=[(nm,i,F) for i in range(F)]
    acc={}
    with Pool(4) as p:
        for nm,i,fr in p.imap_unordered(_job,jobs,chunksize=4): acc.setdefault(nm,{})[i]=fr
    for nm,d in acc.items():
        arr=np.stack([d[i] for i in range(len(d))]); np.save(f'assets/anim_{nm}.npy',arr); print(nm,arr.shape,flush=True)
if __name__=='__main__' and len(__import__('sys').argv)>1 and __import__('sys').argv[1]=='all':
    render_all(); raise SystemExit
if __name__=='__main__':
    names=list(ANIMS); us=[0.15,0.45,0.75]
    rows=[]
    for nm in names:
        fn,L=ANIMS[nm]; rows.append(np.hstack([fn(u,L) for u in us]))
    cols=[np.vstack(rows[i:i+5]) for i in range(0,len(rows),5)]
    h=max(c.shape[0] for c in cols); cols=[np.vstack([c,np.zeros((h-c.shape[0],c.shape[1],4),np.uint8)]) for c in cols]
    sheet=np.hstack(cols); bg=np.full(sheet.shape[:2]+(3,),(76,54,98),np.uint8); a=sheet[...,3:4]/255.0
    rgb=(sheet[...,:3]*a+bg*(1-a)).astype(np.uint8); cv2.imwrite('assets/_anim2.png',cv2.cvtColor(rgb,cv2.COLOR_RGB2BGR)); print('ok',sheet.shape)
