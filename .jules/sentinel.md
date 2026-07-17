## 2023-10-24 - Bare except block DoS risk
**Vulnerability:** Bare `except:` blocks catching `BaseException`.
**Learning:** Bare `except:` clauses can catch `SystemExit` and `KeyboardInterrupt`, preventing graceful shutdown and creating potential denial-of-service (DoS) conditions in long-running simulation components.
**Prevention:** Always use `except Exception:` to only catch application-level errors and allow critical system signals to propagate.
