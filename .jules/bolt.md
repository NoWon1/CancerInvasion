## 2026-08-14 - Optimize CC3D SWIG Spatial Array Lookups
**Learning:** SWIG object boundary exceptions in CompuCell3D (like out-of-bounds self.cell_field accesses) incur significant overhead within tightly nested spatial loops. Relying on try-except blocks instead of explicit boundary checks degrades performance.
**Action:** Use explicit boundary checks (e.g., 0 <= x < self.dim.x) prior to accessing CC3D arrays to prevent SWIG lookup exceptions and improve speed.
