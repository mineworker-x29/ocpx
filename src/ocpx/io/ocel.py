"""Defensive wrappers around PM4Py OCEL I/O APIs."""

from __future__ import annotations

from pathlib import Path
from typing import Any


class OcelIOError(RuntimeError):
    """Raised when OCEL input/output cannot be completed."""


def _require_pm4py() -> Any:
    try:
        import pm4py
    except ModuleNotFoundError as exc:
        raise OcelIOError("PM4Py is required for OCEL I/O. Install dependency `pm4py`.") from exc
    return pm4py


def read_ocel(path: str | Path, /, **kwargs: Any) -> Any:
    """Read an OCEL file with PM4Py while handling API differences.

    Args:
        path: Path to OCEL source file.
        **kwargs: Forwarded to PM4Py reader.

    Returns:
        PM4Py OCEL object.

    Raises:
        OcelIOError: If PM4Py is unavailable or no suitable reader exists.
    """

    p = Path(path)
    if not p.exists():
        raise OcelIOError(f"OCEL input path does not exist: {p}")

    pm4py = _require_pm4py()

    if hasattr(pm4py, "read_ocel"):
        return pm4py.read_ocel(str(p), **kwargs)

    try:
        from pm4py.objects.ocel.importer import importer as ocel_importer
    except Exception as exc:  # pragma: no cover - fallback dependency path
        raise OcelIOError("Could not import PM4Py OCEL importer.") from exc

    try:
        return ocel_importer.apply(str(p), **kwargs)
    except Exception as exc:
        raise OcelIOError(f"Failed to read OCEL from {p}: {exc}") from exc


def write_ocel(ocel: Any, path: str | Path, /, **kwargs: Any) -> None:
    """Write an OCEL object using PM4Py while handling API differences.

    Args:
        ocel: PM4Py OCEL object.
        path: Destination path.
        **kwargs: Forwarded to PM4Py writer.

    Raises:
        OcelIOError: If writing fails or no suitable exporter exists.
    """

    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    pm4py = _require_pm4py()

    if hasattr(pm4py, "write_ocel"):
        try:
            pm4py.write_ocel(ocel, str(p), **kwargs)
            return
        except Exception as exc:
            raise OcelIOError(f"Failed to write OCEL to {p}: {exc}") from exc

    try:
        from pm4py.objects.ocel.exporter import exporter as ocel_exporter
    except Exception as exc:  # pragma: no cover - fallback dependency path
        raise OcelIOError("Could not import PM4Py OCEL exporter.") from exc

    try:
        ocel_exporter.apply(ocel, str(p), **kwargs)
    except Exception as exc:
        raise OcelIOError(f"Failed to write OCEL to {p}: {exc}") from exc
