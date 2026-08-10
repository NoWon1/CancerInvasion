## 2026-08-10 - Prevent System Signal Swallowing in SWIG Loops
**Vulnerability:** Bare except blocks inside tightly nested spatial loops swallow system signals (KeyboardInterrupt/SystemExit) leading to potential localized DoS.
**Learning:** In CompuCell3D, out-of-bounds SWIG object lookups throw exceptions, and developers use bare excepts to handle them quickly, unintentionally silencing critical signals.
**Prevention:** Use `except Exception:` instead to catch only non-system-exiting exceptions, maintaining reliability while allowing the application to be safely terminated.
