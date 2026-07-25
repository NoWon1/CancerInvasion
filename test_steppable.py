import pytest
from unittest.mock import MagicMock
import sys

# Mock CompuCell3D dependencies
mock_cc3d = MagicMock()
class SteppableBasePy:
    def __init__(self, frequency=1):
        self.frequency = frequency
        self.cell_list = []
        self.field = MagicMock()
        class Dim:
            x = 500
            y = 500
        self.dim = Dim()
        self.CELL = 1
        self.ECMFIBER = 2

class MitosisSteppableBase(SteppableBasePy):
    def __init__(self, frequency=1):
        super().__init__(frequency)

mock_cc3d.core.PySteppables.SteppableBasePy = SteppableBasePy
mock_cc3d.core.PySteppables.MitosisSteppableBase = MitosisSteppableBase
sys.modules["cc3d"] = mock_cc3d
sys.modules["cc3d.core"] = mock_cc3d.core
sys.modules["cc3d.core.PySteppables"] = mock_cc3d.core.PySteppables

from Simulation.CancerInvasionSteppables import CancerInvasionSteppable

# Custom dictionary that returns None instead of KeyError like CC3D
class MockCellField(dict):
    def __getitem__(self, key):
        return self.get(key, None)

def test_safe_cell_removal():
    steppable = CancerInvasionSteppable()
    cell = MagicMock()
    cell.xCOM = 250
    cell.yCOM = 250
    steppable.cell_field = MockCellField()
    steppable.cell_field[(250, 250, 0)] = cell
    assert steppable.safe_cell_removal(cell) is True
    assert steppable.cell_field[(250, 250, 0)] is None


def test_check_ecm_contact_out_of_bounds():
    steppable = CancerInvasionSteppable()
    steppable.cell_field = MockCellField()
    cell = MagicMock()
    cell.xCOM = 550
    cell.yCOM = 550
    # Should return False gracefully without KeyErrors or Exceptions
    assert steppable.check_ecm_contact(cell) is False
