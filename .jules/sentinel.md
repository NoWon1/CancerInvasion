## 2024-05-24 - Bare except block masking system signals
**Vulnerability:** Found multiple instances of bare `except:` blocks in CompuCell3D steppables catching `BaseException`.
**Learning:** Bare `except:` blocks in Python swallow critical system-level signals like `KeyboardInterrupt` and `SystemExit`, making it impossible to gracefully terminate applications and leading to DoS risks.
**Prevention:** Always use `except Exception:` when catching general application errors to allow system signals to correctly propagate.
