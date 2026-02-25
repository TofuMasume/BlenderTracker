"""
Operators for Pattern & Version Manager.

Operators:
  OBJECT_OT_pv_rename           - Alt+F2 rename with auto-suffix
  OBJECT_OT_pv_copy_normal      - Standard duplicate
  OBJECT_OT_pv_copy_pattern     - Duplicate with incremented Pt number
  COLLECTION_OT_pv_rename       - Rename active collection with auto-suffix
  COLLECTION_OT_pv_copy_pattern - Duplicate collection with incremented Pt number
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

    new_base_name: bpy.props.StringProperty(  # noqa: F722
        name="Base Name",  # noqa: F722
        description="Object base name (suffix _Pt.000_v.000 will be appended)",  # noqa: F722
        default="",  # noqa: F722
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
        # If no numeric Pt exists in scene, start from Pt.000
        next_pt = max_pt + 1

        bpy.ops.object.duplicate(linked=False)
        new_name = naming.build_name_from_int(base, next_pt, 0)
        context.active_object.name = new_name

        return {'FINISHED'}


def _find_parent_collection(target_col, context):
    """Return the parent collection of target_col in the scene hierarchy, or None."""
    def _search(current_col):
        for child in current_col.children:
            if child == target_col:
                return current_col
            found = _search(child)
            if found:
                return found
        return None

    return _search(context.scene.collection)


class COLLECTION_OT_pv_rename(bpy.types.Operator):
    bl_idname = "collection.pv_rename"
    bl_label = "PV Rename Collection"
    bl_description = (
        "Rename collection with _Pt.000_v.000 suffix appended automatically"
    )
    bl_options = {'REGISTER', 'UNDO'}

    new_base_name: bpy.props.StringProperty(  # noqa: F722
        name="Base Name",  # noqa: F722
        description="Collection base name (suffix _Pt.000_v.000 will be appended)",  # noqa: F722
        default="",  # noqa: F722
    )

    @classmethod
    def poll(cls, context):
        alc = context.view_layer.active_layer_collection
        return alc is not None and alc.collection != context.scene.collection

    def invoke(self, context, event):
        col = context.view_layer.active_layer_collection.collection
        self.new_base_name = naming.strip_suffix(col.name)
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
        col = context.view_layer.active_layer_collection.collection
        col.name = naming.build_name(base, "000", "000")
        return {'FINISHED'}


class COLLECTION_OT_pv_copy_pattern(bpy.types.Operator):
    bl_idname = "collection.pv_copy_pattern"
    bl_label = "Pattern Copy Collection"
    bl_description = (
        "Duplicate collection and assign next Pt number. Version resets to 000"
    )
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        alc = context.view_layer.active_layer_collection
        return alc is not None and alc.collection != context.scene.collection

    def execute(self, context):
        source_col = context.view_layer.active_layer_collection.collection

        parsed = naming.parse_name(source_col.name)
        base = parsed.base if parsed else source_col.name

        # Scan before duplicating so the new collection is not included
        max_pt = naming.max_pt_number_for_base(base, bpy.data.collections)
        next_pt = max_pt + 1
        new_name = naming.build_name_from_int(base, next_pt, 0)

        parent_col = _find_parent_collection(source_col, context)
        if parent_col is None:
            parent_col = context.scene.collection

        new_col = bpy.data.collections.new(new_name)
        parent_col.children.link(new_col)

        for obj in source_col.objects:
            new_obj = obj.copy()
            if obj.data:
                new_obj.data = obj.data.copy()
            new_col.objects.link(new_obj)

        return {'FINISHED'}


CLASSES = [
    OBJECT_OT_pv_rename,
    OBJECT_OT_pv_copy_normal,
    OBJECT_OT_pv_copy_pattern,
    COLLECTION_OT_pv_rename,
    COLLECTION_OT_pv_copy_pattern,
]
