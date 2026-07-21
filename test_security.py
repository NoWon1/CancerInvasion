import ast
import os
import unittest

class TestSecurity(unittest.TestCase):
    def test_no_bare_exceptions(self):
        """
        Verify that there are no bare 'except:' clauses in the simulation scripts.
        Bare exceptions can swallow critical system signals like KeyboardInterrupt or SystemExit,
        leading to localized Denial of Service (DoS) and reliability risks.
        """
        filepath = os.path.join(os.path.dirname(__file__), 'Simulation', 'CancerInvasionSteppables.py')
        with open(filepath, 'r') as f:
            source = f.read()

        tree = ast.parse(source)

        bare_exceptions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    bare_exceptions.append(node.lineno)

        self.assertEqual(len(bare_exceptions), 0, f"Bare exceptions found at lines: {bare_exceptions}")

if __name__ == '__main__':
    unittest.main()
