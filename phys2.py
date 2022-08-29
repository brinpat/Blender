import bpy
from math import sin
from random import randint

# nucleus
n = 3

for i in range(n):
    
    if i > round(n/2):
        r = 0.05*randint( 100,1000 )/1000
    else:
        r = 0.05*randint( 100,1000 )/1000
    
    position = [ randint( -10,10 )/100 for axis in 'xyz' ]
    
    bpy.ops.object.effector_add(type = 'FORCE', location = position)
    bpy.context.object.field.strength = -5000
    bpy.context.object.hide_viewport = True
    
    bpy.ops.mesh.primitive_uv_sphere_add(location = position, radius=r)
    bpy.ops.rigidbody.object_add()
    
    
    
bpy.ops.object.select_all(action='DESELECT')

objects = bpy.data.objects
a = objects['Sphere']
b = objects['Force']
b.parent = a



for i in range(n-1):
    
    bpy.ops.object.select_all(action='DESELECT')
    objects = bpy.data.objects
    a = objects['Sphere.00'+str(i+1)]
    b = objects['Force.00'+str(i+1)]
    b.parent = a
    
    
# electrons
n = 8


for i in range(n):
    
    if i > round(n/2):
        r = 0.02*randint( 100,1000 )/1000
    else:
        r = 0.02*randint( 100,1000 )/1000
    
    position = [ randint( -100,100 )/100 for axis in 'xyz' ]
    
    bpy.ops.object.effector_add(type = 'FORCE', location = position)
    bpy.context.object.field.strength = -10
    #bpy.context.object.hide_viewport = True
    
    bpy.ops.mesh.primitive_uv_sphere_add(location = position, radius=r)
    bpy.ops.rigidbody.object_add()
    
    
    
bpy.ops.object.select_all(action='DESELECT')

objects = bpy.data.objects
a = objects['Sphere']
b = objects['Force']
b.parent = a



for i in range(n-1):
    
    bpy.ops.object.select_all(action='DESELECT')
    objects = bpy.data.objects
    a = objects['Sphere.00'+str(i+1)]
    b = objects['Force.00'+str(i+1)]
    b.parent = a