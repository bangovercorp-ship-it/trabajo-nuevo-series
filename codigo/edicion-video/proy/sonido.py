"""Diseno de sonido: SFX sintetizados + musica con ducking suave + master -14 LUFS."""
import numpy as np, soundfile as sf, json, subprocess
from scipy import signal
from cues import SFX, nuevo, DUR
SR=48000
rng=np.random.default_rng(7)
def T(n): return np.arange(n)/SR
def sos(kind,f,order=4): return signal.butter(order,f,btype=kind,fs=SR,output='sos')
def lp(x,f): return signal.sosfilt(sos('low',f),x)
def hp(x,f): return signal.sosfilt(sos('high',f),x)
def bp(x,lo,hi): return signal.sosfilt(sos('band',[lo,hi]),x)
def noise(n): return rng.standard_normal(n)
def stereo(x,pan=0.0):
    a=np.sqrt((1-pan)/2)*np.sqrt(2); b=np.sqrt((1+pan)/2)*np.sqrt(2)
    return np.stack([x*a,x*b],1)
_IRC={}
def _ir(tail,tau):
    k=(tail,tau)
    if k not in _IRC:
        n=int(tail*SR); t=T(n); ir=[hp(lp(noise(n),7000),180)*np.exp(-t/tau) for _ in range(2)]; _IRC[k]=[i/np.abs(i).max() for i in ir]
    return _IRC[k]
def reverb(x,mix=0.25,tail=0.9,tau=0.28):
    IR=_ir(tail,tau); n=len(IR[0])
    xs=x if x.ndim==2 else np.stack([x,x],1)
    L=len(xs)+n-1; out=np.zeros((L,2))
    for c in range(2): out[:,c]=signal.fftconvolve(xs[:,c],IR[c])*0.03
    dry=np.zeros_like(out); dry[:len(xs)]=xs
    return dry*(1-mix*0.5)+out*mix*8

def boom(vol=1):
    n=int(1.7*SR); t=T(n)
    f=36+(135-36)*np.exp(-t/0.11); ph=2*np.pi*np.cumsum(f)/SR
    sub=np.sin(ph)*np.exp(-t/0.42)*(1-np.exp(-t/0.003))
    body=np.sin(2*np.pi*88*t)*np.exp(-t/0.16)*0.5
    cr=bp(noise(n),140,3200)*np.exp(-t/0.085)*0.35
    click=hp(noise(n),2500)*np.exp(-t/0.004)*0.25
    x=(sub*1.0+body+cr+click)*vol*0.9
    return reverb(stereo(x),mix=0.22)

def thud(vol=1):
    n=int(0.35*SR); t=T(n); f=78-30*(1-np.exp(-t/0.05)); ph=2*np.pi*np.cumsum(f)/SR
    x=np.sin(ph)*np.exp(-t/0.11)+lp(noise(n),420)*np.exp(-t/0.03)*0.4
    return stereo(x*vol*0.95)

def whoosh(dur=0.5,up=True,vol=1):
    n=int(dur*SR); t=T(n)/dur
    bands=[(250,900),(900,2600),(2600,7000)]; out=np.zeros(n)
    cen=[0.25,0.5,0.75] if up else [0.75,0.5,0.25]
    base=noise(n)
    for (lo,hi),c in zip(bands,cen):
        g=np.exp(-((t-c)/0.20)**2); out+=bp(base,lo,hi)*g
    env=np.sin(np.pi*np.clip(t,0,1))**1.6
    x=out*env*vol*0.55
    pan=np.linspace(-0.6,0.6,n) if up else np.linspace(0.6,-0.6,n)
    L=x*np.sqrt((1-pan)/2)*1.41; R=x*np.sqrt((1+pan)/2)*1.41
    return np.stack([L,R],1)

def tension(dur=2.0,vol=1):
    n=int(dur*SR); t=T(n); u=t/dur
    f=190+(1500-190)*u**1.6; ph=2*np.pi*np.cumsum(f)/SR
    tone=(np.sin(ph)+0.6*np.sin(ph*1.007)+0.25*np.sin(ph*2.01))/1.9
    trem_f=6+16*u**1.2; trem=0.65+0.35*np.sin(2*np.pi*np.cumsum(trem_f)/SR)
    nz=hp(noise(n),900)*(0.2+0.8*u)
    amp=(u**2.2)
    x=(tone*trem*0.5+nz*0.45)*amp
    gap=int(0.055*SR); x[-gap:]*=np.linspace(1,0,gap)**2     # hueco de aire antes del impacto
    return stereo(x*vol*0.8)

KEY=[698.46,830.61,932.33,1046.50,1244.51,1396.91,1661.2,1864.7]    # Fa menor pentatonica (F5..Bb6)
def pop(n=0,vol=1):
    f=KEY[n%len(KEY)]; L=int(0.34*SR); t=T(L)
    x=(np.sin(2*np.pi*f*t)+0.38*np.sin(2*np.pi*2*f*t)+0.14*np.sin(2*np.pi*3*f*t))*np.exp(-t/0.075)*(1-np.exp(-t/0.0012))
    x=x+hp(noise(L),3000)*np.exp(-t/0.004)*0.25
    return reverb(stereo(x*vol*0.55,pan=rng.uniform(-0.2,0.2)),mix=0.14,tail=0.5,tau=0.18)

def tick(vol=1):
    L=int(0.05*SR); t=T(L)
    x=bp(noise(L),2500,7000)*np.exp(-t/0.006)*0.7+np.sin(2*np.pi*4200*t)*np.exp(-t/0.008)*0.35
    return stereo(x*vol*0.55)

def bloop(f=520,vol=1):
    L=int(0.22*SR); t=T(L); fr=f+(f*1.9-f)*(1-np.exp(-t/0.05)); ph=2*np.pi*np.cumsum(fr)/SR
    x=np.sin(ph)*np.exp(-t/0.09)*(1-np.exp(-t/0.002))+0.3*np.sin(2*ph)*np.exp(-t/0.05)
    return stereo(x*vol*0.55)

def stab(vol=1):
    L=int(0.9*SR); t=T(L); x=np.zeros(L)
    for f in (87.3,92.5,130.8):
        ph=2*np.pi*f*t; saw=signal.sawtooth(ph)*0.5+np.sin(ph)*0.5; x+=saw
    x=lp(x,900)*np.exp(-t/0.30)*(1-np.exp(-t/0.004))/3
    return reverb(stereo(x*vol*0.8),mix=0.2,tail=0.6,tau=0.2)

def chime(vol=1):
    L=int(2.2*SR); out=np.zeros((L,2))
    for k,(f,dl) in enumerate(((1396.9,0.0),(2093.0,0.13))):
        n=L-int(dl*SR); t=T(n); x=np.zeros(n)
        for pr,am,tau in ((1,1,0.9),(2.76,0.45,0.5),(5.4,0.22,0.3),(8.93,0.1,0.18)):
            x+=am*np.sin(2*np.pi*f*pr*t)*np.exp(-t/tau)
        x*=(1-np.exp(-t/0.002))*0.35
        out[int(dl*SR):]+=stereo(x,pan=-0.15+0.3*k)
    return reverb(out*vol,mix=0.3,tail=1.2,tau=0.5)

FN={'boom':lambda p:boom(p.get('vol',1)),'thud':lambda p:thud(p.get('vol',1)),'whoosh':lambda p:whoosh(p.get('dur',.5),p.get('up',True),p.get('vol',1)),
    'tension':lambda p:tension(p.get('dur',2),p.get('vol',1)),'pop':lambda p:pop(p.get('n',0),p.get('vol',1)),'tick':lambda p:tick(p.get('vol',1)),
    'bloop':lambda p:bloop(p.get('f',520),p.get('vol',1)),'stab':lambda p:stab(p.get('vol',1)),'chime':lambda p:chime(p.get('vol',1))}

if __name__=='__main__':
    N=int(round(DUR*SR)); sfx=np.zeros((N+3*SR,2))
    # cuadricula de la musica: cada impacto grande se pega al golpe mas cercano si esta a < 70 ms
    r=json.load(open('../in/ritmo.json')); gol=np.array(r['golpes'])
    cfg=json.load(open('musica_cfg.json')); off=cfg['offset']
    grid=gol-off
    ev=[]
    for t,k,p in SFX:
        tn=nuevo(t)
        if k in ('boom','thud'):
            d=grid-tn; j=np.argmin(np.abs(d))
            if abs(d[j])<0.07: tn=grid[j]
        ev.append((tn,k,p))
    json.dump([(round(a,4),k) for a,k,p in ev],open('sfx_times.json','w'))
    NORM={'boom':-4.0,'thud':-5.0,'whoosh':-13.0,'tension':-14.0,'pop':-15.0,'tick':-19.0,'bloop':-14.0,'stab':-12.0,'chime':-17.0}
    for tn,k,p in ev:
        s=FN[k]({**p,'vol':1.0}); s=s/(np.abs(s).max()+1e-9)*10**(NORM[k]/20)*p.get('vol',1.0); i=int(round(tn*SR))
        if k=='tension': i=int(round(tn*SR))     # empieza en tn y termina en tn+dur
        if i<0: continue
        sfx[i:i+len(s)]+=s[:len(sfx)-i]
    sfx=sfx[:N]
    # --- voz ---
    voz,_=sf.read('voz_limpia.wav'); voz=voz[:N]; voz=np.stack([voz,voz],1) if voz.ndim==1 else voz
    if len(voz)<N: voz=np.vstack([voz,np.zeros((N-len(voz),2))])
    # --- musica ---
    mus,_=sf.read('musica48.wav'); o=int(off*SR); mus=mus[o:o+N]
    if len(mus)<N: mus=np.vstack([mus,np.zeros((N-len(mus),2))])
    mus=hp(mus[:,0],35)[:,None]*np.ones((1,2))*0+np.stack([hp(mus[:,0],35),hp(mus[:,1],35)],1)
    # hueco de voz pa la voz: -2.5 dB en 2 kHz
    sosv=signal.iirpeak(2000/(SR/2),1.1); 
    # envolvente de ducking a partir de la voz
    hop=int(SR*0.010); nfr=N//hop; vm=voz.mean(1)
    rms=np.sqrt((vm[:nfr*hop].reshape(nfr,hop)**2).mean(1)+1e-12); db=np.convolve(20*np.log10(rms),np.ones(5)/5,'same')
    real=db[db>-90]; fl,pk=np.percentile(real,10),np.percentile(real,95); hi=fl+(pk-fl)*.35; lo=fl+(pk-fl)*.18
    sp=np.zeros(nfr,bool); on=False
    for k in range(nfr):
        on=True if (not on and db[k]>hi) else (False if (on and db[k]<lo) else on); sp[k]=on
    BASE,DUCK=-2.0,-9.0; PRE,HOLD=0.10,0.22; RD,RU=45.0,16.0
    tgt=np.full(nfr,BASE,float)
    for k in np.where(sp)[0]: tgt[max(0,k-int(PRE*100)):k+int(HOLD*100)]=BASE+DUCK
    # silencio como efecto alrededor de "Punto."
    thud=[nuevo(t) for t,kk,p in SFX if kk=='thud'][0]
    a,b=int((thud-0.14)*100),int((thud+0.34)*100); tgt[a:b]=-26
    g=np.empty(nfr); cur=tgt[0]
    for k,t in enumerate(tgt):
        cur=max(t,cur-RD*0.01) if t<cur else (min(t,cur+RU*0.01) if t>cur else cur); g[k]=cur
    w=15; ker=np.ones(w)/w
    for _ in range(2): g=np.convolve(np.r_[np.full(w,g[0]),g,np.full(w,g[-1])],ker,'same')[w:-w]
    gs=np.interp(np.arange(N),(np.arange(nfr)+.5)*hop,g); gain=10**(gs/20)
    mus=mus*gain[:,None]
    fi,fo=int(0.5*SR),int(2.2*SR)
    mus[:fi]*=(np.sin(np.linspace(0,1,fi)*np.pi/2)**2)[:,None]; mus[-fo:]*=(np.cos(np.linspace(0,1,fo)*np.pi/2)**2)[:,None]
    sf.write('stem_voz.wav',voz.astype(np.float32),SR,subtype='FLOAT')
    sf.write('stem_musica.wav',mus.astype(np.float32),SR,subtype='FLOAT')
    sf.write('stem_sfx.wav',sfx.astype(np.float32),SR,subtype='FLOAT')
    print("stems escritos; pico voz %.2f  musica %.2f  sfx %.2f"%(np.abs(voz).max(),np.abs(mus).max(),np.abs(sfx).max()))
    print("mayor salto de ganancia de musica: %.4f dB/muestra"%np.abs(np.diff(gs)).max())
