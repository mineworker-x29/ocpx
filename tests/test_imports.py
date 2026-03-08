from ocpx.ocel.loader import load_ocel2
from ocpx.ocel.models import CanonicalOCEL


def test_imports():
    assert load_ocel2 is not None
    assert CanonicalOCEL is not None