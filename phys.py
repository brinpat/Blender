import bpy
from math import sin


from random import randint
# Generate 50 cubes in random locations
for i in range(5):
    position = [ randint( -10, 10 ) for axis in 'xyz' ]
    
    bpy.ops.object.effector_add(type = 'FORCE', location = position)
    bpy.context.object.field.strength = -1000
    
    bpy.ops.mesh.primitive_uv_sphere_add(location = position)
    bpy.ops.rigidbody.object_add()
    
        
bpy.ops.object.select_all(action='DESELECT')
 

for o in ("Sphere", "Force"):
    obj = bpy.context.scene.objects.get(o)
    if obj: obj.select_set(True)
    bpy.ops.object.parent_set(type = 'ARMATURE_NAME')