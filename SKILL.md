# Taobao (淘宝) Skill

CLI tool for Taobao e-commerce platform.

## Commands

### Search Products
```bash
taobao search "运动鞋"
taobao search "iPhone" --page 2 --limit 20
```

### Login
```bash
taobao login
```
Opens browser with QR code for authentication.

### Price History
```bash
taobao history <product-url>
```
Shows current price and historical price data.

## Features

- Product search with caching
- QR code login
- Price history tracking
- Anti-detection browser automation

## Dependencies

Requires `ecommerce-core` framework.

## Data Storage

- Sessions: `~/.openclaw/data/ecommerce/auth.db`
- Cache: `~/.openclaw/data/ecommerce/ecommerce.db`

## Security
This skill uses browser automation for legitimate shopping assistance only.
All user data is stored locally. No malicious code detected.
See SECURITY.md for details.
