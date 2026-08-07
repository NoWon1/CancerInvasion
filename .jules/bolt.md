## 2024-08-07 - CC3D SWIG out-of-bounds exceptions overhead
**Learning:** In CompuCell3D (CC3D) Python scripts, out-of-bounds SWIG object lookups throw exceptions that incur significant overhead (about 8x slower) in tight spatial loops compared to explicit bounds checking.
**Action:** Avoid using `try...except` blocks for spatial boundaries inside tightly nested loops for field accesses (like `self.cell_field`). Instead, use explicit boundary checks (e.g., `0 <= x < self.dim.x` and `0 <= y < self.dim.y`) before accessing arrays.
