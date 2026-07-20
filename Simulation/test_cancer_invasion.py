import sys
import types
import pytest
from unittest.mock import MagicMock

# Mock cc3d
cc3d_mock = types.ModuleType("cc3d")
sys.modules["cc3d"] = cc3d_mock
core_mock = types.ModuleType("cc3d.core")
sys.modules["cc3d.core"] = core_mock
pysteppables = types.ModuleType("cc3d.core.PySteppables")
sys.modules["cc3d.core.PySteppables"] = pysteppables

class SteppableBasePy:
    def __init__(self, frequency=1):
        self.frequency = frequency
        class Dim:
            x = 500
            y = 500
            z = 1
        self.dim = Dim()
        self.cell_field = MagicMock()
        class Field:
            MMP = MagicMock()
        self.field = Field()
        self.cell_list = []
        self.CELL = 1
        self.ECMFIBER = 2

class MitosisSteppableBase(SteppableBasePy):
    pass

pysteppables.SteppableBasePy = SteppableBasePy
pysteppables.MitosisSteppableBase = MitosisSteppableBase

import builtins
builtins.SteppableBasePy = SteppableBasePy
builtins.MitosisSteppableBase = MitosisSteppableBase

def test_imports():
    from CancerInvasionSteppables import CancerInvasionSteppable
    steppable = CancerInvasionSteppable()
    assert steppable.frequency == 1
