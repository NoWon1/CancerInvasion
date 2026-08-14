## 2026-08-14 - Prevent Out-of-Bounds DoS Overhead
**Vulnerability:** Hardcoded grid size limits (e.g., 500) in spatial checks instead of dynamic boundaries.
**Learning:** In CC3D, out-of-bounds SWIG object lookups throw exceptions that, when caught in tight loops, incur significant overhead leading to localized DoS.
**Prevention:** Use dynamic dimensions like `self.dim.x` and `self.dim.y` for spatial checks.
