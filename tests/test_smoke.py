from pathlib import Path

import pytest

from ocpx import read_ocel
from ocpx.io.ocel import OcelIOError


def test_package_exports_read_ocel() -> None:
    assert callable(read_ocel)


def test_read_ocel_missing_path_raises_helpful_error(tmp_path: Path) -> None:
    missing = tmp_path / "missing.jsonocel"
    with pytest.raises(OcelIOError, match="does not exist"):
        read_ocel(missing)
