import sys
import unittest
from unittest.mock import MagicMock
from collections import defaultdict

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
        self.steppable.ECMFIBER = 2  # Assign an arbitrary type ID for ECMFIBER

        # Mock cell field as defaultdict returning None for empty spaces
        self.steppable.cell_field = defaultdict(lambda: None)

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

    def test_check_simple_fiber_contact_no_contact(self):
        """Test simple fiber contact check with no contact"""
        cell = MagicMock()
        cell.xCOM, cell.yCOM = 100.0, 100.0

        self.assertFalse(self.steppable.check_simple_fiber_contact(cell))

    def test_check_simple_fiber_contact_with_contact(self):
        """Test simple fiber contact check with contact"""
        cell = MagicMock()
        cell.xCOM, cell.yCOM = 100.0, 100.0

        # Create a mock fiber cell
        fiber_cell = MagicMock()
        fiber_cell.type = self.steppable.ECMFIBER

        # Place it within the neighborhood (dx=3, dy=-2)
        self.steppable.cell_field[103, 98, 0] = fiber_cell

        self.assertTrue(self.steppable.check_simple_fiber_contact(cell))

    def test_check_simple_fiber_contact_out_of_bounds(self):
        """Test simple fiber contact check at boundary"""
        cell = MagicMock()
        cell.xCOM, cell.yCOM = 0.0, 0.0

        # Negative indices will be skipped by 0 <= nx < self.dim.x
        # Put a fiber at (1, 1) and make sure it finds it even at the boundary
        fiber_cell = MagicMock()
        fiber_cell.type = self.steppable.ECMFIBER
        self.steppable.cell_field[1, 1, 0] = fiber_cell

        self.assertTrue(self.steppable.check_simple_fiber_contact(cell))

    def test_check_simple_fiber_contact_exception(self):
        """Test simple fiber contact check handles exceptions"""
        cell = MagicMock()
        # Make xCOM throw a ValueError by giving it a string
        cell.xCOM = "not_a_number"
        cell.yCOM = 100.0

        self.assertFalse(self.steppable.check_simple_fiber_contact(cell))


if __name__ == '__main__':
    unittest.main()
