## 2026-08-14 - Optimize CC3D SWIG Spatial Array Lookups
**Learning:** SWIG object boundary exceptions in CompuCell3D (like out-of-bounds self.cell_field accesses) incur significant overhead within tightly nested spatial loops. Relying on try-except blocks instead of explicit boundary checks degrades performance.
**Action:** Use explicit boundary checks (e.g., 0 <= x < self.dim.x) prior to accessing CC3D arrays to prevent SWIG lookup exceptions and improve speed.
## 2026-08-25 - Pre-calculate nested loop bounds
**Learning:** In nested spatial loops within CompuCell3D steppables, passing expressions (like `int(cell.yCOM)`) into the inner loop's `range()` causes redundant re-evaluation. Including `if 0 <= x < dim.x` boundary checks inside the loop also adds overhead.
**Action:** Pre-calculate strict `min()` and `max()` bounds before entering the outer loop and use those for the `range()` generators to eliminate redundant evaluations and inner boundary checks.
