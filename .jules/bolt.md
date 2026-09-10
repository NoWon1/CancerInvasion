## 2026-08-14 - Optimize CC3D SWIG Spatial Array Lookups
**Learning:** SWIG object boundary exceptions in CompuCell3D (like out-of-bounds self.cell_field accesses) incur significant overhead within tightly nested spatial loops. Relying on try-except blocks instead of explicit boundary checks degrades performance.
**Action:** Use explicit boundary checks (e.g., 0 <= x < self.dim.x) prior to accessing CC3D arrays to prevent SWIG lookup exceptions and improve speed.
## 2026-08-30 - Pre-calculate nested spatial loops bounds in CC3D
**Learning:** Checking boundary conditions (e.g., `0 <= x < self.dim.x`) during *every single iteration* inside tightly nested loops degrades performance in operations executed frequently per MCS (like cell removals or checking neighborhood contacts).
**Action:** When a bounding box is known relative to a central coordinate, use `min` and `max` with grid dimensions *outside* the loop to strictly bound the `range()` generators, completely eliminating conditionally evaluated boundary checks inside the innermost loop body.
## 2024-05-20 - Fast typed cell iteration in CC3D
**Learning:** Iterating over the entire cell list and performing manual type checks in Python is slow for large populations.
**Action:** Always prefer using `self.cell_list_by_type(self.CELL_TYPE)` over manual iteration when applying logic specific to a single cell type.
## 2026-09-08 - Fast CC3D neighbor iterator break
**Learning:** In CompuCell3D, breaking early from neighbor iterators (like `get_cell_neighbor_data_list`) avoids lazy SWIG instantiation of neighbor cell Python objects for the remainder of the C++ list, significantly reducing overhead in hot loops.
**Action:** Always break from CC3D neighbor iteration loops as soon as a required condition (like a contact area threshold) is met.
## 2026-09-09 - Safe Cell Removal with Pixel Lists in CC3D
**Learning:** Replacing bounding-box pixel searches with `self.get_cell_pixel_list(cell)` is a massive performance win in CC3D, but modifying the `cell_field` while directly iterating over this list invalidates the underlying C++ iterator, breaking the simulation.
**Action:** Always materialize the CC3D C++ pixel list into a Python list (e.g., `pixels = [(pt.pixel.x, pt.pixel.y, pt.pixel.z) for pt in self.get_cell_pixel_list(cell)]`) BEFORE iterating to modify the field.
## 2026-09-10 - Cache SWIG properties
**Learning:** Redundant SWIG boundary crossings (like accessing cell properties) in CC3D are computationally expensive.
**Action:** Cache these properties in local variables instead of recalculating them multiple times.
