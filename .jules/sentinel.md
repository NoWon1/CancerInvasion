## 2024-07-15 - [Medium] Swallowing System Exceptions in Simulation
**Vulnerability:** Bare `except:` blocks within tight simulation loops (e.g. `CancerInvasionSteppables.py`)
**Learning:** Simulation models sometimes use bare `except:` to swallow errors from spatial/SWIG out-of-bounds errors to prevent simulation crashes, but this hides critical system exceptions like `KeyboardInterrupt` or `SystemExit`, creating a DoS risk if the program cannot be cleanly exited.
**Prevention:** Always use `except Exception:` instead of bare `except:` to ensure `BaseException` variants correctly propagate to the OS.
