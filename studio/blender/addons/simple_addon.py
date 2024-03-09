bl_info = {
    "name": "simple studio addon",
    "author": "Tovias",
    "version": (1, 0),
    "blender": (3, 3, 0),
    "location": "3DView",
    "description": "test",
    "warning": "",
    "support": "COMMUNITY",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}

import bpy

class OBJECT_OT_simple(bpy.types.Operator):
    bl_idname = "objects.simple"
    bl__label = "SIMPLE"

    @classmethod
    def poll(cls, context):
        return True
    def execute(self, context):
        print("Simple Operator")
        return {'FINISHED'} 

def register():
    bpy.utils.register_class(OBJECT_OT_simple)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_simple)