## 2024-05-24 - Fix Bare Except DoS Risk
**Vulnerability:** Bare except blocks in spatial loops.
**Learning:** Bare excepts swallow system-level exceptions like KeyboardInterrupt and SystemExit, posing a localized DoS risk.
**Prevention:** Always specify exception types such as Exception when using try-except blocks.
