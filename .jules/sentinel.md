## 2024-05-15 - Prevent Localized DoS via Bare Excepts
**Vulnerability:** Bare `except:` blocks within nested loops swallow all system-level exceptions, including `KeyboardInterrupt` and `SystemExit`.
**Learning:** In long-running simulation loops, swallowing `KeyboardInterrupt` prevents graceful termination, leading to a localized Denial of Service and making debugging nearly impossible when errors occur deep within spatial lookups.
**Prevention:** Always use `except Exception:` instead of bare `except:` to only catch standard program errors while allowing critical system signals to propagate to the Python runtime.
