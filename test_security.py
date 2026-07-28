import ast
import os

def test_no_bare_excepts():
    filepath = "Simulation/CancerInvasionSteppables.py"
    with open(filepath, "r") as f:
        source_code = f.read()

    tree = ast.parse(source_code)
    bare_excepts = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler):
            if node.type is None:
                bare_excepts.append(node.lineno)

    assert not bare_excepts, f"Found bare 'except:' statements at lines: {bare_excepts}. Use 'except Exception:' instead."
