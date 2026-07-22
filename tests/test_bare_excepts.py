import ast

def test_no_bare_excepts():
    with open("Simulation/CancerInvasionSteppables.py", "r") as f:
        code = f.read()

    tree = ast.parse(code)
    bare_excepts = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler):
            if node.type is None:
                bare_excepts.append(node)

    assert len(bare_excepts) == 0, f"Found {len(bare_excepts)} bare except block(s)."
