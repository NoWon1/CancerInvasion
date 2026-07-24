import sys
import builtins
import types

# Create mock cc3d modules
pysteppables_mock = types.ModuleType('cc3d.core.PySteppables')
sys.modules['cc3d'] = types.ModuleType('cc3d')
sys.modules['cc3d.core'] = types.ModuleType('cc3d.core')
sys.modules['cc3d.core.PySteppables'] = pysteppables_mock

# The builtins trick to provide base classes
class MockSteppableBasePy:
    def __init__(self, frequency=1):
        pass

class MockMitosisSteppableBase:
    def __init__(self, frequency=1):
        pass

builtins.SteppableBasePy = MockSteppableBasePy
builtins.MitosisSteppableBase = MockMitosisSteppableBase

sys.path.append('Simulation')
from CancerInvasionSteppables import CancerInvasionSteppable

class MockCell:
    def __init__(self, id, type, xCOM, yCOM):
        self.id = id
        self.type = type
        self.xCOM = xCOM
        self.yCOM = yCOM

class MockDim:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class MockCellField:
    def __init__(self):
        self._data = {}

    def __getitem__(self, key):
        return self._data.get(key, None)

    def __setitem__(self, key, value):
        self._data[key] = value

def test_safe_cell_removal():
    steppable = CancerInvasionSteppable()
    steppable.dim = MockDim(500, 500)
    steppable.cell_field = MockCellField()

    cell = MockCell(1, 1, 250, 250)
    steppable.cell_field[250, 250, 0] = cell
    steppable.cell_field[251, 250, 0] = cell

    removed = steppable.safe_cell_removal(cell)
    assert removed == True
    assert steppable.cell_field[250, 250, 0] is None
    assert steppable.cell_field[251, 250, 0] is None

def test_check_ecm_contact():
    steppable = CancerInvasionSteppable()
    steppable.dim = MockDim(500, 500)
    steppable.cell_field = MockCellField()
    steppable.ECMFIBER = 2

    cell = MockCell(1, 1, 250, 250)

    contact = steppable.check_ecm_contact(cell)
    assert contact == False

    ecm_cell = MockCell(2, steppable.ECMFIBER, 251, 251)
    steppable.cell_field[251, 251, 0] = ecm_cell

    contact = steppable.check_ecm_contact(cell)
    assert contact == True
