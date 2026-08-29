## 2026-08-14 - Optimize CC3D SWIG Spatial Array Lookups
**Learning:** SWIG object boundary exceptions in CompuCell3D (like out-of-bounds self.cell_field accesses) incur significant overhead within tightly nested spatial loops. Relying on try-except blocks instead of explicit boundary checks degrades performance.
**Action:** Use explicit boundary checks (e.g., 0 <= x < self.dim.x) prior to accessing CC3D arrays to prevent SWIG lookup exceptions and improve speed.

## 2026-08-29 - Pre-calculate Loop Boundaries in Spatial Loops
**Learning:** In CompuCell3D spatial loops, placing boundary checks like `min()` and `int()` directly in the inner loop's `range()` causes them to be redundantly evaluated, and inner `if` boundary checks are redundant when range limits are strictly enforced.
**Action:** Pre-calculate boundaries prior to entering the spatial loops and remove redundant `if` checks within the loop body.
