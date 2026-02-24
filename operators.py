"""
Operators for Pattern & Version Manager.

Operators:
  OBJECT_OT_pv_rename        - Alt+F2 rename with auto-suffix
  OBJECT_OT_pv_copy_normal   - Standard duplicate
  OBJECT_OT_pv_copy_pattern  - Duplicate with incremented Pt number
"""

import bpy
from . import naming


class OBJECT_OT_pv_rename(bpy.types.Operator):
    bl_idname = "object.pv_rename"
    bl_label = "PV Rename"
    bl_description = (
        "Rename object with _Pt.000_v.000 suffix appended automatically"
    )
    bl_options = {'REGISTER', 'UNDO'}

    new_base_name: bpy.props.StringProperty(
        name="Base Name",
        description="Object base name (suffix _Pt.000_v.000 will be appended)",
        default="",
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def invoke(self, context, event):
        obj = context.active_object
        self.new_base_name = naming.strip_suffix(obj.name)
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Suffix  _Pt.000_v.000  will be appended.")
        layout.prop(self, "new_base_name")

    def execute(self, context):
        base = self.new_base_name.strip()
        if not base:
            self.report({'WARNING'}, "Name cannot be empty.")
            return {'CANCELLED'}
        context.active_object.name = naming.build_name(base, "000", "000")
        return {'FINISHED'}


class OBJECT_OT_pv_copy_normal(bpy.types.Operator):
    bl_idname = "object.pv_copy_normal"
    bl_label = "Normal Copy"
    bl_description = "Standard duplicate without name transformation"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.ops.object.duplicate(linked=False)
        return {'FINISHED'}


class OBJECT_OT_pv_copy_pattern(bpy.types.Operator):
    bl_idname = "object.pv_copy_pattern"
    bl_label = "Pattern Copy"
    bl_description = (
        "Duplicate and assign next Pt number. Version resets to 000"
    )
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        source_obj = context.active_object

        parsed = naming.parse_name(source_obj.name)
        base = parsed.base if parsed else source_obj.name

        # Scan before duplicating so the new object is not included
        max_pt = naming.max_pt_number_for_base(base, context.scene.objects)
        # Unmanaged source is treated as implicit Pt.000; first copy → Pt.001
        next_pt = max(max_pt + 1, 1)

        bpy.ops.object.duplicate(linked=False)
        context.active_object.name = naming.build_name_from_int(base, next_pt, 0)

        return {'FINISHED'}


CLASSES = [
    OBJECT_OT_pv_rename,
    OBJECT_OT_pv_copy_normal,
    OBJECT_OT_pv_copy_pattern,
]
