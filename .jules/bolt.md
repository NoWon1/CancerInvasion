## 2024-05-18 - CompuCell3D Field Access Exceptions
**Learning:** In CompuCell3D Python scripts, avoid using `try...except` blocks inside tightly nested spatial loops for field accesses (like `self.cell_field`). Out-of-bounds SWIG object lookups throw exceptions that incur significant overhead.
**Action:** Use explicit boundary checks (e.g., `min()`, `max()`) before accessing arrays to avoid throwing/catching exceptions.
