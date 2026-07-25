## Description: <br>
Taobao Shopping helps an agent evaluate public Taobao listings, sellers, SKUs, reviews, visible prices, promotions, return protections, and buy/wait/avoid decisions. Login, account pages, cookies, cart changes, coupon claiming, checkout, order submission, and payment remain user-controlled. <br>

This skill is intended for public research and pre-purchase decision support. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>

## Use Case: <br>
Users and shopping assistants use this skill to research Taobao products from public listing evidence, compare seller and SKU risks, and produce a manual pre-purchase checklist. It does not change account state or complete transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Final price, coupon eligibility, SKU availability, delivery, or returns may depend on private account or checkout-only conditions. <br>
Mitigation: Use visible evidence only and require the user to manually verify the selected SKU, final payable amount, delivery, stock, return policy, invoice, warranty, and payment. <br>
Risk: Seller or review signals may be incomplete or misleading. <br>
Mitigation: Present evidence and uncertainty separately; do not treat low price, store type, sales, or reviews as proof of authenticity or value. <br>

## Reference(s): <br>
- [Taobao Shopping ClawHub listing](https://clawhub.ai/harrylabsj/skills/taobao-shopping) <br>
- [Browser Workflow](artifact/references/browser-workflow.md) <br>
- [Marketplace Guide](artifact/references/marketplace-guide.md) <br>
- [Output Patterns](artifact/references/output-patterns.md) <br>

## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, analysis] <br>
**Output Format:** [Markdown with verdict, evidence, risk, and final-check sections] <br>
**Other Properties Related to Output:** [Uses public-visible Taobao evidence and hands off account-state, checkout, and payment steps to the user.] <br>

## Skill Version(s): <br>
2.1.3 (source: GitHub release branch) <br>

## Ethical Considerations: <br>
Users should review the evidence and generated recommendations before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
