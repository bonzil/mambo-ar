# Blender: export the rigged Mambo (skin + bones, no animation) to GLB.
import bpy, sys
out = sys.argv[sys.argv.index('--') + 1]
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.export_scene.gltf(filepath=out, export_format='GLB', export_skins=True, export_animations=False,
    export_apply=False, export_image_format='JPEG', export_image_quality=80, export_yup=True, export_def_bones=False)
