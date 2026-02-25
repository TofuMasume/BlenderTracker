"""
N-Panel for Pattern & Version Manager.

Location: View3D > Sidebar > Pt/Ver tab
"""

import bpy
from . import naming


class VIEW3D_PT_pv_main(bpy.types.Panel):
    bl_label = "Pattern & Version"
    bl_idname = "VIEW3D_PT_pv_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Pt/Ver"

    def draw(self, context):
        layout = self.layout

        # --- Object section ---
        obj = context.active_object
        box = layout.box()
        box.label(text="Active Object", icon='OBJECT_DATA')
        if obj is None:
            box.label(text="No active object.", icon='INFO')
        else:
            parsed = naming.parse_name(obj.name)
            if parsed:
                info_col = box.column(align=True)
                info_col.label(text=f"Base:    {parsed.base}")
                info_col.label(text=f"Pattern: Pt.{parsed.pt}")
                info_col.label(text=f"Version: v.{parsed.version}")
            else:
                box.label(text=obj.name)
                box.label(text="(unmanaged — no suffix)", icon='ERROR')

            layout.operator(
                "object.pv_rename",
                text="Rename  (Alt+F2)",
                icon='FONT_DATA',
            )
            layout.label(text="Copy:")
            row = layout.row(align=True)
            row.operator(
                "object.pv_copy_normal",
                text="Normal",
                icon='DUPLICATE',
            )
            row.operator(
                "object.pv_copy_pattern",
                text="Pattern Copy",
                icon='COPYDOWN',
            )

        layout.separator()

        # --- Collection section ---
        alc = context.view_layer.active_layer_collection
        active_col = (
            alc.collection
            if alc is not None and alc.collection != context.scene.collection
            else None
        )

        box2 = layout.box()
        box2.label(text="Active Collection", icon='OUTLINER_COLLECTION')
        if active_col is None:
            box2.label(text="No active collection.", icon='INFO')
        else:
            parsed_col = naming.parse_name(active_col.name)
            if parsed_col:
                info_col2 = box2.column(align=True)
                info_col2.label(text=f"Base:    {parsed_col.base}")
                info_col2.label(text=f"Pattern: Pt.{parsed_col.pt}")
                info_col2.label(text=f"Version: v.{parsed_col.version}")
            else:
                box2.label(text=active_col.name)
                box2.label(text="(unmanaged — no suffix)", icon='ERROR')

            layout.operator(
                "collection.pv_rename",
                text="Rename Collection",
                icon='FONT_DATA',
            )
            row2 = layout.row(align=True)
            row2.operator(
                "collection.pv_copy_pattern",
                text="Pattern Copy",
                icon='COPYDOWN',
            )


CLASSES = [
    VIEW3D_PT_pv_main,
]
