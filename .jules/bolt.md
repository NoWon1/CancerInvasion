## 2024-08-09 - Avoid try-except in CC3D spatial loops
**Learning:** In CompuCell3D, out-of-bounds SWIG object lookups throw exceptions that incur significant overhead when caught in tightly nested spatial loops.
**Action:** Use explicit boundary checks (e.g., using `self.dim.x` and `self.dim.y`) before accessing arrays instead of try-except blocks.
