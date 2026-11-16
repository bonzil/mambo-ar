# Replace KHR_materials_unlit on face parts with an "emissive-only" standard material:
# black base color + texture in emissive => looks unlit, and survives the iPhone USDZ export.
import json,struct,sys
path=sys.argv[1]
b=open(path,'rb').read();n=struct.unpack('<I',b[12:16])[0];j=json.loads(b[20:20+n]);rest=b[20+n:]
for m in j['materials']:
    ext=m.get('extensions',{})
    if 'KHR_materials_unlit' not in ext: continue
    del ext['KHR_materials_unlit']
    if not ext: m.pop('extensions')
    pbr=m['pbrMetallicRoughness']; tex=dict(pbr['baseColorTexture'])
    m['emissiveTexture']=tex; m['emissiveFactor']=[1,1,1]
    pbr['metallicFactor']=0; pbr['roughnessFactor']=1; pbr['baseColorFactor']=[0,0,0,1]
    if m.get('alphaMode','OPAQUE') in ('OPAQUE',) or m['name'] in ('Eyes','Mouth'):
        m['alphaMode']='OPAQUE'; m.pop('alphaCutoff',None); pbr.pop('baseColorTexture')   # textures fully opaque
    else:
        pbr['baseColorTexture']={'index':tex['index']}   # kept only for alpha (color x 0)
j['extensionsUsed']=[e for e in j['extensionsUsed'] if e!='KHR_materials_unlit']
js=json.dumps(j,separators=(',',':')).encode();js+=b' '*((4-len(js)%4)%4)
open(path,'wb').write(b'glTF'+struct.pack('<II',2,20+len(js)+len(rest))+struct.pack('<I',len(js))+b'JSON'+js+rest)
print([(m['name'],m.get('alphaMode'),'emis' if 'emissiveTexture' in m else '') for m in j['materials']])
