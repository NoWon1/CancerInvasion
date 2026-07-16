## 2024-05-18 - Avoid try...except blocks in CC3D spatial loops
**Learning:** In CompuCell3D (CC3D) Python scripts, avoiding `try...except` blocks inside tightly nested spatial loops for field accesses (like `self.cell_field`) is critical for performance. Out-of-bounds SWIG object lookups throw exceptions that incur significant overhead.
**Action:** Use explicit boundary checks (e.g., `min()`, `max()`) before accessing arrays instead of relying on `try...except` to catch out-of-bounds access.
