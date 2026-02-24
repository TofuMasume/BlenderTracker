"""
Keymap registration for Pattern & Version Manager.

Registers the following shortcuts in the 3D View:
  Alt+F2        - Rename with auto-suffix (object.pv_rename)
  Ctrl+Shift+D  - Pattern copy (object.pv_copy_pattern)
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

    kmi_pattern = km.keymap_items.new(
        "object.pv_copy_pattern",
        type='D',
        value='PRESS',
        ctrl=True,
        shift=True,
    )
    _addon_keymaps.append((km, kmi_pattern))


def unregister():
    for km, kmi in _addon_keymaps:
        km.keymap_items.remove(kmi)
    _addon_keymaps.clear()
