import pytest
import sys
from unittest.mock import MagicMock

# Mock cc3d modules
cc3d_mock = MagicMock()
core_mock = MagicMock()
pysteppables_mock = MagicMock()
class SteppableBasePyMock:
    def __init__(self, frequency=1):
        self.frequency = frequency
class MitosisSteppableBaseMock:
    def __init__(self, frequency=1):
        self.frequency = frequency

pysteppables_mock.SteppableBasePy = SteppableBasePyMock
pysteppables_mock.MitosisSteppableBase = MitosisSteppableBaseMock

core_mock.PySteppables = pysteppables_mock
cc3d_mock.core = core_mock
sys.modules['cc3d'] = cc3d_mock
sys.modules['cc3d.core'] = core_mock
sys.modules['cc3d.core.PySteppables'] = pysteppables_mock

# Now we can safely import our module
from CancerInvasionSteppables import CancerInvasionSteppable

class MockDim:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class MockCell:
    def __init__(self, cell_type, x, y):
        self.type = cell_type
        self.xCOM = x
        self.yCOM = y

class SafeDict(dict):
    def __getitem__(self, key):
        return self.get(key, None)

def test_no_swig_exceptions():
    # Instantiate the steppable
    steppable = CancerInvasionSteppable(frequency=1)

    # Mock necessary properties that CC3D injects
    steppable.dim = MockDim(500, 500)
    steppable.CELL = 1
    steppable.ECMFIBER = 2

    # Use SafeDict to simulate CC3D's SWIG cell_field
    # If the code uses try..except to catch KeyErrors on missing items, this will fail if we don't return None safely for out-of-bounds,
    # OR we just populate all possible bounds.
    # Actually, the SafeDict mirrors normal `get` behavior which CC3D's SWIG wrapper does when in-bounds,
    # but SWIG throws when out of bounds. We want to ensure we don't query out of bounds!

    class StrictBoundDict(dict):
        def __init__(self, x_dim, y_dim):
            self.x_dim = x_dim
            self.y_dim = y_dim
            super().__init__()

        def __getitem__(self, key):
            x, y, z = key
            if x < 0 or x >= self.x_dim or y < 0 or y >= self.y_dim:
                raise Exception(f"SWIG IndexError: out of bounds {x}, {y}")
            return super().get(key, None)

    steppable.cell_field = StrictBoundDict(steppable.dim.x, steppable.dim.y)
    steppable.new_cell = lambda t: MockCell(t, 0, 0)
    steppable.cell_list = []

    # Test create_paper_cell near the boundary to ensure it doesn't throw SWIG error
    # With center (495, 495) and radius 6, it will check up to 501, which should be caught by our dynamic boundary check.
    result = steppable.create_paper_cell(495, 495, 6)

    # Test check_ecm_contact near boundary
    boundary_cell = MockCell(steppable.CELL, 498, 498)
    # Should not throw exception
    steppable.check_ecm_contact(boundary_cell)

    # Test safe_cell_removal
    steppable.safe_cell_removal(boundary_cell)

if __name__ == "__main__":
    pytest.main(["-v", "test_optimization.py"])
