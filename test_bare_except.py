import ast

def test_no_bare_excepts():
    with open('Simulation/CancerInvasionSteppables.py', 'r') as f:
        tree = ast.parse(f.read())

    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler):
            assert node.type is not None, "Found a bare except! Use 'except Exception:' instead."
