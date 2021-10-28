import bpy
from bpy.utils import previews
import os
import math
import sys
sys.modules['monmod'] = bpy.data.texts['vec.py'].as_module()
from monmod import *
sys.modules['easybpy'] = bpy.data.texts['easybpy.py'].as_module()
from easybpy import *

def vec(source_collection, name, vertices, edges, faces, smooth_data, uv_xy, location):
    new_mesh = bpy.data.meshes.new(name)
    new_mesh.from_pydata(vertices, edges, faces)
    new_mesh.update()
    new_object = bpy.data.objects.new(name=name, object_data=new_mesh)
    source_collection.objects.link(new_object)
    new_object.location = location
    new_object.rotation_euler = (0.0, 0.0, 0.0)
    new_object.scale = (1.0, 1.0, 1.0)
    for i, polygon in enumerate(new_object.data.polygons):
        polygon.use_smooth = (True if smooth_data[i] else False)
    new_uv = new_object.data.uv_layers.new(name='MaCarteUV')
    for loop in new_object.data.loops:
        new_uv.data[loop.index].uv = uv_xy[loop.index]
    new_object.data.update()
    return new_object



source_collection = bpy.data.collections.new('MaColl')
bpy.context.scene.collection.children.link(source_collection)
o = bpy.data.objects.new( "empty", None )
source_collection.objects.link(o)
fl = vec(source_collection, 'fl', vertices2, edges2, faces2, smooth_data2, uv_xy2, (0.0, 0.0, 1.0) )
fl.parent = o
nor = vec(source_collection, 'cyl', vertices1, edges1, faces1, smooth_data1, uv_xy1, (0.0, 0.0, 0.0) )
nor.parent = o
fu = vec(source_collection, 'fu', vertices2, edges2, faces2, smooth_data2, uv_xy2, (0.0, 0.0, 1.0) )
fu.parent = fl


fc = fl.constraints.new('TRACK_TO')
fc.track_axis = 'TRACK_NEGATIVE_Z'
fc.target = o
nc = nor.constraints.new('TRACK_TO')
nc.track_axis = 'TRACK_Z'
nc.target = fl
drv = nor.driver_add('scale',2)
var = drv.driver.variables.new()
var.name='MaVar'
var.type='LOC_DIFF'
var.targets[0].id = o
var.targets[1].id = fl
drv.driver.expression = var.name  + '-0.5'


fc = fu.constraints.new('TRACK_TO')
fc.track_axis = 'TRACK_NEGATIVE_Z'
fc.target = o
drv = fu.driver_add('location',2)
var = drv.driver.variables.new()
var.name='MaVar'
var.type='LOC_DIFF'
var.targets[0].id = o
var.targets[1].id = fl
drv.driver.expression = var.name +'*-1.0 +1'
