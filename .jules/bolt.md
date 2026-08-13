## 2024-08-13 - [SWIG Exception Overhead in CC3D Spatial Loops]
**Learning:** In CompuCell3D (CC3D) Python scripts, using try...except blocks inside tightly nested spatial loops for field accesses (like self.cell_field) incurs significant overhead because out-of-bounds SWIG object lookups throw expensive exceptions.
**Action:** Always use explicit boundary checks (e.g., comparing against self.dim.x and self.dim.y) before accessing arrays instead of relying on try-except blocks for boundary handling.
