## 2024-05-24 - CC3D SWIG Exception Overhead in Spatial Loops
**Learning:** In CompuCell3D (CC3D) scripts, accessing fields out-of-bounds throws SWIG object exceptions. Catching these with `try...except` inside tightly nested spatial loops incurs massive performance overhead compared to explicit integer boundary checks.
**Action:** Always use explicit boundary checks (e.g., `0 <= x < self.dim.x`) instead of `try...except` for CC3D field accesses like `self.cell_field` or `self.field.MMP`.
