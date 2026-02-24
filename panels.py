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
        obj = context.active_object

        if obj is None:
            layout.label(text="No active object.", icon='INFO')
            return

        parsed = naming.parse_name(obj.name)

        # Name breakdown
        box = layout.box()
        box.label(text="Active Object", icon='OBJECT_DATA')
        if parsed:
            col = box.column(align=True)
            col.label(text=f"Base:    {parsed.base}")
            col.label(text=f"Pattern: Pt.{parsed.pt}")
            col.label(text=f"Version: v.{parsed.version}")
        else:
            box.label(text=obj.name)
            box.label(text="(unmanaged — no suffix)", icon='ERROR')

        layout.separator()

        layout.operator(
            "object.pv_rename",
            text="Rename  (Alt+F2)",
            icon='FONT_DATA',
        )

        layout.separator()
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


CLASSES = [
    VIEW3D_PT_pv_main,
]
