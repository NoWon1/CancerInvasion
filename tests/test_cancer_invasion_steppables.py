import sys
from unittest.mock import MagicMock
import numpy as np
import pytest

# Mock cc3d dependencies before importing our module
sys.modules['cc3d'] = MagicMock()
sys.modules['cc3d.core'] = MagicMock()
pmock = MagicMock()
class SteppableBasePy:
    def __init__(self, freq): pass
pmock.SteppableBasePy = SteppableBasePy
sys.modules['cc3d.core.PySteppables'] = pmock

from Simulation.CancerInvasionSteppables import CancerInvasionSteppable

class TestSafeCellRemoval:

    @pytest.fixture
    def steppable(self):
        s = CancerInvasionSteppable()
        # Mocking the dimensions
        s.dim = MagicMock()
        s.dim.x = 10
        s.dim.y = 10

        # Mocking the cell_field as a numpy array with an extra dimension to mimic [x, y, 0] access
        # Since it accesses s.cell_field[x, y, 0], let's create a 3D list or array.
        # However, numpy object arrays are good. We'll use a normal object array.
        s.cell_field = np.empty((10, 10, 1), dtype=object)

        return s

    def test_safe_cell_removal_success(self, steppable):
        """Verify successful cell removal."""
        cell_to_remove = "cell1"
        steppable.cell_field[2, 3, 0] = cell_to_remove
        steppable.cell_field[2, 4, 0] = cell_to_remove
        steppable.cell_field[5, 5, 0] = "cell2"

        result = steppable.safe_cell_removal(cell_to_remove)

        assert result is True
        assert steppable.cell_field[2, 3, 0] is None
        assert steppable.cell_field[2, 4, 0] is None
        assert steppable.cell_field[5, 5, 0] == "cell2"

    def test_safe_cell_removal_no_cell_found(self, steppable):
        """Verify behavior when the cell is absent."""
        cell_to_remove = "cell1"
        steppable.cell_field[5, 5, 0] = "cell2"

        result = steppable.safe_cell_removal(cell_to_remove)

        assert result is False
        assert steppable.cell_field[5, 5, 0] == "cell2"

    def test_safe_cell_removal_exception_in_loop(self, steppable):
        """Verify error handling for exceptions during pixel processing."""
        cell_to_remove = "cell1"
        steppable.cell_field[2, 3, 0] = cell_to_remove

        # We will mock the cell_field to raise an exception on specific access.
        # One way is to create a wrapper class that raises Exception for (5,5,0)
        class MockCellField:
            def __init__(self, data):
                self.data = data

            def __getitem__(self, key):
                if key == (5, 5, 0):
                    raise IndexError("Mocked exception")
                return self.data[key]

            def __setitem__(self, key, value):
                if key == (5, 5, 0):
                    raise IndexError("Mocked exception")
                self.data[key] = value

        steppable.cell_field = MockCellField(steppable.cell_field)

        result = steppable.safe_cell_removal(cell_to_remove)

        assert result is True
        assert steppable.cell_field[2, 3, 0] is None

    def test_safe_cell_removal_global_exception(self, steppable):
        """Verify error handling for broader exceptions (like missing dimensions)."""
        # If we delete dim, accessing self.dim.x should raise AttributeError
        del steppable.dim

        result = steppable.safe_cell_removal("cell1")

        assert result is False
