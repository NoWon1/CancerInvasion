import pytest
import sys
import unittest.mock as mock

# Mock cc3d
cc3d = mock.MagicMock()
sys.modules['cc3d'] = cc3d
sys.modules['cc3d.core'] = mock.MagicMock()
sys.modules['cc3d.core.PySteppables'] = mock.MagicMock()

class MockSteppableBasePy:
    def __init__(self, frequency):
        self.frequency = frequency
        self.dim = mock.MagicMock()
        self.dim.x = 500
        self.dim.y = 500
        self.cell_field = {}
        self.cell_list = []
        self.CELL = 1
        self.ECMFIBER = 2

    def new_cell(self, cell_type):
        cell = mock.MagicMock()
        cell.type = cell_type
        cell.id = len(self.cell_list) + 1
        cell.xCOM = 250
        cell.yCOM = 250
        self.cell_list.append(cell)
        return cell

    def get_field_secretor(self, field_name):
        return mock.MagicMock()

sys.modules['cc3d.core.PySteppables'].SteppableBasePy = MockSteppableBasePy
import builtins
builtins.SteppableBasePy = MockSteppableBasePy


import Simulation.CancerInvasionSteppables as cis

def test_initialization():
    steppable = cis.CancerInvasionSteppable(frequency=1)
    steppable.start()
    assert steppable.simulation_failed == False
