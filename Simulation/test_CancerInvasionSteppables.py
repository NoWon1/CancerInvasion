import sys
import builtins
from unittest.mock import MagicMock
import pytest

# Mocking the cc3d module because it's not a standard Python package
class MockSteppableBasePy:
    def __init__(self, frequency=1):
        self.frequency = frequency

@pytest.fixture(autouse=True)
def mock_steppable_base(monkeypatch):
    monkeypatch.setattr(builtins, "SteppableBasePy", MockSteppableBasePy, raising=False)

    mock_module = MagicMock()
    mock_module.SteppableBasePy = MockSteppableBasePy
    mock_module.__all__ = ['SteppableBasePy']

    monkeypatch.setitem(sys.modules, 'cc3d', MagicMock())
    monkeypatch.setitem(sys.modules, 'cc3d.core', MagicMock())
    monkeypatch.setitem(sys.modules, 'cc3d.core.PySteppables', mock_module)

def test_cancer_invasion_steppable_init():
    """Verify initialization of the CancerInvasionSteppable class"""
    # Need to import locally within test so that the monkeypatch has taken effect
    from Simulation.CancerInvasionSteppables import CancerInvasionSteppable
    steppable = CancerInvasionSteppable(frequency=2)

    # Asserting that Base Class initialization is properly invoked
    assert steppable.frequency == 2
