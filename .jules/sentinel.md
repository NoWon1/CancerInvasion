## 2024-05-24 - Fix Bare Except DoS Risk
**Vulnerability:** Bare except blocks in spatial loops.
**Learning:** Bare excepts swallow system-level exceptions like KeyboardInterrupt and SystemExit, posing a localized DoS risk.
**Prevention:** Always specify exception types such as Exception when using try-except blocks.
## 2024-05-24 - Fix Hardcoded Grid Dimensions
**Vulnerability:** Hardcoded lattice dimensions (e.g., `500`) in spatial boundary checks in CompuCell3D simulation scripts.
**Learning:** Hardcoding grid bounds can lead to `IndexError` exceptions and application crashes (localized DoS) if the simulation size is changed dynamically or externally, breaking simulation robustness.
**Prevention:** Always use dynamic dimension attributes like `self.dim.x` and `self.dim.y` (provided by `SteppableBasePy`) to validate spatial bounds.
