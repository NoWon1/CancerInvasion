import sys
import math
from unittest.mock import MagicMock
import pytest

# Mock CompuCell3D dependencies before importing
cc3d_mock = MagicMock()
sys.modules['cc3d'] = cc3d_mock
sys.modules['cc3d.core'] = cc3d_mock
sys.modules['cc3d.core.PySteppables'] = cc3d_mock

class DummySteppableBase:
    def __init__(self, frequency=1):
        pass

cc3d_mock.SteppableBasePy = DummySteppableBase

sys.path.append('Simulation')
from CancerInvasionSteppables import CancerInvasionSteppable

class TestCancerInvasionSteppable:
    def setup_method(self):
        self.steppable = CancerInvasionSteppable()

    def test_create_simple_fiber_happy_path(self):
        """Test basic fiber generation in the middle of the field"""
        start_x, start_y = 100, 100
        angle = 0  # Points directly along x-axis

        pixels = self.steppable.create_simple_fiber(start_x, start_y, angle)

        # Verify it returns a list
        assert isinstance(pixels, list)
        assert len(pixels) > 0

        # Base length should be self.fiber_length (18),
        # plus thickness points means length should be > 18
        assert len(pixels) > self.steppable.fiber_length

        # Verify the starting point is in the pixels
        assert (start_x, start_y) in pixels

        # Since angle=0, dx=1, dy=0, so the max x should be around start_x + fiber_length
        xs = [p[0] for p in pixels]
        ys = [p[1] for p in pixels]

        assert max(xs) >= start_x + self.steppable.fiber_length - 2 # -1 or so due to int rounding and range length

        # y values should be tight around start_y due to thickness (+1, -1)
        assert max(ys) <= start_y + 1
        assert min(ys) >= start_y - 1

    def test_create_simple_fiber_boundary_conditions(self):
        """Test fiber generation near boundaries [50, 450)"""
        angle = 0  # Points right

        # 1. Start inside, grow outside right boundary (>=450)
        # 450 is the boundary, so starting at 440 with length 18 will cross it
        pixels_right = self.steppable.create_simple_fiber(440, 100, angle)

        # Ensure no pixels have x >= 450
        assert all(p[0] < 450 for p in pixels_right)

        # 2. Start outside completely (e.g. <50)
        pixels_left = self.steppable.create_simple_fiber(40, 100, angle)

        # Since the start is 40 and it points right, some pixels might reach >= 50
        # But ensure no pixels are < 50
        assert all(p[0] >= 50 for p in pixels_left)

        # 3. Start completely out of bounds that won't ever reach inside
        pixels_far_left = self.steppable.create_simple_fiber(10, 10, math.pi) # Points further left
        assert len(pixels_far_left) == 0

    def test_create_simple_fiber_error_handling(self):
        """Test error handling when given invalid inputs"""
        # Pass string instead of float for angle to trigger TypeError in math.cos
        invalid_angle = "invalid"

        pixels = self.steppable.create_simple_fiber(100, 100, invalid_angle)

        # Should catch exception and return empty list rather than crashing
        assert isinstance(pixels, list)
        assert len(pixels) == 0
