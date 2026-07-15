## 2024-05-24 - CompuCell3D Field Access Overhead
**Learning:** In CompuCell3D Python scripts, accessing SWIG C++ objects like `cell_field[x, y, 0]` with a `try...except` block in a tight inner loop causes massive overhead because when it throws (e.g. out of bounds), Python and SWIG exception handling dominates CPU time.
**Action:** Always pre-calculate exact boundary limits (`min`/`max`) outside tight loops to avoid out-of-bounds exceptions entirely, and remove the `try...except` from the inner pixel-iteration loops.
