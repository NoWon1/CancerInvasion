import sys
import unittest
from unittest.mock import MagicMock

# Mock cc3d module and dependencies before importing Steppable


class MockSteppableBasePy:
    def __init__(self, frequency=1):
        self.frequency = frequency


mock_cc3d = MagicMock()
mock_cc3d.core.PySteppables.SteppableBasePy = MockSteppableBasePy
sys.modules['cc3d'] = mock_cc3d
sys.modules['cc3d.core'] = mock_cc3d.core
sys.modules['cc3d.core.PySteppables'] = mock_cc3d.core.PySteppables

from Simulation.CancerInvasionSteppables import CancerInvasionSteppable  # noqa


class TestCancerInvasionSteppable(unittest.TestCase):
    def setUp(self):
        self.steppable = CancerInvasionSteppable(frequency=1)
        # Mock dim object
        self.steppable.dim = MagicMock()
        self.steppable.dim.x = 500
        self.steppable.dim.y = 500

    def test_create_simple_fiber_basic(self):
        """Test basic fiber creation within valid boundaries"""
        start_x, start_y = 250, 250
        angle = 0  # Horizontal fiber (dx=1, dy=0)
        self.steppable.fiber_length = 5

        pixels = self.steppable.create_simple_fiber(start_x, start_y, angle)

        # Base points should be (250, 250), (251, 250)... etc
        self.assertTrue(len(pixels) > 0)
        self.assertIn((250, 250), pixels)
        self.assertIn((254, 250), pixels)

        # Check thickness offsets (e.g. at start point)
        self.assertIn((249, 250), pixels)  # x-1
        self.assertIn((251, 250), pixels)  # x+1
        self.assertIn((250, 249), pixels)  # y-1
        self.assertIn((250, 251), pixels)  # y+1

    def test_create_simple_fiber_boundary_low(self):
        """Test fiber creation near the lower boundary (< 50)"""
        start_x, start_y = 45, 250  # Start x is below the 50 threshold
        angle = 0  # Moving right
        self.steppable.fiber_length = 10

        pixels = self.steppable.create_simple_fiber(start_x, start_y, angle)

        # Points below 50 should be skipped
        for x, y in pixels:
            self.assertTrue(x >= 50)
            self.assertTrue(y >= 50)

    def test_create_simple_fiber_boundary_high(self):
        """Test fiber creation near the upper boundary (>= dim - 50)"""
        start_x, start_y = 445, 250  # Dim is 500, max allowed is < 450
        angle = 0  # Moving right
        self.steppable.fiber_length = 10

        pixels = self.steppable.create_simple_fiber(start_x, start_y, angle)

        # Points >= 450 should be skipped
        for x, y in pixels:
            self.assertTrue(x < 450)
            self.assertTrue(y < 450)

    def test_create_simple_fiber_exception_handling(self):
        """Test that exceptions during fiber creation are handled"""
        # Force an exception by breaking dim
        del self.steppable.dim.x

        start_x, start_y = 250, 250
        angle = 0

        pixels = self.steppable.create_simple_fiber(start_x, start_y, angle)

        self.assertEqual(pixels, [])

    def test_handle_mmp_system_secretion(self):
        """Test that MMP is secreted by cells that touch a simple fiber."""
        # Set up constants manually for testing
        self.steppable.CELL = 1
        self.steppable.ECMFIBER = 2

        # Set up fields
        mock_mmp_field = MagicMock()
        mock_secretor = MagicMock()

        self.steppable.field = MagicMock()
        self.steppable.field.MMP = mock_mmp_field
        self.steppable.get_field_secretor = MagicMock(
            return_value=mock_secretor
        )
        self.steppable.check_simple_fiber_contact = MagicMock(
            return_value=True
        )

        # Set up a cell
        mock_cell = MagicMock()
        mock_cell.type = self.steppable.CELL

        self.steppable.cell_list = [mock_cell]

        self.steppable.handle_mmp_system()

        # Assert secretion happened
        mock_secretor.secreteInsideCell.assert_called_once_with(

            mock_cell, self.steppable.mmp_secretion_rate)

    def test_handle_mmp_system_no_contact(self):
        """Test that MMP is not secreted if cell doesn't contact fiber."""
        self.steppable.CELL = 1
        self.steppable.ECMFIBER = 2

        mock_mmp_field = MagicMock()
        mock_secretor = MagicMock()

        self.steppable.field = MagicMock()
        self.steppable.field.MMP = mock_mmp_field
        self.steppable.get_field_secretor = MagicMock(
            return_value=mock_secretor
        )
        self.steppable.check_simple_fiber_contact = MagicMock(
            return_value=False
        )

        mock_cell = MagicMock()
        mock_cell.type = self.steppable.CELL

        self.steppable.cell_list = [mock_cell]

        self.steppable.handle_mmp_system()

        # Assert secretion didn't happen
        mock_secretor.secreteInsideCell.assert_not_called()

    def test_handle_mmp_system_fiber_degradation(self):
        """Test that fibers are degraded when MMP concentration is high."""
        self.steppable.CELL = 1
        self.steppable.ECMFIBER = 2

        # We need a proper dict-like field for degradation
        mock_mmp_field = {(100, 100, 0): 2.0}   # conc 2.0 > thresh 1.0

        self.steppable.field = MagicMock()
        self.steppable.field.MMP = mock_mmp_field
        self.steppable.get_field_secretor = MagicMock()
        self.steppable.safe_cell_removal = MagicMock()

        # Set up a fiber cell
        mock_fiber = MagicMock()
        mock_fiber.type = self.steppable.ECMFIBER
        mock_fiber.xCOM = 100
        mock_fiber.yCOM = 100

        self.steppable.cell_list = [mock_fiber]

        self.steppable.handle_mmp_system()

        # Check that fiber was removed
        self.steppable.safe_cell_removal.assert_called_once_with(mock_fiber)

        # Check that concentration decreased
        self.assertEqual(mock_mmp_field[(100, 100, 0)], 1.5)

    def test_handle_mmp_system_fiber_no_degradation(self):
        """Test that fibers are not degraded when MMP concentration is low."""
        self.steppable.CELL = 1
        self.steppable.ECMFIBER = 2

        mock_mmp_field = {(100, 100, 0): 0.5}   # conc 0.5 < thresh 1.0

        self.steppable.field = MagicMock()
        self.steppable.field.MMP = mock_mmp_field
        self.steppable.get_field_secretor = MagicMock()
        self.steppable.safe_cell_removal = MagicMock()

        mock_fiber = MagicMock()
        mock_fiber.type = self.steppable.ECMFIBER
        mock_fiber.xCOM = 100
        mock_fiber.yCOM = 100

        self.steppable.cell_list = [mock_fiber]

        self.steppable.handle_mmp_system()

        self.steppable.safe_cell_removal.assert_not_called()
        self.assertEqual(mock_mmp_field[(100, 100, 0)], 0.5)

    def test_handle_mmp_system_exception_handling(self):
        """Test that exceptions during handle_mmp_system are caught."""
        self.steppable.field = MagicMock()
        # Force exception by passing object without MMP attribute
        del self.steppable.field.MMP

        self.steppable.error_count = 0

        self.steppable.handle_mmp_system()

        # The error count should increment upon handling exception
        self.assertEqual(self.steppable.error_count, 1)


if __name__ == '__main__':
    unittest.main()
