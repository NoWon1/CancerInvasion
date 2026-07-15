import sys
from unittest.mock import MagicMock
import pytest

# Mock cc3d before importing Simulation
cc3d_mock = MagicMock()
class SteppableBasePy:
    def __init__(self, frequency=1):
        self.frequency = frequency

cc3d_mock.SteppableBasePy = SteppableBasePy
sys.modules['cc3d'] = cc3d_mock
sys.modules['cc3d.core'] = cc3d_mock
sys.modules['cc3d.core.PySteppables'] = cc3d_mock

from Simulation.CancerInvasionSteppables import CancerInvasionSteppable

class TestSafeCellRemoval:
    def setup_method(self):
        self.steppable = CancerInvasionSteppable()

        # Mock dim using a simple class instead of MagicMock to avoid mutation issues
        class DimMock:
            def __init__(self):
                self.x = 10
                self.y = 10
        self.steppable.dim = DimMock()

        # Set up a mock cell field
        self.cell_field_data = {}

        # A simple cell field mock that intercepts indexing
        class MockCellField:
            def __init__(self, data):
                self.data = data

            def __getitem__(self, key):
                return self.data.get(key, None)

            def __setitem__(self, key, value):
                self.data[key] = value

        self.steppable.cell_field = MockCellField(self.cell_field_data)

    def test_safe_cell_removal_success(self):
        """Test successful cell removal"""
        mock_cell = MagicMock()
        mock_cell.id = 1

        # Place cell in field
        self.cell_field_data[(5, 5, 0)] = mock_cell
        self.cell_field_data[(5, 6, 0)] = mock_cell

        result = self.steppable.safe_cell_removal(mock_cell)

        assert result is True
        assert self.cell_field_data[(5, 5, 0)] is None
        assert self.cell_field_data[(5, 6, 0)] is None

    def test_safe_cell_removal_no_cell_found(self):
        """Test removal when cell is not in field"""
        mock_cell = MagicMock()
        mock_cell.id = 1

        result = self.steppable.safe_cell_removal(mock_cell)

        assert result is False

    def test_safe_cell_removal_inner_exception(self):
        """Test inner exception handling (Exception on accessing cell field for a single pixel)"""
        mock_cell = MagicMock()

        # Mock cell field to raise an exception on specific access, but not all
        class ErrorCellField:
            def __getitem__(self, key):
                if key == (5, 5, 0):
                    raise ValueError("Inner error")
                return None

            def __setitem__(self, key, value):
                pass

        self.steppable.cell_field = ErrorCellField()

        result = self.steppable.safe_cell_removal(mock_cell)

        assert result is False

    def test_safe_cell_removal_outer_exception(self):
        """Test outer exception handling to verify it gracefully returns False"""
        mock_cell = MagicMock()

        # To trigger the outer exception, use a custom class for dim
        class ErrorDimMock:
            @property
            def x(self):
                raise RuntimeError("Outer error")

            @property
            def y(self):
                return 10

        self.steppable.dim = ErrorDimMock()

        result = self.steppable.safe_cell_removal(mock_cell)

        assert result is False
