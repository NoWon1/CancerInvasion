## 2024-08-09 - Fix Bare Except DoS
**Vulnerability:** Bare except statements in spatial loops catching critical system signals (like KeyboardInterrupt/SystemExit).
**Learning:** In Python scripts for CompuCell3D, replacing bare `except:` with `except Exception:` prevents localized Denial of Service (DoS) and reliability risks by ensuring critical system-level signals propagate correctly.
**Prevention:** Ensure `Exception` is explicitly caught instead of bare `except:` to prevent swallowing system signals.
