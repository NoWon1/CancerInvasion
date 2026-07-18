import sys
from unittest.mock import MagicMock

# Mock cc3d
cc3d_mock = MagicMock()
cc3d_mock.core = MagicMock()
cc3d_mock.core.PySteppables = MagicMock()

# Mock SteppableBasePy and MitosisSteppableBase
class MockSteppableBasePy:
    def __init__(self, frequency=1):
        self.frequency = frequency
        self.cell_list = []
        self.cell_field = MagicMock()
        self.field = MagicMock()
        self.dim = MagicMock()
        self.dim.x = 500
        self.dim.y = 500
        self.dim.z = 1
        self.CELL = 1
        self.ECMFIBER = 2

    def new_cell(self, cell_type):
        cell = MagicMock()
        cell.type = cell_type
        return cell

    def get_field_secretor(self, field_name):
        return MagicMock()

class MockMitosisSteppableBase(MockSteppableBasePy):
    pass

cc3d_mock.core.PySteppables.SteppableBasePy = MockSteppableBasePy
cc3d_mock.core.PySteppables.MitosisSteppableBase = MockMitosisSteppableBase
sys.modules['cc3d'] = cc3d_mock
sys.modules['cc3d.core'] = cc3d_mock.core
sys.modules['cc3d.core.PySteppables'] = cc3d_mock.core.PySteppables

# Now import
import builtins
builtins.SteppableBasePy = MockSteppableBasePy
builtins.MitosisSteppableBase = MockMitosisSteppableBase

from Simulation.CancerInvasionSteppables import CancerInvasionSteppable

def test_safe_cell_removal():
    steppable = CancerInvasionSteppable()
    cell = MagicMock()
    cell.xCOM = 250
    cell.yCOM = 250

    # Setup cell_field mock to return cell at a specific location
    def cell_field_getitem(idx):
        x, y, z = idx
        if x == 250 and y == 250:
            return cell
        return None

    def cell_field_setitem(idx, val):
        pass

    steppable.cell_field.__getitem__.side_effect = cell_field_getitem
    steppable.cell_field.__setitem__.side_effect = cell_field_setitem

    result = steppable.safe_cell_removal(cell)
    assert result == True

if __name__ == "__main__":
    test_safe_cell_removal()
    print("Test passed!")
