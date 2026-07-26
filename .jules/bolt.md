## 2024-05-24 - CompuCell3D SWIG Exception Overhead in Spatial Loops
**Learning:** Out-of-bounds SWIG object lookups (e.g., `self.cell_field[x, y, 0]`) throw exceptions that incur significant performance overhead inside tightly nested spatial loops. Using `try...except` to catch these exceptions is slow.
**Action:** Use explicit, dynamic boundary checks (e.g., `0 <= x < self.dim.x` and `0 <= y < self.dim.y`) before accessing arrays to prevent SWIG exceptions, rather than relying on `try...except`.
