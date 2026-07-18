## 2024-05-18 - Optimize CC3D SWIG Array Lookups
**Learning:** In CompuCell3D (CC3D) Python scripts, using `try...except` blocks inside tightly nested spatial loops for field accesses (like `self.cell_field`) incurs significant overhead. Out-of-bounds SWIG object lookups throw exceptions that are costly to handle inside hot loops.
**Action:** Replace bare `except:` blocks around array accesses in spatial loops with explicit boundary checks (e.g., `0 <= x < self.dim.x`) before accessing arrays to significantly improve performance.
