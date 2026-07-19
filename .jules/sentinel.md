## 2024-07-19 - DoS Risk in CompuCell3D Spatial Loops
**Vulnerability:** Bare `except:` blocks inside tightly nested spatial loops.
**Learning:** These can swallow critical system signals (like `KeyboardInterrupt` or `SystemExit`) making the process unkillable or causing localized DoS.
**Prevention:** Always use `except Exception:` instead of bare `except:` to ensure system-level exceptions within BaseException can propagate correctly.
