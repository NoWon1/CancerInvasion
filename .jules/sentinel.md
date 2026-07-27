## 2024-07-27 - Bare Except Blocks in CC3D Spatial Loops
**Vulnerability:** Bare `except:` blocks were catching and swallowing all exceptions, including critical system-level signals like `KeyboardInterrupt` and `SystemExit`, causing potential localized Denial of Service (DoS) and application unresponsiveness.
**Learning:** In CompuCell3D (CC3D) simulation scripts, bare `except:` blocks inside tightly nested spatial loops or heavily accessed functions can lead to unresponsive environments and swallow fatal errors that should crash the program.
**Prevention:** Always use `except Exception:` to catch standard application errors without interfering with critical system signals.
