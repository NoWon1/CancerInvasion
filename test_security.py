import ast
import os

def test_no_bare_excepts():
    filepath = "Simulation/CancerInvasionSteppables.py"
    with open(filepath, "r") as f:
        source_code = f.read()

    tree = ast.parse(source_code)
    bare_excepts_found = False

    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler):
            if node.type is None:
                bare_excepts_found = True
                print(f"Bare except found at line {node.lineno}")

    assert not bare_excepts_found, "Bare excepts are not allowed due to security/reliability risks."
