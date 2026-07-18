import sys
import ast
from unittest.mock import MagicMock

# Mock cc3d dependencies
sys.modules['cc3d'] = MagicMock()
sys.modules['cc3d.core'] = MagicMock()
sys.modules['cc3d.core.PySteppables'] = MagicMock()

import builtins
class MockSteppableBasePy:
    def __init__(self, frequency=1):
        self.frequency = frequency

builtins.SteppableBasePy = MockSteppableBasePy

def test_no_bare_except():
    with open("Simulation/CancerInvasionSteppables.py", "r") as f:
        content = f.read()

    tree = ast.parse(content)
    bare_excepts = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler):
            if node.type is None:
                bare_excepts.append(node.lineno)

    assert len(bare_excepts) == 0, f"Found bare except blocks at lines: {bare_excepts}"
