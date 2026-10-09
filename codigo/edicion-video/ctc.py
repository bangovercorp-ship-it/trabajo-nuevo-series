import sys, json, numpy as np, soundfile as sf, sherpa_onnx
SC=sys.argv[1]; m='/tmp/claude-0/asr/sherpa-onnx-nemo-fast-conformer-ctc-es-1424-int8/'
rec=sherpa_onnx.OfflineRecognizer.from_nemo_ctc(model=m+'model.int8.onnx',tokens=m+'tokens.txt',num_threads=4)
x,sr=sf.read(SC+'/in/voz16.wav',dtype='float32')
if x.ndim>1: x=x.mean(1)
tr=np.load(SC+'/tramos.npy'); out=[]
for i,(a,b) in enumerate(tr):
    a0=max(0,a-0.2); s=rec.create_stream(); s.accept_waveform(sr,x[int(a0*sr):int((b+0.3)*sr)]); rec.decode_stream(s); r=s.result
    toks=list(r.tokens); ts=[round(a0+t,3) for t in r.timestamps]
    out.append({'i':i,'a':float(a),'b':float(b),'text':r.text,'tokens':toks,'ts':ts}); print(i,round(a,2),round(b,2),r.text,flush=True)
json.dump(out,open(SC+'/proy/ctc_tramos.json','w'),ensure_ascii=False)
print(out[0]['tokens'],out[0]['ts'])
