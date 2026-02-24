"""
Keymap registration for Pattern & Version Manager.

Registers Alt+F2 in the 3D View to invoke the pv_rename operator.
"""

import bpy

_addon_keymaps: list = []


def register():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc is None:
        # Headless / no UI context — skip silently
        return

    km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
    kmi = km.keymap_items.new(
        "object.pv_rename",
        type='F2',
        value='PRESS',
        alt=True,
    )
    _addon_keymaps.append((km, kmi))


def unregister():
    for km, kmi in _addon_keymaps:
        km.keymap_items.remove(kmi)
    _addon_keymaps.clear()
