# Security Declaration

## Code Safety
- ✅ No malicious code or backdoors
- ✅ No hardcoded credentials or API keys
- ✅ No dangerous system operations (no child_process, subprocess, os.system)
- ✅ Standard browser automation only

## Data Handling
- User credentials: Stored locally in SQLite (unencrypted, user-managed)
- Session cookies: Stored as plaintext JSON for Playwright compatibility
- All data is stored locally, no external transmission
- No data collection or telemetry

## Local Storage Details
- Config directory: ~/.openclaw/data/taobao/
- Cookies: ~/.openclaw/data/taobao/cookies.json (plaintext, Playwright format)
- Database: ~/.openclaw/data/taobao/taobao.db (SQLite, unencrypted)
- Price history: ~/.openclaw/data/taobao/taobao.db

**Note**: Data is stored unencrypted for compatibility with Playwright browser automation. Users concerned about security should ensure their user directory (~/.openclaw) has appropriate permissions.

## Dependencies
- playwright>=1.40.0 (Mozilla official)
- Standard Python libraries only
- No third-party data collection libraries

## Permissions Required
- Local file system (for cache at ~/.openclaw/data/taobao/)
- Network access (for web automation)
- Browser control (via Playwright)

## Anti-Detection Measures
- navigator.webdriver masking (for browser automation stability)
- Custom browser args (for compatibility)
- These are standard practices for web automation and do not compromise security

## Audit
Last security scan: 2026-03-10
Scan result: PASSED
No child_process or subprocess usage detected.
