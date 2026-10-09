import numpy as np, soundfile as sf, subprocess, json
SR=48000
v,_=sf.read('stem_voz.wav'); m,_=sf.read('stem_musica.wav'); f,_=sf.read('stem_sfx.wav')
mix=v*0.90+m*1.0+f*1.0
sf.write('mezcla_pre.wav',mix.astype(np.float32),SR,subtype='FLOAT')
def medir(p,extra=''):
    r=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',p,'-af',extra+'loudnorm=I=-14:TP=-1.0:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True).stderr
    j=r[r.rindex('{'):r.rindex('}')+1]; return json.loads(j)
d=medir('mezcla_pre.wav')
print({k:d[k] for k in('input_i','input_tp','input_lra','input_thresh')})
af=(f"loudnorm=I=-14:TP=-1.0:LRA=11:measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}:linear=true,alimiter=limit=0.89:attack=3:release=50:level=disabled")
subprocess.run(['ffmpeg','-y','-v','error','-i','mezcla_pre.wav','-af',af,'-ar','48000','-c:a','pcm_s16le','mezcla_master.wav'],check=True)
r=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i','mezcla_master.wav','-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
print(r[r.rindex('Integrated loudness'):])
