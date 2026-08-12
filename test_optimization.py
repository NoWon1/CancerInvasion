import pytest
import sys
from unittest.mock import MagicMock
import random
import math

class MockCellField:
    def __init__(self):
        self.data = {}

    def __getitem__(self, key):
        return self.data.get(key, None)

    def __setitem__(self, key, value):
        self.data[key] = value

class MockCell:
    def __init__(self, cell_type, cell_id=1):
        self.type = cell_type
        self.id = cell_id
        self.xCOM = 100
        self.yCOM = 100

class MockDim:
    def __init__(self, x=500, y=500):
        self.x = x
        self.y = y

class MockSteppableBasePy:
    def __init__(self, frequency=1):
        self.frequency = frequency
        self.dim = MockDim()
        self.cell_field = MockCellField()
        self.cell_list = []
        self.field = MagicMock()
        self.CELL = 1
        self.ECMFIBER = 2

    def new_cell(self, cell_type):
        cell = MockCell(cell_type, cell_id=random.randint(1, 1000))
        self.cell_list.append(cell)
        return cell

    def get_field_secretor(self, field_name):
        return MagicMock()

# Mock the cc3d module and its submodules
mock_cc3d = MagicMock()
mock_core = MagicMock()
mock_core.PySteppables = MagicMock()
mock_core.PySteppables.SteppableBasePy = MockSteppableBasePy
mock_core.PySteppables.MitosisSteppableBase = MockSteppableBasePy
mock_cc3d.core = mock_core
sys.modules['cc3d'] = mock_cc3d
sys.modules['cc3d.core'] = mock_core
sys.modules['cc3d.core.PySteppables'] = mock_core.PySteppables

from Simulation.CancerInvasionSteppables import CancerInvasionSteppable

def test_safe_cell_removal():
    steppable = CancerInvasionSteppable(frequency=1)

    cell = steppable.new_cell(steppable.CELL)
    cell.xCOM = 10
    cell.yCOM = 10

    steppable.cell_field[10, 10, 0] = cell
    steppable.cell_field[11, 11, 0] = cell

    result = steppable.safe_cell_removal(cell)

    assert result is True
    assert steppable.cell_field[10, 10, 0] is None
    assert steppable.cell_field[11, 11, 0] is None

def test_check_ecm_contact():
    steppable = CancerInvasionSteppable(frequency=1)

    cancer_cell = steppable.new_cell(steppable.CELL)
    cancer_cell.xCOM = 100
    cancer_cell.yCOM = 100

    ecm_cell = steppable.new_cell(steppable.ECMFIBER)
    ecm_cell.xCOM = 102
    ecm_cell.yCOM = 102
    steppable.cell_field[102, 102, 0] = ecm_cell

    result = steppable.check_ecm_contact(cancer_cell)
    assert result is True

    # Test boundary condition
    cancer_cell_boundary = steppable.new_cell(steppable.CELL)
    cancer_cell_boundary.xCOM = 0
    cancer_cell_boundary.yCOM = 0

    # No ECM nearby
    result_boundary = steppable.check_ecm_contact(cancer_cell_boundary)
    assert result_boundary is False
