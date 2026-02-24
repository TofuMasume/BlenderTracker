"""
Naming convention utilities for Pattern & Version Manager.

Name format: <BaseName>_Pt.<PtToken>_v.<VToken>
  PtToken: "Base" | 3-digit zero-padded integer (000-999)
  VToken:  3-digit zero-padded integer (000-999)

This module has no bpy dependency and can be tested with plain Python.
"""

import re
from dataclasses import dataclass
from typing import Optional

PT_BASE_TOKEN = "Base"

_PATTERN = re.compile(
    r'^(?P<base>.+?)_Pt\.(?P<pt>Base|\d{3})_v\.(?P<v>\d{3})$'
)


@dataclass
class ParsedName:
    base: str
    pt: str      # "Base" or "000"–"999"
    version: str  # "000"–"999"

    @property
    def pt_is_base(self) -> bool:
        return self.pt == PT_BASE_TOKEN

    @property
    def pt_int(self) -> Optional[int]:
        """Returns integer value of pt, or None if pt is 'Base'."""
        return None if self.pt_is_base else int(self.pt)


def parse_name(full_name: str) -> Optional[ParsedName]:
    """
    Parse a managed object name.
    Returns None if the name does not match the managed pattern.
    """
    m = _PATTERN.match(full_name)
    if not m:
        return None
    return ParsedName(
        base=m.group("base"),
        pt=m.group("pt"),
        version=m.group("v"),
    )


def build_name(base: str, pt: str, version: str) -> str:
    """
    Construct a managed object name from components.
    pt can be 'Base' or a zero-padded 3-digit string like '000'.
    version must be a zero-padded 3-digit string.
    """
    return f"{base}_Pt.{pt}_v.{version}"


def build_name_from_int(base: str, pt_int: int, version_int: int) -> str:
    """Construct a managed object name from integer pt and version values."""
    return build_name(base, f"{pt_int:03d}", f"{version_int:03d}")


def strip_suffix(full_name: str) -> str:
    """
    If the name matches the managed pattern, return only the base name.
    Otherwise return the name unchanged.
    Used to pre-populate the rename dialog.
    """
    parsed = parse_name(full_name)
    return parsed.base if parsed else full_name


def max_pt_number_for_base(base: str, scene_objects) -> int:
    """
    Scan scene objects and return the highest integer Pt number for a
    given base name. Returns -1 if no managed objects with numeric Pt
    are found. 'Base' tokens are excluded from the numeric max.
    """
    max_pt = -1
    for obj in scene_objects:
        parsed = parse_name(obj.name)
        if parsed is None:
            continue
        if parsed.base != base:
            continue
        if parsed.pt_is_base:
            continue
        if parsed.pt_int is not None:
            max_pt = max(max_pt, parsed.pt_int)
    return max_pt
