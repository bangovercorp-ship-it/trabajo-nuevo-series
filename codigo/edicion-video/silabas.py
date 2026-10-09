import numpy as np, librosa, scipy.signal as sg
y, sr = librosa.load('in/voz16.wav', sr=16000, mono=True)
# banda de voz y envolvente
b,a = sg.butter(4,[250,3500],btype='band',fs=sr); yb = sg.filtfilt(b,a,y)
hop=160  # 10 ms
env = np.sqrt(np.convolve(yb**2, np.ones(hop*2)/(hop*2), 'same'))[::hop]
env = np.clip(sg.savgol_filter(env, 9, 2),1e-6,None)
db = 20*np.log10(env+1e-6)
thr = np.percentile(db, 30)
# segmentos de habla (hueco >= 0.30 s corta)
act = db > (db.max()-38)
segs=[];i=0;n=len(act)
while i<n:
    if act[i]:
        j=i
        while j<n and act[j]: j+=1
        segs.append([i,j]); i=j
    else: i+=1
m=[]
for s in segs:
    if m and (s[0]-m[-1][1])<30: m[-1][1]=s[1]
    else: m.append(s)
m=[s for s in m if (s[1]-s[0])>=12]
# nucleos silabicos: picos de la envolvente suavizada
sm = np.clip(sg.savgol_filter(env, 15, 2),1e-6,None)
sm_db = 20*np.log10(sm+1e-6)
pk,_ = sg.find_peaks(sm_db, distance=11, prominence=2.2)
print(f"{len(m)} tramos de habla\n")
print(" #   inicio   fin    dur   silabas  sil/s")
for k,(a_,b_) in enumerate(m,1):
    c = int(((pk>=a_)&(pk<b_)).sum()); d=(b_-a_)/100
    print(f"{k:2d}  {a_/100:6.2f} {b_/100:6.2f} {d:5.2f}   {c:4d}    {c/d:4.1f}")
np.save('tramos.npy', np.array(m)/100.0)
np.save('picos.npy', pk/100.0)
