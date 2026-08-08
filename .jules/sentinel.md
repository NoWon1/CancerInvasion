## 2026-08-08 - Prevent DoS from Bare Excepts
**Vulnerability:** Bare except blocks (`except:`) catch system-level exceptions like KeyboardInterrupt or SystemExit, potentially causing a Denial of Service and making the script unkillable.
**Learning:** In Python, it is a security and reliability risk to catch all exceptions indiscriminately.
**Prevention:** Always use `except Exception:` to only catch application-level errors and allow system signals to propagate.
