## 2024-07-26 - Fix Bare Exceptions
**Vulnerability:** Bare except blocks
**Learning:** Bare exceptions inside spatial loops swallow critical system signals
**Prevention:** Catch Exception specifically instead of using bare except:
