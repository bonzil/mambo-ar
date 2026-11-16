# Post-process mambo.glb: face parts copy Face normals (no lighting seams) + unlit like the playground.
import json,struct,sys,numpy as np
path=sys.argv[1]
b=open(path,'rb').read();n=struct.unpack('<I',b[12:16])[0];j=json.loads(b[20:20+n]);B=bytearray(b[20+n+8:])
def view(i):
    a=j['accessors'][i];v=j['bufferViews'][a['bufferView']];assert v.get('byteStride',12)==12
    return v.get('byteOffset',0)+a.get('byteOffset',0),a['count']
def get(i):
    o,c=view(i);return np.frombuffer(bytes(B[o:o+c*12]),dtype='<f4').reshape(c,3).copy()
P={j['materials'][p['material']]['name']:p for p in j['meshes'][0]['primitives']}
fp=get(P['Face']['attributes']['POSITION']);fn=get(P['Face']['attributes']['NORMAL'])
for nm in ['Mouth','Eyes','Cheek','Brows_L','Brows_R']:
    p=P[nm];pos=get(p['attributes']['POSITION']);nor=get(p['attributes']['NORMAL'])
    d=((pos[:,None,:]-fp[None,:,:])**2).sum(-1);idx=d.argmin(1)
    new=fn[idx];new/=np.linalg.norm(new,axis=1,keepdims=True)
    print(nm,'mean normal change deg',float(np.degrees(np.arccos(np.clip((new*nor).sum(1),-1,1))).mean().round(1)))
    o,c=view(p['attributes']['NORMAL']);B[o:o+c*12]=new.astype('<f4').tobytes()
j['extensionsUsed']=sorted(set(j.get('extensionsUsed',[]))|{'KHR_materials_unlit'})
for m in j['materials']:
    if m['name'] in ('Face','Eyes','Mouth','Cheek','Brows_L','Brows_R'):
        m.setdefault('extensions',{})['KHR_materials_unlit']={}
js=json.dumps(j,separators=(',',':')).encode();js+=b' '*((4-len(js)%4)%4);bc=bytes(B)
open(path,'wb').write(b'glTF'+struct.pack('<II',2,28+len(js)+len(bc))+struct.pack('<I',len(js))+b'JSON'+js+struct.pack('<I',len(bc))+b'BIN\x00'+bc)
print('ok')
