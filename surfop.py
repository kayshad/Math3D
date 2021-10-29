from __future__ import division
from sympy import *
x, y, z, t = symbols('x y z t')
k, m, n = symbols('k m n', integer=True)
f, g, h = symbols('f g h', cls=Function)
init_printing()



import bpy


verts = []
edges = []
faces  = []

name = 'Grid'

div = 1
rge = int(10*1/div)*2
rgf = rge*2
rgfd = rgf+1
print(rge)

verts.extend([(i*div,j*div,sin(i)) for i in range(-rge,rge+1) for j in range(-rge,rge+1)])
faces.extend([i+(j*rgfd),(i+(j*rgfd)+rgfd),(i+(j*rgfd)+rgfd+1),(i+(j*rgfd)+1)] for i in range(rgf) for j in range(rgf))
mesh = bpy.data.meshes.new(name)
mesh.from_pydata(verts, [], faces)
mesh.update(calc_edges=True)
for f in mesh.polygons:
    f.use_smooth = True
obj = bpy.data.objects.new(name, mesh)
obj.modifiers.new('My SubDiv', 'SUBSURF')
bpy.context.scene.collection.objects.link(obj)
