🎯 **What:** Abstract field access try-except blocks into a context manager
Created a `safe_field_access` context manager to abstract out repetitive `try... except (IndexError, KeyError): continue` blocks around grid field access throughout `Simulation/CancerInvasionSteppables.py`.

💡 **Why:** How this improves maintainability
This reduces duplicated exception-handling logic, making it cleaner and easier to read when bounds checking is being explicitly ignored during field access.

✅ **Verification:** How you confirmed the change is safe
Ran `pytest tests/` ensuring all tests including `test_create_simple_fiber_exception_handling` passed correctly. Checked the output against flake8 and visually verified that the new `with self.safe_field_access():` properly replicates the intent of the old code by silencing field indexing errors.

✨ **Result:** The improvement achieved
Successfully removed six duplicated try-except error catching structures across the `CancerInvasionSteppable` class logic.
