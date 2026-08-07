import ast

def test_no_bare_except():
    with open("Simulation/CancerInvasionSteppables.py", "r") as f:
        tree = ast.parse(f.read())

    bare_excepts = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler):
            if node.type is None:
                bare_excepts.append(node.lineno)

    assert len(bare_excepts) == 0, f"Found bare except blocks at lines {bare_excepts}"
