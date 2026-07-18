## 2024-07-18 - Replacing Bare Excepts in CompuCell3D Steppables
**Vulnerability:** Bare `except:` clauses were used extensively in simulation step functions and spatial loops.
**Learning:** Bare excepts catch all exceptions, including `SystemExit` and `KeyboardInterrupt`, swallowing system signals which can lead to unresponsive scripts and localized DoS conditions in simulations.
**Prevention:** Always use `except Exception:` instead of `except:` when catching generalized errors to ensure critical system exceptions propagate correctly.
