import sys
import pytest
from unittest.mock import MagicMock

# --- Mock cc3d before import ---
mock_cc3d = MagicMock()
class MockSteppableBasePy:
    def __init__(self, frequency=1):
        pass
mock_cc3d.core.PySteppables.SteppableBasePy = MockSteppableBasePy

class MockModule:
    pass

mod = MockModule()
mod.SteppableBasePy = MockSteppableBasePy

sys.modules['cc3d'] = mock_cc3d
sys.modules['cc3d.core'] = mock_cc3d.core
sys.modules['cc3d.core.PySteppables'] = mod
# --- End Mock cc3d ---

from Simulation.CancerInvasionSteppables import CancerInvasionSteppable

class MockCell:
    def __init__(self, xCOM, yCOM, cell_type=None):
        self.xCOM = xCOM
        self.yCOM = yCOM
        self.type = cell_type

class MockCellField:
    def __init__(self):
        self.data = {}
    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        return None
    def __setitem__(self, key, value):
        self.data[key] = value

class TestCheckSimpleFiberContact:
    def setup_method(self):
        self.steppable = CancerInvasionSteppable(frequency=1)
        self.steppable.ECMFIBER = 2 # Dummy type for ECMFIBER
        self.steppable.cell_field = MockCellField()

    def test_contact_with_fiber(self):
        """Test that contact with an ECMFIBER cell returns True."""
        cell = MockCell(100.0, 100.0)

        # Place an ECM fiber nearby (dx=2, dy=1)
        fiber_cell = MockCell(102, 101, cell_type=self.steppable.ECMFIBER)
        self.steppable.cell_field[102, 101, 0] = fiber_cell

        assert self.steppable.check_simple_fiber_contact(cell) is True

    def test_no_contact(self):
        """Test that no contact returns False."""
        cell = MockCell(100.0, 100.0)

        # Place a different type of cell nearby
        other_cell = MockCell(102, 101, cell_type=1) # Not ECMFIBER
        self.steppable.cell_field[102, 101, 0] = other_cell

        assert self.steppable.check_simple_fiber_contact(cell) is False

    def test_boundary_conditions(self):
        """Test that boundary conditions are handled without crashing and return correct values."""
        cell = MockCell(0.0, 0.0) # Edge of grid

        # Place a fiber at (-1, 0) which is out of bounds
        fiber_cell_out_bounds = MockCell(-1, 0, cell_type=self.steppable.ECMFIBER)
        self.steppable.cell_field[-1, 0, 0] = fiber_cell_out_bounds

        # Place a fiber at (1, 1) which is in bounds
        fiber_cell_in_bounds = MockCell(1, 1, cell_type=self.steppable.ECMFIBER)
        self.steppable.cell_field[1, 1, 0] = fiber_cell_in_bounds

        assert self.steppable.check_simple_fiber_contact(cell) is True

        # Now remove in-bounds fiber and check
        self.steppable.cell_field[1, 1, 0] = None
        # The code will ignore the out-of-bounds check and should return False
        assert self.steppable.check_simple_fiber_contact(cell) is False

    def test_exception_handling(self):
        """Test that exceptions during cell coordinate access or field access return False."""
        # Cell without xCOM/yCOM should trigger an exception and return False
        class BadCell:
            pass

        cell = BadCell()
        assert self.steppable.check_simple_fiber_contact(cell) is False

        # Test exception in cell_field access
        good_cell = MockCell(50.0, 50.0)
        class ExceptionCellField:
            def __getitem__(self, key):
                raise Exception("Field access error")

        self.steppable.cell_field = ExceptionCellField()
        # Even with exception, it should return False and not crash
        assert self.steppable.check_simple_fiber_contact(good_cell) is False
