
# Author: Will Alcorn 2017

import bpy

WIDTH = 512
HEIGHT = 512

def set_face_texture(obj, img):
    for face in obj.data.uv_textures.active.data:
        face.image = img

def setup_baked(obj):
    bpy.ops.object.material_slot_remove()
    bpy.ops.object.material_slot_add()
    mat = bpy.data.materials.new('baked')
    obj.material_slots[0].material = mat
    mat.use_shadeless = True
    mat.use_transparency = True
    mat.alpha = 0
    tex = bpy.data.textures.new('baked', type='IMAGE')
    mat.texture_slots.add()
    mat.texture_slots[0].texture = tex
    mat.texture_slots[0].use_map_alpha = True
    img = bpy.data.images.new(name='baked.png', width=WIDTH, height=HEIGHT)
    tex.image = img
    set_face_texture(obj, img)

a = bpy.context.active_object
bpy.ops.object.duplicate()
b = bpy.context.active_object
setup_baked(b)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.dissolve_limited() # note: ngons
bpy.ops.uv.muv_uvw_box_map(size=16)
bpy.ops.uv.packislands_noscale()
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')
a.select = True
b.select = True
render = bpy.context.scene.render
render.use_bake_selected_to_active = True
render.bake_margin = 0
bpy.ops.object.bake_image()

