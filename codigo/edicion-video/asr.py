import sys, json, numpy as np, soundfile as sf, sherpa_onnx
SC=sys.argv[1]
m='/tmp/claude-0/asr/sherpa-onnx-whisper-small/'
rec=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=m+'small-encoder.int8.onnx',decoder=m+'small-decoder.int8.onnx',tokens=m+'small-tokens.txt',language='es',task='transcribe',num_threads=4)
x,sr=sf.read(SC+'/in/voz16.wav',dtype='float32')
if x.ndim>1: x=x.mean(1)
print(sr,len(x)/sr)
tr=np.load(SC+'/tramos.npy')
out=[]
def run(a,b):
    s=rec.create_stream(); s.accept_waveform(sr,x[int(a*sr):int(b*sr)]); rec.decode_stream(s); return s.result.text.strip()
for i,(a,b) in enumerate(tr):
    t=run(max(0,a-0.15),min(len(x)/sr,b+0.25)); out.append([float(a),float(b),t]); print(i,round(a,2),round(b,2),t,flush=True)
full=run(0,30); print('FULL0-30:',full)
full2=run(30,len(x)/sr); print('FULL30-end:',full2)
json.dump(out,open(SC+'/proy/asr_tramos.json','w'),ensure_ascii=False,indent=1)
