## 2024-07-23 - Prevent Localized DoS from Bare Excepts
**Vulnerability:** Bare except blocks swallow system signals like KeyboardInterrupt.
**Learning:** SWIG object lookups in CompuCell3D fail often and bare excepts were used for error handling but caused DoS risks.
**Prevention:** Use except Exception: instead.
