## 2026-07-16 - Prevent Exception Masking
**Vulnerability:** Masking base exceptions with bare except blocks
**Learning:** Python bare `except:` blocks catch `BaseException`, including `SystemExit`, `KeyboardInterrupt`, and `GeneratorExit`. Swallowing these system-level exceptions can prevent an application from shutting down gracefully or responding to termination signals, which represents an operational risk and a potential localized Denial of Service (DoS) vector.
**Prevention:** Always restrict exception handling to `except Exception:` unless specifically handling base signals, ensuring system processes can still terminate safely.
