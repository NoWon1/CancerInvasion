## 2024-07-24 - Avoid Bare Except Blocks in CC3D
**Vulnerability:** Bare `except:` blocks within tight spatial loops (e.g., catching errors from out-of-bounds SWIG object lookups) swallow BaseException, dropping critical system-level signals like KeyboardInterrupt or SystemExit, which poses a localized Denial of Service (DoS) and reliability risk.
**Learning:** In scientific simulations like CompuCell3D where exceptions might be used for boundary checks, it's critical to ensure system signals propagate to allow graceful shutdowns.
**Prevention:** Always use `except Exception:` instead of bare `except:` to only catch standard exceptions.
