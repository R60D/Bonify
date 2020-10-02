bl_info = {
    "name": "R60D'S TOOLS",
    "author": "R60D",
    "version": (3, 0),
    "blender": (2, 90, 1),
    "location": "View3D > Object",
    "description": "A lot of tools used for getting blender physics simulations into source",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}

import bpy
import object_print3d_utils
from bpy.types import (
    AddonPreferences,
    Operator,
    Panel,
    PropertyGroup,
)
from bpy.props import (IntProperty)

class OBJECT_OT_Bonify(Operator):
    bl_label = "Bonify"
    bl_idname = "object.bonify"
    bl_description = "Adds a bone for each selected object"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.object.select_get() and context.object.type == 'MESH'
    
    def execute(self, context):
        x = 0
        t = "Physics_"
        N = "Newton"
        col = "RIGIDBODY"
        
        #REMOVES PRE-EXISTING ARMATURES AND ANIMATIONS
        for reanim in  bpy.data.actions:
            bpy.data.actions.remove(reanim)
            
        for rearm in  bpy.data.armatures:
            bpy.data.armatures.remove(rearm)
        
        
        
        #DESELECTS NON MESH
        for initialsel in bpy.context.selected_objects:
            if initialsel.type != 'MESH':
                initialsel.select_set(False) 
                

        
        
        
        #SELECTED OBJECTS GET ASSIGNED
        for tv in bpy.context.selected_objects:
            tv.name = t+str(x+1)
            tv.data.name = t+str(x+1)
            bpy.context.view_layer.objects.active = tv
            if len(bpy.context.active_object.vertex_groups) >=1:
                bpy.ops.object.vertex_group_remove(all=True)
                
            #CREATES NEWTON ARMATURE
            if ('Newton' in bpy.data.objects) == False:
                bpy.ops.object.armature_add()
                bpy.ops.object.editmode_toggle()
                bpy.ops.armature.select_all()
                bpy.ops.armature.select_all()
                bpy.ops.armature.delete()
                bpy.context.object.name = N
                bpy.context.object.data.name = "Physics_Base"
                bpy.ops.armature.delete()
                bpy.ops.object.editmode_toggle()
            tv.select_set(True)
            x += 1
            bpy.context.view_layer.objects.active = tv
            if len(tv.vertex_groups) < 1:
                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.object.vertex_group_assign_new()
                tv.vertex_groups[0].name = str(x)
                bpy.ops.object.editmode_toggle()
            bpy.data.objects[N].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects[N]
            bpy.ops.object.editmode_toggle()
            bpy.ops.armature.bone_primitive_add(name=str(x))
            bpy.ops.object.editmode_toggle()
        bpy.data.objects[N].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[N]
        bpy.ops.object.posemode_toggle()
        bpy.ops.pose.select_all(action='SELECT')
        for thinger in bpy.context.selected_pose_bones:
            thinger.constraints.new(type='CHILD_OF')
        for ding in bpy.data.objects[N].pose.bones:
            ding.constraints['Child Of'].target = bpy.data.objects['Physics_'+ding.name]
        bpy.ops.object.posemode_toggle()
        bpy.ops.object.move_to_collection(collection_index=0, is_new=True, new_collection_name=col)
        self.report({'INFO'}, "Successful Bonify")
        return{'FINISHED'}

class OBJECT_OT_Bonify_Splitter(Operator):
    bl_label = "Split 127"
    bl_idname = "object.bonify_splitter"
    bl_description = "Splits the Physics Armature into 127 bone pieces"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        N = "Newton"
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[N].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[N]
        while len(bpy.data.armatures['Physics_Base'].bones) >=  128:
            x = 0
            
            for abc in bpy.data.armatures['Physics_Base'].bones:
                abc.select=False
            for thing in bpy.data.armatures['Physics_Base'].bones:  
                if x == 127:
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.armature.separate()
                    bpy.ops.object.editmode_toggle()
                    break
                else:
                    x += 1
                    thing.select=True
        self.report({'INFO'}, "Successful Split")
        return{'FINISHED'}

class OBJECT_OT_Mesh_Splitter(Operator):
    bl_label = "Split Mesh"
    bl_idname = "object.mesh_splitter"
    bl_description = "Splits the Mesh for each NEWTON armature"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Limitation. Anything above Newton.009 is ignored. but 1270 bones is enough I believe.
        
        # Remove World
        bpy.ops.rigidbody.world_remove()

        
        x = -1
        for arm in bpy.data.objects:
            if "Newton" in arm.name:
                x += 1
        while x >= 1:
            bpy.ops.object.select_all(action='DESELECT')
            for bone in bpy.data.objects["Newton.00"+str(x)].data.bones:
                bpy.data.objects["Physics_"+bone.name].select_set(True)
                bpy.context.view_layer.objects.active = bpy.data.objects["Physics_"+bone.name]
            bpy.ops.object.location_clear(clear_delta=False)
            bpy.ops.object.join()
            bpy.context.object.name = "Newton_Mesh.00"+str(x)
            bpy.ops.object.modifier_add(type='ARMATURE')
            bpy.context.object.modifiers["Armature"].object = bpy.data.objects["Newton.00"+str(x)]
            x -= 1
        bpy.ops.object.select_all(action='DESELECT')
        for bone in bpy.data.objects["Newton"].data.bones:
                bpy.data.objects["Physics_"+bone.name].select_set(True)
                bpy.context.view_layer.objects.active = bpy.data.objects["Physics_"+bone.name]
        bpy.ops.object.location_clear(clear_delta=False)
        bpy.ops.object.join()
        bpy.context.object.name = "Newton_Mesh"
        bpy.ops.object.modifier_add(type='ARMATURE')
        bpy.context.object.modifiers["Armature"].object = bpy.data.objects["Newton"]
        nbm = 0
        bpy.ops.object.select_all(action='DESELECT')
        for objct in bpy.data.objects:
            if "Newton" in objct.name and objct.type == 'ARMATURE':
                objct.select_set(True)
                if nbm > 0:
                    bpy.data.objects["Newton_Mesh.00"+str(nbm)].select_set(True)
                else:
                    bpy.data.objects["Newton_Mesh"].select_set(True)
                bpy.ops.object.move_to_collection(collection_index=0, is_new=True, new_collection_name=str(nbm))
                bpy.ops.object.select_all(action='DESELECT')
                nbm += 1
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.rotation_clear(clear_delta=True)
        bpy.ops.object.location_clear(clear_delta=True)
        bpy.ops.object.scale_clear(clear_delta=True)
        self.report({'INFO'}, "Successful MeshSplit")
        return{'FINISHED'}

class OBJECT_OT_Clothify(Operator):
    bl_label = "Clothify"
    bl_idname = "mesh.clothify"
    bl_description = "Clotifies any Rectangle[Has to be flat]"
    bl_space_type = ("VIEW_3D")
    bl_region_type = 'Mesh'
    bl_options = {'REGISTER', 'UNDO'}
    bl_context = 'mesh_edit'
    
    def execute(self, context):
        # removes any cloth modifires
        bpy.ops.object.modifier_remove(modifier="Cloth")
    
        # sets rectangle origin to middle
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN') 
        bpy.ops.object.modifier_add(type='CLOTH')
        bpy.context.object.modifiers["Cloth"].show_render = False
        bpy.context.object.modifiers["Cloth"].show_viewport = False

        
        # Clears all Vertex groups
        if len(bpy.context.active_object.vertex_groups) != 0:
            bpy.ops.object.vertex_group_remove(all=True)

        # Cloth data
        loc = bpy.context.active_object.location
        dim = bpy.context.active_object.dimensions
        nex = bpy.context.active_object
        corner = loc-dim/2

        # moves 3d cursor to selected object origin + moves to edge of object
        xo = corner[0]
        yo = corner[1]
        zo = corner[2]
        xd = dim[0]
        yd = dim[1]
        zd = dim[2]
        x = 1

        bpy.ops.object.armature_add(enter_editmode=True,location=corner)
        bpy.context.active_object.name = "Galileo"
        bpy.ops.object.editmode_toggle()
        bpy.context.active_object.data.bones['Bone'].name ="1"
        h = 0
        # val is the density of the bone grid. 0.1 results in 11x11 bone grid which is 121 bones, just below the limit of 128
        val = 0.1
        tx = val
        while h <= 1:
            
                  
            t = val
            while t <= 1: 
                bpy.context.scene.cursor.location=(xo+xd*t,yo+yd*h,zo)
                x += 1
                bpy.ops.object.editmode_toggle()
                bpy.ops.armature.bone_primitive_add(name=str(x))
                bpy.ops.object.editmode_toggle()
                
                t += val
                
            while tx <= 1:
                bpy.context.scene.cursor.location=(xo,yo+yd*tx,zo)
                x += 1
                bpy.ops.object.editmode_toggle()
                bpy.ops.armature.bone_primitive_add(name=str(x))
                bpy.ops.object.editmode_toggle()
                tx += val
                
            h += val
            
            
        # AUTO-WEIGHT PAINT
        bpy.ops.object.select_all(action='DESELECT')
        nex.select_set(True)
        bpy.data.objects['Galileo'].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects['Galileo']
        bpy.ops.object.parent_set(type='ARMATURE_AUTO')
        
        # CONSTRAINTS
        bpy.ops.object.posemode_toggle()
        bpy.ops.pose.select_all(action='SELECT')

        for thinger in bpy.context.selected_pose_bones:
            thinger.constraints.new(type='COPY_LOCATION')
            thinger.constraints['Copy Location'].target = nex
            thinger.constraints['Copy Location'].subtarget = thinger.name
            thinger.constraints.new(type='SHRINKWRAP')
            thinger.constraints['Shrinkwrap'].target = nex
            thinger.constraints['Shrinkwrap'].use_track_normal = True
            thinger.constraints['Shrinkwrap'].shrinkwrap_type = 'TARGET_PROJECT'
            thinger.constraints['Shrinkwrap'].track_axis = 'TRACK_Y'
        bpy.ops.object.posemode_toggle()
        
        #smooth weights and remove armature
        bpy.context.view_layer.objects.active = nex
        bpy.ops.paint.weight_paint_toggle()
        bpy.ops.object.vertex_group_smooth(group_select_mode='ALL',repeat=30)
        bpy.ops.paint.weight_paint_toggle()
        bpy.ops.object.modifier_remove(modifier="Armature")

        self.report({'INFO'}, "Successful Clothify")
        return{'FINISHED'}
    
class OBJECT_OT_Clothify_pin(Operator):
    bl_label = "Pin"
    bl_idname = "mesh.clothify_pin"
    bl_description = "Pins a vertex"
    bl_space_type = ("VIEW_3D")
    bl_region_type = 'UI'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if bpy.context.mode == 'EDIT_MESH':
                bpy.ops.object.vertex_group_assign_new()
                bpy.context.active_object.vertex_groups.active.name = "pin"
                bpy.ops.object.editmode_toggle()
                bpy.context.active_object.modifiers["Cloth"].settings.vertex_group_mass = "pin"
        self.report({'INFO'}, "Successful pin")
        return{'FINISHED'}
    
class OBJECT_OT_Bone_Unlock(Operator):
    bl_label = "Bone Toggle"
    bl_idname = "pose.bone_unlock"
    bl_description = "Toggles Influence of bone location"
    bl_space_type = ("VIEW_3D")
    bl_region_type = 'UI'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if bpy.context.active_pose_bone.constraints['Copy Location'].influence < 1.0:
            for bone in bpy.context.selected_pose_bones_from_active_object:
                bone.constraints['Copy Location'].influence = 1
        else:
            for bone in bpy.context.selected_pose_bones_from_active_object:
             bone.constraints['Copy Location'].influence = 0
        return{'FINISHED'}
class OBJECT_OT_Bone_CRemover(Operator):
    bl_label = "Bone Pure Remove"
    bl_idname = "pose.bone_pureremove"
    bl_description = "removes the bone with the vertex groups"
    bl_space_type = ("VIEW_3D")
    bl_region_type = 'UI'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        #Return state
        ed = False

        if bpy.context.mode == 'EDIT_ARMATURE':
            bpy.ops.object.posemode_toggle()
            ed = True
            
        for posbone in bpy.context.selected_pose_bones:
            nt = posbone.name

            # gets and active vertex group for a bone
            tx = bpy.context.selected_objects[0].vertex_groups[nt].index
            bpy.context.selected_objects[0].vertex_groups.active_index = tx
            # removes selected vertex group
            bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
            bpy.ops.object.vertex_group_remove()
            bpy.context.view_layer.objects.active = bpy.context.selected_objects[1]

        # Removes selected bones 
        bpy.ops.object.editmode_toggle()
        bpy.ops.armature.delete()
        if ed != True:
            bpy.ops.object.posemode_toggle()
        return{'FINISHED'}
class OBJECT_OT_MassClamp(Operator):
    bl_label = "MassClamp"
    bl_idname = "object.massclamp"
    bl_description = "Clamps the minimum weight"
    bl_space_type = ("VIEW_3D")
    bl_region_type = 'UI'
    bl_options = {'REGISTER', 'UNDO'}
    
    #Properites
    MassClampParameters: bpy.props.IntProperty(
        name = "Minimum Weight",
        default = 10,
        min = 1,
        max = 1000,
        description = "Clamps weight to specified number",
    )
    
    def execute(self, context):
        Mini = 0

        for object in bpy.data.objects:
            if object.type == "MESH" and object.rigid_body.mass < self.MassClampParameters:
                object.rigid_body.mass = self.MassClampParameters
                Mini += 1
        self.report({'INFO'}, "Success! Affected "+str(Mini)+" objects")
        return{'FINISHED'}
class OBJECT_OT_NormalFix(Operator):
    bl_label = "NormalFix"
    bl_idname = "object.normalfix"
    bl_description = "Fixes VMF2OBJ normals"
    bl_space_type = ("VIEW_3D")
    bl_region_type = 'UI'
    bl_options = {'REGISTER', 'UNDO'}
     
    def execute(self, context):

        selection = bpy.context.selected_objects

        for o in selection:
            try:
                bpy.context.view_layer.objects.active = o
                bpy.ops.mesh.customdata_custom_splitnormals_clear()
            except:
                self.report("Object has no custom split normals: " + o.name + ", skipping")
        return{'FINISHED'}
    
def menu_func(self, context):
    self.layout.operator(OBJECT_OT_Bonify.bl_idname)
    self.layout.operator(OBJECT_OT_Bonify_Splitter.bl_idname)
    self.layout.operator(OBJECT_OT_Mesh_Splitter.bl_idname)
    self.layout.operator(OBJECT_OT_Clothify.bl_idname)
    self.layout.operator(OBJECT_OT_MassClamp.bl_idname)
    self.layout.operator(OBJECT_OT_NormalFix.bl_idname)
        
def menu_func_mesh(self, context):
    self.layout.operator(OBJECT_OT_Clothify_pin.bl_idname)
    
def menu_func_pose(self, context):
    self.layout.operator(OBJECT_OT_Bone_Unlock.bl_idname)
    self.layout.operator(OBJECT_OT_Bone_CRemover.bl_idname)

def menu_func_arm_edit(self, context):
    self.layout.operator(OBJECT_OT_Bone_CRemover.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_OT_Bonify)
    bpy.utils.register_class(OBJECT_OT_Bonify_Splitter)
    bpy.utils.register_class(OBJECT_OT_Mesh_Splitter)
    bpy.utils.register_class(OBJECT_OT_Clothify)
    bpy.utils.register_class(OBJECT_OT_Clothify_pin)
    bpy.utils.register_class(OBJECT_OT_Bone_Unlock)
    bpy.utils.register_class(OBJECT_OT_Bone_CRemover)
    bpy.utils.register_class(OBJECT_OT_MassClamp)
    bpy.utils.register_class(OBJECT_OT_NormalFix)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    bpy.types.VIEW3D_MT_edit_mesh.append(menu_func_mesh)
    bpy.types.VIEW3D_MT_pose.append(menu_func_pose)
    bpy.types.VIEW3D_MT_edit_armature.append(menu_func_arm_edit)
    
def unregister():
    bpy.utils.unregister_class(OBJECT_OT_Bonify)
    bpy.utils.unregister_class(OBJECT_OT_Bonify_Splitter)
    bpy.utils.unregister_class(OBJECT_OT_Mesh_Splitter)
    bpy.utils.unregister_class(OBJECT_OT_Clothify)
    bpy.utils.unregister_class(OBJECT_OT_Clothify_pin)
    bpy.utils.unregister_class(OBJECT_OT_Bone_Unlock)
    bpy.utils.unregister_class(OBJECT_OT_Bone_CRemover)
    bpy.utils.unregister_class(OBJECT_OT_MassClamp)
    bpy.utils.unregister_class(OBJECT_OT_NormalFix)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    bpy.types.VIEW3D_MT_edit_mesh.remove(menu_func_mesh)
    bpy.types.VIEW3D_MT_pose.remove(menu_func_pose)
    bpy.types.VIEW3D_MT_edit_armature.remove(menu_func_arm_edit)
    

if __name__ == "__main__":
    register() 