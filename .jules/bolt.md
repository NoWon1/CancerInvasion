## 2026-08-14 - Optimize CC3D SWIG Spatial Array Lookups
**Learning:** SWIG object boundary exceptions in CompuCell3D (like out-of-bounds self.cell_field accesses) incur significant overhead within tightly nested spatial loops. Relying on try-except blocks instead of explicit boundary checks degrades performance.
**Action:** Use explicit boundary checks (e.g., 0 <= x < self.dim.x) prior to accessing CC3D arrays to prevent SWIG lookup exceptions and improve speed.
## 2026-08-22 - Pre-calculated boundaries for nested spatial loops
**Learning:** Redundant boundary checks inside tightly nested spatial loops incur significant overhead in CC3D Python scripts.
**Action:** Pre-calculate strict min/max boundaries for the loop's range() generators before entering the loop to skip out-of-bounds iterations and eliminate redundant conditional evaluations, while keeping the try...except wrappers for defensive programming.
