from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import pm4py

from .adapters import pm4py_ocel_to_canonical
from .models import CanonicalOCEL


def load_ocel2_pm4py(path: str | Path, variant_str: Optional[str] = None) -> Any:
    """
    Load an OCEL 2.0 log using PM4Py and return the raw PM4Py OCEL object.
    Supported formats are delegated to PM4Py (e.g. .jsonocel, .xmlocel, .sqlite).
    """
    path = str(path)
    return pm4py.read_ocel2(path, variant_str=variant_str)


def load_ocel2(path: str | Path, variant_str: Optional[str] = None) -> CanonicalOCEL:
    """
    Load an OCEL 2.0 log and convert it to ocpx's canonical representation.
    """
    pm4py_ocel = load_ocel2_pm4py(path=path, variant_str=variant_str)
    return pm4py_ocel_to_canonical(pm4py_ocel)


def load_ocel2_json(path: str | Path, variant_str: Optional[str] = None) -> CanonicalOCEL:
    pm4py_ocel = pm4py.read_ocel2_json(str(path), variant_str=variant_str)
    return pm4py_ocel_to_canonical(pm4py_ocel)


def load_ocel2_xml(path: str | Path, variant_str: Optional[str] = None) -> CanonicalOCEL:
    pm4py_ocel = pm4py.read_ocel2_xml(str(path), variant_str=variant_str)
    return pm4py_ocel_to_canonical(pm4py_ocel)


def load_ocel2_sqlite(path: str | Path, variant_str: Optional[str] = None) -> CanonicalOCEL:
    pm4py_ocel = pm4py.read_ocel2_sqlite(str(path), variant_str=variant_str)
    return pm4py_ocel_to_canonical(pm4py_ocel)