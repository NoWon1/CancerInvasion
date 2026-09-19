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
## 2026-09-11 - Fast single-target population loops
**Learning:** Iterating over an entire cell population to find a single target (like a cell ready for mitosis when only one divides per step) wastes O(N) evaluations of cell properties.
**Action:** Add an early `break` as soon as the target cell is found to prevent unnecessary SWIG overhead for the remaining cells.
## 2024-09-14 - Caching SWIG properties in nested loops
**Learning:** Redundant SWIG property lookups (like self.ECMFIBER) inside tight spatial loops are computationally expensive in CompuCell3D.
**Action:** Cache these properties in local variables before entering nested loops to eliminate redundant evaluations.
## 2026-10-24 - Pre-calculate nested spatial loops bounds in CC3D
**Learning:** In Python nested loops (like spatial loops in CompuCell3D), passing complex expressions or SWIG boundaries directly into an inner loop's `range()` definition or conditionally checking them inside the innermost loop body causes them to be repeatedly evaluated for every iteration of the outer loop.
**Action:** When a bounding box is known relative to a central coordinate, use `min` and `max` with grid dimensions *outside* the loop to strictly bound the `range()` generators, completely eliminating conditionally evaluated boundary checks inside the innermost loop body. Cache these dimensions as local variables prior to entering the loop.
## 2026-12-08 - Cache SWIG properties in hot iteration functions in CC3D
**Learning:** Accessing SWIG boundary properties (like `self.dim` or `self.field`) directly inside per-cell calculations incurring hot loop traversals (like chemotaxis) imposes high overhead due to repeated boundary crossings.
**Action:** Cache these properties as local variables once per simulation step in the main outer loop and pass them as arguments to per-cell helper functions, completely eliminating redundant SWIG evaluations per cell.
