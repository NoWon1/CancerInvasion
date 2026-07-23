import ast
import os

def test_no_bare_excepts():
    filepath = os.path.join(os.path.dirname(__file__), 'Simulation', 'CancerInvasionSteppables.py')
    with open(filepath, 'r') as f:
        tree = ast.parse(f.read(), filename=filepath)

    bare_excepts = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler):
            if node.type is None:
                bare_excepts.append(node.lineno)

    assert len(bare_excepts) == 0, f"Found bare except blocks at lines: {bare_excepts}"
