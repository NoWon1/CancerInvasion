## 2026-08-14 - Optimize CC3D SWIG Spatial Array Lookups
**Learning:** SWIG object boundary exceptions in CompuCell3D (like out-of-bounds self.cell_field accesses) incur significant overhead within tightly nested spatial loops. Relying on try-except blocks instead of explicit boundary checks degrades performance.
**Action:** Use explicit boundary checks (e.g., 0 <= x < self.dim.x) prior to accessing CC3D arrays to prevent SWIG lookup exceptions and improve speed.
## 2026-08-30 - Pre-calculate nested spatial loops bounds in CC3D
**Learning:** Checking boundary conditions (e.g., `0 <= x < self.dim.x`) during *every single iteration* inside tightly nested loops degrades performance in operations executed frequently per MCS (like cell removals or checking neighborhood contacts).
**Action:** When a bounding box is known relative to a central coordinate, use `min` and `max` with grid dimensions *outside* the loop to strictly bound the `range()` generators, completely eliminating conditionally evaluated boundary checks inside the innermost loop body.
