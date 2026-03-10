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

- Python 3.9+
- `playwright>=1.40.0` (浏览器自动化)
- `cryptography>=42.0.0` (加密库)
- 安装命令: `pip install -r requirements.txt`

## 数据存储与安全

### 存储位置
- **主目录**: `~/.openclaw/data/taobao/` (加密存储)
- **会话数据**: `cookies.enc` (AES-256 加密存储)
- **缓存数据**: `taobao.db` (SQLite数据库)
- **加密密钥**: `.key` (权限 600)

### 隐私保护
1. **加密存储**: 所有敏感数据使用 Fernet 加密
2. **用户同意**: 首次运行需要明确同意数据使用条款
3. **数据控制**: 支持一键清除所有个人数据
4. **透明审计**: 可查看所有存储的文件和权限

### 隐私控制命令
```bash
# 查看隐私信息
taobao privacy info

# 清除所有个人数据
taobao privacy clear

# 导出加密数据（备份）
taobao privacy export
```

## Security
This skill uses browser automation for legitimate shopping assistance only.
All user data is encrypted and stored locally. No data transmission to external servers.
See SECURITY.md for details.
