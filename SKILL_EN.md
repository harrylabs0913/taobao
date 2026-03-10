---
name: taobao
description: "CLI tool for Taobao e-commerce platform - search products, track prices, and manage authentication"
---

# Taobao Skill

A command-line interface for Taobao (淘宝), China's largest C2C e-commerce platform. This skill provides comprehensive access to product search, price history tracking, and authentication management.

## Description

Taobao is a powerful CLI tool designed for interacting with the Taobao e-commerce ecosystem. It enables automated product searches with intelligent caching, detailed price history analysis, and secure QR code-based authentication. The platform offers an enormous selection of products from millions of merchants, making it ideal for price research, product discovery, and competitive analysis.

### Use Cases

- **Product Discovery**: Find products across Taobao's vast marketplace
- **Price Analysis**: Track historical pricing to identify buying opportunities
- **Seller Research**: Analyze seller ratings and sales data
- **Market Intelligence**: Gather competitive pricing information

## Installation

```bash
# Install the ecommerce-core dependency first
pip install -r ../ecommerce-core/requirements.txt

# Install the Taobao skill
pip install -e .
```

## Usage

### Commands

#### Search Products
```bash
taobao search "运动鞋"
taobao search "iPhone" --page 2 --limit 20
```

Search for products by keyword with pagination support.

- **Arguments:**
  - `query` - Search keyword (required)
  - `--page` - Page number (default: 1)
  - `--limit` - Number of results per page (default: 20)

**Example:**
```bash
# Basic search
taobao search "wireless earbuds"

# Paginated search
taobao search "coffee maker" --page 5 --limit 30
```

#### Login
```bash
taobao login
```

Authenticate with Taobao using QR code. Opens a browser window with a QR code that can be scanned with the Taobao/Alipay mobile app. Session tokens are securely stored for future use.

#### Price History
```bash
taobao history <product-url>
```

Display current price and historical price data for a specific product.

- **Arguments:**
  - `product-url` - Full Taobao product URL (required)

**Example:**
```bash
taobao history "https://item.taobao.com/item.htm?id=123456789"
```

## Features

- **Product Search with Caching**: Intelligent caching system for fast repeated searches and reduced API load
- **QR Code Login**: Secure and convenient authentication via mobile app QR code scanning
- **Price History Tracking**: Comprehensive historical price data to identify trends and optimal purchase timing
- **Anti-Detection Browser Automation**: Stealth automation that mimics human interaction patterns
- **Session Persistence**: Long-lived authentication tokens for uninterrupted access

## Examples

### Product Search
```bash
# Search for electronics
taobao search "iPhone 15 Pro"

# Search with custom results
taobao search "running shoes" --page 2 --limit 50
```

### Price Analysis
```bash
# Get price history
taobao history "https://item.taobao.com/item.htm?id=687543210"

# Check historical low price
taobao history "https://item.taobao.com/item.htm?id=123456" | grep -i "lowest"
```

### Authentication Setup
```bash
# First-time login
taobao login
# Scan QR code with Taobao app
```

## Technical Details

### Data Storage

| Data Type | Location |
|-----------|----------|
| Session Tokens | `~/.openclaw/data/ecommerce/auth.db` |
| Search Cache | `~/.openclaw/data/ecommerce/ecommerce.db` |

### Dependencies

- `ecommerce-core` framework (required)
- Browser automation with anti-detection capabilities
- SQLite for data persistence

### Platform Notes

Taobao operates as a C2C (Consumer-to-Consumer) platform with:
- Millions of individual sellers
- Diverse product categories
- Competitive pricing through negotiation
- Integrated with Alipay for payments

### Anti-Detection Implementation

All browser automation includes:
- Randomized timing between actions
- Human-like mouse movements and clicks
- Realistic navigation patterns
- Session fingerprint management