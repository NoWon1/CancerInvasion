import ast
import os

def test_no_bare_excepts():
    filepath = os.path.join(os.path.dirname(__file__), '..', 'Simulation', 'CancerInvasionSteppables.py')
    with open(filepath, 'r') as f:
        tree = ast.parse(f.read())

    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler):
            assert node.type is not None, f"Found bare except at line {node.lineno}"
