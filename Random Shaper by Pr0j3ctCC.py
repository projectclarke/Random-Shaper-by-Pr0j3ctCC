bl_info = {
    "name": "Random Shaper by Pr0j3ctCC",
    "blender": (2, 80, 0),
    "version": (1, 5, 0),
    "category": "Object",
    "description": "Add random shapes with customizable offsets, rotations, and dimensions",
}

import bpy
import random

class OBJECT_OT_add_random_shapes(bpy.types.Operator):
    bl_idname = "object.add_random_shapes"
    bl_label = "Add Random Shapes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        shape = context.scene.shape
        count = context.scene.count
        dimension_x = context.scene.dimension_x
        dimension_y = context.scene.dimension_y
        dimension_z = context.scene.dimension_z
        random_axis = context.scene.random_axis
        offset = context.scene.offset
        random_offset = context.scene.random_offset
        min_offset = context.scene.min_offset
        max_offset = context.scene.max_offset

        random_rotation = context.scene.random_rotation
        rotation_axis = context.scene.rotation_axis
        min_rotation = context.scene.min_rotation
        max_rotation = context.scene.max_rotation

        random_dimensions = context.scene.random_dimensions
        lock_x = context.scene.lock_x
        lock_y = context.scene.lock_y
        lock_z = context.scene.lock_z
        min_dimension = context.scene.min_dimension
        max_dimension = context.scene.max_dimension

        current_offset = 0

        for i in range(count):
            if shape == 'CUBE':
                bpy.ops.mesh.primitive_cube_add()
            elif shape == 'SPHERE':
                bpy.ops.mesh.primitive_uv_sphere_add()
            elif shape == 'CYLINDER':
                bpy.ops.mesh.primitive_cylinder_add()
            elif shape == 'CONE':
                bpy.ops.mesh.primitive_cone_add()

            obj = bpy.context.object
            
            if random_dimensions:
                scale_x = dimension_x if lock_x else random.uniform(min_dimension, max_dimension)
                scale_y = dimension_y if lock_y else random.uniform(min_dimension, max_dimension)
                scale_z = dimension_z if lock_z else random.uniform(min_dimension, max_dimension)
            else:
                scale_x = dimension_x
                scale_y = dimension_y
                scale_z = dimension_z

            obj.scale = (scale_x / 2, scale_y / 2, scale_z / 2)

            if random_axis == 'X':
                obj.location.x += current_offset
                current_offset += random.uniform(min_offset, max_offset) if random_offset else offset
            elif random_axis == 'Y':
                obj.location.y += current_offset
                current_offset += random.uniform(min_offset, max_offset) if random_offset else offset
            elif random_axis == 'Z':
                obj.location.z += current_offset
                current_offset += random.uniform(min_offset, max_offset) if random_offset else offset

            if random_rotation:
                if rotation_axis == 'X':
                    obj.rotation_euler[0] = random.uniform(min_rotation, max_rotation)
                elif rotation_axis == 'Y':
                    obj.rotation_euler[1] = random.uniform(min_rotation, max_rotation)
                elif rotation_axis == 'Z':
                    obj.rotation_euler[2] = random.uniform(min_rotation, max_rotation)

        return {'FINISHED'}

class VIEW3D_PT_add_random_shapes_panel(bpy.types.Panel):
    bl_label = "Random Shaper by Pr0j3ctCC"
    bl_idname = "VIEW3D_PT_add_random_shapes"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Random Shaper'

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        
        col.prop(context.scene, "shape")
        col.prop(context.scene, "count")
        col.prop(context.scene, "dimension_x")
        col.prop(context.scene, "dimension_y")
        col.prop(context.scene, "dimension_z")
        col.prop(context.scene, "random_axis")
        col.prop(context.scene, "offset")
        col.prop(context.scene, "random_offset")
        if context.scene.random_offset:
            col.prop(context.scene, "min_offset")
            col.prop(context.scene, "max_offset")
        col.prop(context.scene, "random_rotation")
        if context.scene.random_rotation:
            col.prop(context.scene, "rotation_axis")
            col.prop(context.scene, "min_rotation")
            col.prop(context.scene, "max_rotation")
        col.prop(context.scene, "random_dimensions")
        if context.scene.random_dimensions:
            col.prop(context.scene, "lock_x")
            col.prop(context.scene, "lock_y")
            col.prop(context.scene, "lock_z")
            col.prop(context.scene, "min_dimension")
            col.prop(context.scene, "max_dimension")
        col.operator("object.add_random_shapes")

def register():
    bpy.utils.register_class(OBJECT_OT_add_random_shapes)
    bpy.utils.register_class(VIEW3D_PT_add_random_shapes_panel)
    
    bpy.types.Scene.shape = bpy.props.EnumProperty(
        name="Shape",
        description="Choose shape to add",
        items=[
            ('CUBE', "Cube", ""),
            ('SPHERE', "Sphere", ""),
            ('CYLINDER', "Cylinder", ""),
            ('CONE', "Cone", "")
        ],
        default='CUBE'
    )
    bpy.types.Scene.count = bpy.props.IntProperty(
        name="Count",
        description="Number of shapes to add",
        default=1,
        min=1,
    )
    bpy.types.Scene.dimension_x = bpy.props.FloatProperty(
        name="Dimension X",
        description="Dimension X",
        default=1.0,
    )
    bpy.types.Scene.dimension_y = bpy.props.FloatProperty(
        name="Dimension Y",
        description="Dimension Y",
        default=1.0,
    )
    bpy.types.Scene.dimension_z = bpy.props.FloatProperty(
        name="Dimension Z",
        description="Dimension Z",
        default=1.0,
    )
    bpy.types.Scene.random_axis = bpy.props.EnumProperty(
        name="Randomize Orientation Axis",
        description="Axis to randomize orientation around",
        items=[
            ('X', "X-Axis", ""),
            ('Y', "Y-Axis", ""),
            ('Z', "Z-Axis", "")
        ],
        default='X'
    )
    bpy.types.Scene.offset = bpy.props.FloatProperty(
        name="Offset",
        description="Fixed offset between shapes",
        default=1.0,
    )
    bpy.types.Scene.random_offset = bpy.props.BoolProperty(
        name="Random Offset",
        description="Randomize the offset between shapes",
        default=False,
    )
    bpy.types.Scene.min_offset = bpy.props.FloatProperty(
        name="Minimum Offset",
        description="Minimum random offset between shapes",
        default=1.0,
    )
    bpy.types.Scene.max_offset = bpy.props.FloatProperty(
        name="Maximum Offset",
        description="Maximum random offset between shapes",
        default=2.0,
    )
    bpy.types.Scene.random_rotation = bpy.props.BoolProperty(
        name="Random Rotation",
        description="Randomize the rotation of shapes",
        default=False,
    )
    bpy.types.Scene.rotation_axis = bpy.props.EnumProperty(
        name="Rotation Axis",
        description="Axis to randomize rotation around",
        items=[
            ('X', "X-Axis", ""),
            ('Y', "Y-Axis", ""),
            ('Z', "Z-Axis", "")
        ],
        default='X'
    )
    bpy.types.Scene.min_rotation = bpy.props.FloatProperty(
        name="Minimum Rotation",
        description="Minimum random rotation",
        default=0.0,
        subtype='ANGLE',
        unit='ROTATION'
    )
    bpy.types.Scene.max_rotation = bpy.props.FloatProperty(
        name="Maximum Rotation",
        description="Maximum random rotation",
        default=6.28,
        subtype='ANGLE',
        unit='ROTATION'
    )
    bpy.types.Scene.random_dimensions = bpy.props.BoolProperty(
        name="Random Dimensions",
        description="Randomize the dimensions of shapes",
        default=False,
    )
    bpy.types.Scene.lock_x = bpy.props.BoolProperty(
        name="Lock X Dimension",
        description="Lock the X dimension",
        default=False,
    )
    bpy.types.Scene.lock_y = bpy.props.BoolProperty(
        name="Lock Y Dimension",
        description="Lock the Y dimension",
        default=False,
    )
    bpy.types.Scene.lock_z = bpy.props.BoolProperty(
        name="Lock Z Dimension",
        description="Lock the Z dimension",
        default=False,
    )
    bpy.types.Scene.min_dimension = bpy.props.FloatProperty(
        name="Minimum Dimension",
        description="Minimum random dimension",
        default=0.5,
    )
    bpy.types.Scene.max_dimension = bpy.props.FloatProperty(
        name="Maximum Dimension",
        description="Maximum random dimension",
        default=2.0,
    )

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_random_shapes)
    bpy.utils.unregister_class(VIEW3D_PT_add_random_shapes_panel)

    del bpy.types.Scene.shape
    del bpy.types.Scene.count
    del bpy.types.Scene.dimension_x
    del bpy.types.Scene.dimension_y
    del bpy.types.Scene.dimension_z
    del bpy.types.Scene.random_axis
    del bpy.types.Scene.offset
    del bpy.types.Scene.random_offset
    del bpy.types.Scene.min_offset
    del bpy.types.Scene.max_offset
    del bpy.types.Scene.random_rotation
    del bpy.types.Scene.rotation_axis
    del bpy.types.Scene.min_rotation
    del bpy.types.Scene.max_rotation
    del bpy.types.Scene.random_dimensions
    del bpy.types.Scene.lock_x
    del bpy.types.Scene.lock_y
    del bpy.types.Scene.lock_z
    del bpy.types.Scene.min_dimension
    del bpy.types.Scene.max_dimension

if __name__ == "__main__":
    register()
