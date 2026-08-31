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


if __name__ == '__main__':
    unittest.main()
