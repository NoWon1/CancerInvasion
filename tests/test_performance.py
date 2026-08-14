import sys
import pytest
from unittest.mock import MagicMock, patch

# Mock CompuCell3D dependencies BEFORE importing steppables
class SteppableBasePy:
    def __init__(self, frequency=1):
        self.frequency = frequency

class MitosisSteppableBase:
    def __init__(self, frequency=1):
        self.frequency = frequency

class MacroscopicCellMock:
    def __init__(self, type_id, id_val):
        self.type = type_id
        self.id = id_val
        self.xCOM = 250.0
        self.yCOM = 250.0
        self.volume = 400
        self.targetVolume = 400

class DimMock:
    def __init__(self):
        self.x = 500
        self.y = 500
        self.z = 1

class CellFieldMock:
    def __init__(self):
        self._data = {}

    def __getitem__(self, key):
        return self._data.get(key, None)

    def __setitem__(self, key, value):
        self._data[key] = value

class MMPFieldMock:
    def __init__(self):
        self._data = {}

    def __getitem__(self, key):
        return self._data.get(key, 0.5)

    def __setitem__(self, key, value):
        self._data[key] = value

class FieldMock:
    def __init__(self):
        self.MMP = MMPFieldMock()

# Setup mocks in sys.modules
mock_cc3d = MagicMock()
mock_cc3d_core = MagicMock()
mock_cc3d_core_PySteppables = MagicMock()
mock_cc3d_core_PySteppables.SteppableBasePy = SteppableBasePy
mock_cc3d_core_PySteppables.MitosisSteppableBase = MitosisSteppableBase

sys.modules['cc3d'] = mock_cc3d
sys.modules['cc3d.core'] = mock_cc3d_core
sys.modules['cc3d.core.PySteppables'] = mock_cc3d_core_PySteppables

# Now we can import the module
from Simulation.CancerInvasionSteppables import CancerInvasionSteppable, GrowthSteppable, ChemotaxisSteppable

def create_steppable(cls):
    steppable = cls(frequency=1)
    steppable.dim = DimMock()
    steppable.cell_field = CellFieldMock()
    steppable.field = FieldMock()
    steppable.cell_list = []

    # Common type mock
    steppable.CELL = 1
    steppable.ECMFIBER = 2

    # Mock methods
    def mock_new_cell(cell_type):
        return MacroscopicCellMock(cell_type, 999)
    steppable.new_cell = mock_new_cell

    return steppable

def test_initialize_paper_ecm_no_exception():
    steppable = create_steppable(CancerInvasionSteppable)
    # Give cell field some data just at the edge to ensure the check is correct
    # The actual implementation just uses the cell_field without exceptions

    try:
        steppable.initialize_paper_ecm()
    except Exception as e:
        pytest.fail(f"initialize_paper_ecm raised exception: {e}")

def test_create_paper_cell_no_exception():
    steppable = create_steppable(CancerInvasionSteppable)
    try:
        steppable.create_paper_cell(495, 495, 10) # Cell near edge
    except Exception as e:
        pytest.fail(f"create_paper_cell raised exception: {e}")

def test_safe_cell_removal_no_exception():
    steppable = create_steppable(CancerInvasionSteppable)
    cell = MacroscopicCellMock(1, 1)
    cell.xCOM = 495
    cell.yCOM = 495
    try:
        steppable.safe_cell_removal(cell)
    except Exception as e:
        pytest.fail(f"safe_cell_removal raised exception: {e}")

def test_paper_mmp_system_no_exception():
    steppable = create_steppable(CancerInvasionSteppable)

    # Add a fiber cell near the edge
    fiber = MacroscopicCellMock(2, 2)
    fiber.xCOM = 498
    fiber.yCOM = 498
    steppable.cell_list.append(fiber)

    try:
        steppable.paper_mmp_system()
    except Exception as e:
        pytest.fail(f"paper_mmp_system raised exception: {e}")

def test_check_ecm_contact_no_exception():
    steppable = create_steppable(CancerInvasionSteppable)
    cell = MacroscopicCellMock(1, 1)
    cell.xCOM = 1
    cell.yCOM = 1

    try:
        result = steppable.check_ecm_contact(cell)
        assert isinstance(result, bool)
    except Exception as e:
        pytest.fail(f"check_ecm_contact raised exception: {e}")

def test_growth_steppable_step_no_exception():
    steppable = create_steppable(GrowthSteppable)

    # Mock get_cell_neighbor_data_list to return empty list
    steppable.get_cell_neighbor_data_list = lambda cell: []

    cell = MacroscopicCellMock(1, 1)
    cell.xCOM = 499
    cell.yCOM = 499
    steppable.cell_list.append(cell)

    try:
        steppable.step(1)
    except Exception as e:
        pytest.fail(f"GrowthSteppable.step raised exception: {e}")

def test_chemotaxis_steppable_apply_no_exception():
    steppable = create_steppable(ChemotaxisSteppable)
    cell = MacroscopicCellMock(1, 1)
    cell.xCOM = 1
    cell.yCOM = 1

    try:
        steppable.apply_paper_chemotaxis(cell)
    except Exception as e:
        pytest.fail(f"ChemotaxisSteppable.apply_paper_chemotaxis raised exception: {e}")
