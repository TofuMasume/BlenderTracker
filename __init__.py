bl_info = {
    "name": "Pattern & Version Manager",
    "author": "masume",
    "version": (0, 1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > N-Panel > Pt/Ver",
    "description": "Manage object naming with Pt.NNN / v.NNN suffixes",
    "category": "Object",
}

import bpy

from . import operators
from . import panels
from . import keymaps

_CLASSES = [
    *operators.CLASSES,
    *panels.CLASSES,
]


def register():
    for cls in _CLASSES:
        bpy.utils.register_class(cls)
    keymaps.register()


def unregister():
    keymaps.unregister()
    for cls in reversed(_CLASSES):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
