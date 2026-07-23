## 2026-07-23 - CompuCell3D SWIG Exception Overhead in Spatial Loops
**Learning:** In CompuCell3D (CC3D) Python scripts, out-of-bounds SWIG object lookups (like `self.cell_field[x, y, 0]`) throw exceptions that incur significant overhead, especially when caught by `try...except` blocks inside tightly nested spatial loops.
**Action:** Avoid using `try...except` blocks for field accesses inside spatial loops. Instead, use explicit boundary checks (e.g., `min()`, `max()`) prior to looping to prevent out-of-bounds SWIG lookups entirely, which can lead to ~2.7x speedups.
