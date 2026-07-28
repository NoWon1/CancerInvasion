import pytest
import sys
from unittest.mock import MagicMock, patch

# Mock cc3d dependency
mock_cc3d = MagicMock()
mock_cc3d.core = MagicMock()
class SteppableBasePy:
    def __init__(self, frequency=1):
        self.frequency = frequency
class MitosisSteppableBase:
    def __init__(self, frequency=1):
        self.frequency = frequency

mock_cc3d.core.PySteppables = MagicMock()
mock_cc3d.core.PySteppables.SteppableBasePy = SteppableBasePy
mock_cc3d.core.PySteppables.MitosisSteppableBase = MitosisSteppableBase
sys.modules['cc3d'] = mock_cc3d
sys.modules['cc3d.core'] = mock_cc3d.core
sys.modules['cc3d.core.PySteppables'] = mock_cc3d.core.PySteppables

from Simulation.CancerInvasionSteppables import CancerInvasionSteppable

class MockCell:
    def __init__(self, x, y, ctype):
        self.xCOM = x
        self.yCOM = y
        self.type = ctype
        self.id = id(self)
        self.volume = 400

class MockCellField:
    def __init__(self, dim_x, dim_y):
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.field = {}

    def __getitem__(self, key):
        if not isinstance(key, tuple) or len(key) != 3:
            return None
        x, y, z = key
        # Explicitly check bounds here to simulate SWIG exceptions
        if not (0 <= x < self.dim_x and 0 <= y < self.dim_y):
            raise IndexError("Out of bounds")
        return self.field.get(key, None)

    def __setitem__(self, key, value):
        if not isinstance(key, tuple) or len(key) != 3:
            return
        x, y, z = key
        if not (0 <= x < self.dim_x and 0 <= y < self.dim_y):
            raise IndexError("Out of bounds")
        self.field[key] = value

class MockMMPField:
    def __init__(self, dim_x, dim_y):
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.field = {}

    def __getitem__(self, key):
        if not isinstance(key, tuple) or len(key) != 3:
            return 0
        x, y, z = key
        if not (0 <= x < self.dim_x and 0 <= y < self.dim_y):
            raise IndexError("Out of bounds")
        return self.field.get(key, 0)

    def __setitem__(self, key, value):
        if not isinstance(key, tuple) or len(key) != 3:
            return
        x, y, z = key
        if not (0 <= x < self.dim_x and 0 <= y < self.dim_y):
            raise IndexError("Out of bounds")
        self.field[key] = value

class MockDim:
    def __init__(self, x, y):
        self.x = x
        self.y = y

@pytest.fixture
def steppable():
    s = CancerInvasionSteppable(frequency=1)
    s.dim = MockDim(500, 500)
    s.cell_field = MockCellField(500, 500)
    s.cell_list = []

    s.field = MagicMock()
    s.field.MMP = MockMMPField(500, 500)

    s.CELL = 1
    s.ECMFIBER = 2

    s.new_cell = MagicMock()
    s.new_cell.side_effect = lambda t: MockCell(0, 0, t)

    return s

def test_check_ecm_contact(steppable):
    cell = MockCell(5, 5, steppable.CELL)
    ecm = MockCell(6, 6, steppable.ECMFIBER)
    steppable.cell_field[6, 6, 0] = ecm

    assert steppable.check_ecm_contact(cell) == True

def test_safe_cell_removal(steppable):
    cell = MockCell(10, 10, steppable.CELL)
    steppable.cell_field[10, 10, 0] = cell
    steppable.cell_field[11, 11, 0] = cell

    assert steppable.safe_cell_removal(cell) == True
    assert steppable.cell_field[10, 10, 0] is None

def test_create_paper_cell(steppable):
    assert steppable.create_paper_cell(250, 250, 5) == True

def test_initialize_paper_ecm(steppable):
    steppable.initialize_paper_ecm()
    # verify fibers were created
    assert len(steppable.fiber_locations) > 0

def test_paper_mmp_system(steppable):
    cell = MockCell(10, 10, steppable.CELL)
    steppable.cell_list.append(cell)

    ecm = MockCell(11, 11, steppable.ECMFIBER)
    steppable.cell_list.append(ecm)

    steppable.cell_field[11, 11, 0] = ecm

    steppable.mmp_secretor = MagicMock()

    steppable.field.MMP[11, 11, 0] = 1.5

    steppable.paper_mmp_system()

    # check secretion called
    steppable.mmp_secretor.secreteInsideCell.assert_called()

    # Check degradation
    assert steppable.field.MMP[11, 11, 0] == 0.5
