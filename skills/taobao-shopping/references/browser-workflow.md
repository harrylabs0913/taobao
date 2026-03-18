# Browser Workflow for Taobao Shopping

This document describes the browser automation workflow for Taobao shopping operations.

## Overview

Taobao browser automation follows a phased approach with clear boundaries between agent-assisted operations and user-controlled checkout.

## Authentication Requirements

| Operation | Login Required | Notes |
|-----------|----------------|-------|
| Search | No | Public search results |
| Browse categories | No | Public category pages |
| View product details | No | Public product pages |
| Read reviews | No | Public review data |
| Compare prices | No | Public price information |
| Add to cart | Yes | Requires active session |
| View cart | Yes | Requires active session |
| Apply coupons | Yes | Requires active session |
| Generate order preview | Yes | Requires active session |
| Payment | Blocked | User only |

## Browser Extraction Order

When extracting data from Taobao pages, follow this priority:

1. **商品标题** - Product title
2. **价格信息** - 原价, 券后价, 到手价
3. **店铺类型** - 天猫/企业店/个人店
4. **店铺评分** - 描述相符, 服务态度, 物流服务
5. **销量** - 月销/总销量
6. **优惠券** - 店铺券, 平台券
7. **满减活动** - 满X减Y
8. **规格选项** - 颜色, 尺寸, 版本
9. **用户评价** - 好评率, 追评, 晒图
10. **物流信息** - 发货地, 运费, 预计送达

## Workflow Phases

### Phase 1: Discovery

**Actions:**
- Navigate to taobao.com
- Enter search query
- Apply filters (price, rating, brand)
- Sort results (sales, price, rating)
- Extract top 3-5 product summaries

**Key Data Points:**
- Product title
- Main image
- Price range
- Sales volume
- Store type badge
- Rating score

### Phase 2: Selection

**Actions:**
- Open selected product page
- Extract detailed specifications
- Read user reviews (first 10-20)
- Check variant options
- Verify seller information

**Key Data Points:**
- Full product description
- All available variants
- Detailed pricing (with coupons)
- Store rating breakdown
- Return policy
- Shipping cost

### Phase 3: Cart & Pre-Order

**Actions:**
- Confirm login status
- Select product variant
- Add to cart
- Navigate to cart page
- Review cart contents
- Check available coupons
- Select delivery address
- Calculate final price

**Key Data Points:**
- Cart subtotal
- Applied coupons
- Shipping fee
- Final price
- Delivery address
- Estimated delivery date

### Phase 4: Checkout Handoff

**Actions:**
- Present complete order summary
- Stop before payment screen
- Provide manual checkout instructions

**Never:**
- Enter payment information
- Click final submit button
- Complete transaction

## Error Handling

### CAPTCHA
When CAPTCHA appears:
1. Stop automation
2. Notify user
3. Provide manual instructions

### Login Required
When login is required:
1. Ask user for confirmation
2. Provide login options
3. Never ask for password in chat

### Price Mismatch
When displayed price differs from expected:
1. Flag the discrepancy
2. Re-extract pricing
3. Confirm with user before proceeding

### Out of Stock
When selected variant is out of stock:
1. Notify user
2. Show available alternatives
3. Wait for user selection

## Security Guidelines

1. **Never store credentials**
2. **Never complete payment**
3. **Always ask before login-required actions**
4. **Snapshot key data for verification**
5. **Provide clear handoff instructions**

## Example Session

```
User: 帮我买蓝牙耳机

Agent: 
1. Searches "蓝牙耳机 天猫" on Taobao
2. Filters by Tmall stores, sorts by sales
3. Extracts top 3 options with prices
4. Presents comparison table

User: 选第二个

Agent:
1. Opens product detail page
2. Extracts specifications and reviews
3. Shows variant options (color, model)
4. Calculates final price with coupons

User: 买白色的

Agent:
1. "需要登录淘宝账号才能加入购物车，是否继续？"

User: 好的

Agent:
1. Checks login status
2. Selects white variant
3. Adds to cart
4. Applies available coupons
5. Generates order preview
6. "订单已准备好，请手动完成支付..."
```

## Related Files

- `marketplace-guide.md` - Taobao marketplace characteristics
- `output-patterns.md` - Response formatting guidelines
