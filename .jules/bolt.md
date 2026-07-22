## 2024-05-23 - Avoid try/except in CC3D spatial loops
**Learning:** Out-of-bounds SWIG object lookups in CompuCell3D throw exceptions that incur significant overhead when caught by `try...except` blocks in tightly nested spatial loops.
**Action:** Use explicit boundary checks (e.g., `0 <= x < self.dim.x`) before accessing CC3D fields to prevent out-of-bounds exceptions and improve performance.
