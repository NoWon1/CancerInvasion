import ast
import os

def test_no_bare_except():
    # Read the target file
    filepath = os.path.join("Simulation", "CancerInvasionSteppables.py")
    with open(filepath, "r", encoding="utf-8") as file:
        source_code = file.read()

    # Parse the source code into an AST
    tree = ast.parse(source_code, filename=filepath)

    # Walk the AST to find ExceptHandler nodes
    bare_excepts = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler):
            # A bare 'except:' has node.type as None
            if node.type is None:
                bare_excepts.append(node.lineno)

    # Assert that no bare excepts were found
    assert len(bare_excepts) == 0, f"Bare 'except:' found at lines: {bare_excepts}. Use 'except Exception:' instead to avoid catching system exceptions like KeyboardInterrupt."
