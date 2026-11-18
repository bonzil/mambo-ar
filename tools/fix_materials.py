# Step 1 after Blender export: sane alpha modes, drop the 'Transparent' overlay sheet, idle mouth = atlas cell 1.
import json,struct,sys
path=sys.argv[1]
b=open(path,'rb').read();n=struct.unpack('<I',b[12:16])[0];j=json.loads(b[20:20+n]);rest=b[20+n:]
mode={'Body':('OPAQUE',),'Tail':('OPAQUE',),'Face':('OPAQUE',),'Hair':('MASK',0.5),'Eyes':('MASK',0.5),'Mouth':('MASK',0.5),'Brows_L':('MASK',0.5),'Brows_R':('MASK',0.5),'Cheek':('BLEND',)}
for m in j['materials']:
    t=mode.get(m['name'])
    if not t: continue
    m['alphaMode']=t[0]; m.pop('alphaCutoff',None)
    if t[0]=='MASK': m['alphaCutoff']=t[1]
    if m['name']=='Mouth':
        m['pbrMetallicRoughness']['baseColorTexture']['extensions']={'KHR_texture_transform':{'offset':[0.25,0]}}
    m['doubleSided']=m['name'] in('Hair','Tail')
mi=[i for i,m in enumerate(j['materials']) if m['name']=='Transparent'][0]
for me in j['meshes']: me['primitives']=[p for p in me['primitives'] if p['material']!=mi]
j.setdefault('extensionsUsed',[])
if 'KHR_texture_transform' not in j['extensionsUsed']: j['extensionsUsed'].append('KHR_texture_transform')
js=json.dumps(j,separators=(',',':')).encode(); js+=b' '*((4-len(js)%4)%4)
open(path,'wb').write(b'glTF'+struct.pack('<II',2,20+len(js)+len(rest))+struct.pack('<I',len(js))+b'JSON'+js+rest)
print('materials ok')
