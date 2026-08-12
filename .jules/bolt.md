## 2024-08-12 - Optimize SWIG Object Lookups
**Learning:** Out-of-bounds SWIG object lookups in CompuCell3D throw exceptions that incur significant overhead in tightly nested spatial loops.
**Action:** Use explicit dynamic boundary checks (e.g., `self.dim.x`, `self.dim.y`) instead of hardcoded sizes or try-except blocks.
