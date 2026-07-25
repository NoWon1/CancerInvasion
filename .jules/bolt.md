## 2025-07-25 - SWIG Exception Overhead in CC3D Spatial Loops
**Learning:** Out-of-bounds SWIG object lookups throw exceptions that incur significant overhead. Using `try...except` blocks inside tightly nested spatial loops for field accesses (like `self.cell_field`) hides these exceptions but still incurs the performance penalty of exception handling on every iteration.
**Action:** Use explicit boundary checks (e.g., `0 <= x < self.dim.x`) before accessing SWIG arrays and completely remove the `try...except` blocks inside spatial loops to prevent the overhead.
