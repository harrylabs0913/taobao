#!/usr/bin/env python3
"""淘宝购物助手 - 支持搜索、历史价格、店铺评价"""

import argparse
import asyncio
import json
import os
import sqlite3
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from urllib.parse import quote, urlparse, parse_qs

try:
    from playwright.async_api import async_playwright, Page, Browser
except ImportError:
    print("请先安装依赖: pip install playwright && playwright install chromium")
    sys.exit(1)

# 配置
CONFIG_DIR = Path.home() / ".taobao"
COOKIES_FILE = CONFIG_DIR / "cookies.json"
DB_FILE = CONFIG_DIR / "taobao.db"
CONFIG_DIR.mkdir(exist_ok=True)

@dataclass
class Product:
    """商品数据类"""
    id: str
    title: str
    price: float
    original_price: Optional[float]
    shop: str
    url: str
    image: str
    location: str = ""
    sales: str = ""

@dataclass
class PricePoint:
    """价格历史点"""
    date: str
    price: float
    lowest: bool = False

class TaobaoClient:
    """淘宝客户端"""
    
    BASE_URL = "https://www.taobao.com"
    SEARCH_URL = "https://s.taobao.com/search"
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.db = self._init_db()
    
    def _init_db(self) -> sqlite3.Connection:
        """初始化SQLite数据库"""
        conn = sqlite3.connect(DB_FILE)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                title TEXT,
                price REAL,
                original_price REAL,
                shop TEXT,
                url TEXT,
                image TEXT,
                location TEXT,
                sales TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT,
                price REAL,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS shops (
                name TEXT PRIMARY KEY,
                rating REAL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        return conn
    
    async def init_browser(self, headless: bool = True):
        """初始化浏览器"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=headless,
            args=['--disable-blink-features=AutomationControlled']
        )
        context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        
        # 加载cookies
        if COOKIES_FILE.exists():
            cookies = json.loads(COOKIES_FILE.read_text())
            await context.add_cookies(cookies)
        
        self.page = await context.new_page()
        
        # 注入反检测脚本
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
    
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
    
    async def login(self):
        """扫码登录"""
        await self.init_browser(headless=False)
        
        print("正在打开淘宝登录页面...")
        await self.page.goto("https://login.taobao.com/")
        
        # 等待用户扫码登录
        print("请使用淘宝APP扫码登录...")
        try:
            await self.page.wait_for_selector(".site-nav-user", timeout=120000)
            
            # 保存cookies
            cookies = await self.page.context.cookies()
            COOKIES_FILE.write_text(json.dumps(cookies))
            print(f"登录成功！Cookies已保存到 {COOKIES_FILE}")
        except Exception as e:
            print(f"登录超时或失败: {e}")
        
        await self.close()
    
    async def search(self, keyword: str, page_num: int = 1) -> List[Product]:
        """搜索商品"""
        if not self.page:
            await self.init_browser()
        
        encoded_keyword = quote(keyword)
        url = f"{self.SEARCH_URL}?q={encoded_keyword}&s={(page_num-1)*44}"
        
        print(f"正在搜索: {keyword}")
        await self.page.goto(url, wait_until="networkidle")
        await asyncio.sleep(3)
        
        products = []
        
        try:
            # 等待商品列表加载
            await self.page.wait_for_selector(".Card--doubleCardWrapper--L2XFE73", timeout=10000)
            items = await self.page.query_selector_all(".Card--doubleCardWrapper--L2XFE73")
            
            for item in items[:20]:
                try:
                    # 提取商品信息
                    link_el = await item.query_selector("a")
                    url = await link_el.get_attribute("href") if link_el else ""
                    if url and not url.startswith("http"):
                        url = f"https:{url}"
                    
                    # 提取商品ID
                    product_id = ""
                    if "id=" in url:
                        parsed = urlparse(url)
                        product_id = parse_qs(parsed.query).get("id", [""])[0]
                    
                    title_el = await item.query_selector(".Title--title--jOqRVdF")
                    title = await title_el.inner_text() if title_el else ""
                    
                    price_el = await item.query_selector(".Price--priceInt--ZlsSi_M")
                    price_text = await price_el.inner_text() if price_el else "0"
                    
                    price_decimal_el = await item.query_selector(".Price--priceFloat--h2RR0RK")
                    price_decimal = await price_decimal_el.inner_text() if price_decimal_el else ""
                    
                    price = float(f"{price_text}{price_decimal}" or 0)
                    
                    shop_el = await item.query_selector(".ShopInfo--shopName--rg6mYQQ")
                    shop = await shop_el.inner_text() if shop_el else ""
                    
                    location_el = await item.query_selector(".Price--procity--_LJIXmq")
                    location = await location_el.inner_text() if location_el else ""
                    
                    sales_el = await item.query_selector(".Price--realSales--H1Wo9fZ")
                    sales = await sales_el.inner_text() if sales_el else ""
                    
                    img_el = await item.query_selector("img")
                    image = await img_el.get_attribute("src") if img_el else ""
                    
                    product = Product(
                        id=product_id,
                        title=title.strip(),
                        price=price,
                        original_price=None,
                        shop=shop,
                        url=url,
                        image=image if image.startswith("http") else f"https:{image}",
                        location=location,
                        sales=sales
                    )
                    products.append(product)
                    self._save_product(product)
                    
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"搜索解析失败: {e}")
        
        return products
    
    def _save_product(self, product: Product):
        """保存商品到数据库"""
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO products 
            (id, title, price, original_price, shop, url, image, location, sales, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (product.id, product.title, product.price, product.original_price,
              product.shop, product.url, product.image, product.location, product.sales))
        
        cursor.execute("""
            INSERT INTO price_history (product_id, price)
            VALUES (?, ?)
        """, (product.id, product.price))
        
        self.db.commit()
    
    async def get_price_history(self, product_url: str) -> tuple:
        """获取商品价格历史"""
        if not self.page:
            await self.init_browser()
        
        print(f"正在获取历史价格: {product_url}")
        await self.page.goto(product_url, wait_until="networkidle")
        await asyncio.sleep(3)
        
        # 提取商品ID
        parsed = urlparse(product_url)
        product_id = parse_qs(parsed.query).get("id", [""])[0]
        
        # 从数据库获取历史价格
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT price, recorded_at FROM price_history 
            WHERE product_id = ? 
            ORDER BY recorded_at DESC 
            LIMIT 30
        """, (product_id,))
        
        history = cursor.fetchall()
        
        # 获取当前商品信息
        try:
            title_el = await self.page.query_selector("h1")
            title = await title_el.inner_text() if title_el else ""
            
            price_el = await self.page.query_selector(".notranslate")
            price_text = await price_el.inner_text() if price_el else "0"
            current_price = float(price_text.replace("¥", "").strip() or 0)
            
        except:
            title = ""
            current_price = 0
        
        return {
            "product_id": product_id,
            "title": title,
            "current_price": current_price,
            "history": history
        }
    
    async def get_shop_info(self, shop_name: str) -> Optional[dict]:
        """获取店铺信息"""
        if not self.page:
            await self.init_browser()
        
        print(f"正在查询店铺: {shop_name}")
        
        # 搜索店铺
        encoded_name = quote(shop_name)
        url = f"https://shopsearch.taobao.com/search?app=shopsearch&q={encoded_name}"
        
        await self.page.goto(url, wait_until="networkidle")
        await asyncio.sleep(2)
        
        try:
            # 获取第一个店铺
            shop_el = await self.page.query_selector(".shop-item")
            if not shop_el:
                return None
            
            name_el = await shop_el.query_selector(".shop-name")
            name = await name_el.inner_text() if name_el else shop_name
            
            rating_el = await shop_el.query_selector(".shop-info .rate")
            rating_text = await rating_el.inner_text() if rating_el else "0"
            
            # 保存店铺信息
            cursor = self.db.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO shops (name, rating, description)
                VALUES (?, ?, ?)
            """, (name, float(rating_text or 0), ""))
            self.db.commit()
            
            return {
                "name": name,
                "rating": rating_text,
                "url": self.page.url
            }
            
        except Exception as e:
            print(f"获取店铺信息失败: {e}")
            return None

def format_product(p: Product, index: int) -> str:
    """格式化商品输出"""
    price_str = f"¥{p.price:.2f}"
    sales_str = f" | 销量: {p.sales}" if p.sales else ""
    location_str = f" | {p.location}" if p.location else ""
    return f"""
[{index}] {p.title[:50]}{'...' if len(p.title) > 50 else ''}
    价格: {price_str}{sales_str}
    店铺: {p.shop}{location_str}
    链接: {p.url}
"""

async def main():
    parser = argparse.ArgumentParser(description="淘宝购物助手")
    parser.add_argument("command", choices=["search", "history", "shop", "login"])
    parser.add_argument("arg", nargs="?", help="搜索关键词/商品链接/店铺名")
    parser.add_argument("--page", type=int, default=1, help="页码")
    
    args = parser.parse_args()
    
    client = TaobaoClient()
    
    try:
        if args.command == "login":
            await client.login()
        
        elif args.command == "search":
            if not args.arg:
                print("请提供搜索关键词")
                return
            products = await client.search(args.arg, args.page)
            print(f"\n找到 {len(products)} 个商品:\n")
            for i, p in enumerate(products, 1):
                print(format_product(p, i))
        
        elif args.command == "history":
            if not args.arg:
                print("请提供商品链接")
                return
            result = await client.get_price_history(args.arg)
            print(f"\n商品: {result['title']}")
            print(f"当前价格: ¥{result['current_price']:.2f}")
            print(f"\n历史价格记录 ({len(result['history'])} 条):")
            for price, date in result['history'][:10]:
                print(f"  {date}: ¥{price:.2f}")
        
        elif args.command == "shop":
            if not args.arg:
                print("请提供店铺名")
                return
            shop = await client.get_shop_info(args.arg)
            if shop:
                print(f"""
店铺: {shop['name']}
评分: {shop['rating']}
链接: {shop['url']}
""")
            else:
                print("未找到店铺信息")
        
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
