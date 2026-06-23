---
title: "Python 自动化实战：Web Scraping 入门到实战"
date: 2026-06-23
tags: ["Python", "爬虫", "自动化", "独立开发"]
description: "从零学会用 Python 抓取网页数据——招聘信息、价格监控、竞品分析，独立开发者必备技能。"
---

## 为什么独立开发者要学爬虫？

我做过的产品里，有好几个的起点都是爬虫。

比如我写过一个宠物领养信息聚合站——爬了 4 个领养平台的公开信息，去重、分类、加上地理位置搜索。上线第一周零推广，纯靠搜索引擎自然流量每天 200+ 访客。因为用户确实有这个需求，而之前没人把这些信息汇总起来。

还写过一个二手相机价格监控器，每天爬几个主流交易平台的特定型号价格，低于设定阈值就推通知。我自己用它在闲鱼上淘到一台 9 成新的 Sony A7M3，比市场价便宜 2000 块。

爬虫不是"非法抓数据"——它是独立开发者的信息杠杆。你不需要爬用户隐私、不需要绕过付费墙、不需要做任何灰色地带的事。互联网上有大量**合法公开的数据**散落各处，没人把它们结构化、没人把它们串联起来。这就是你的机会。

今天这篇文章从零开始讲 Python Web Scraping，附带两个实战案例。

## 核心流程

![爬虫工作流程](/images/web-scraping-flow.png)

整个爬虫就四个环节：发请求 → 解析 → 提取 → 存储。任何一个爬虫项目都是这个流程的变体。

## 第一件事：装库

```bash
pip install requests beautifulsoup4 lxml
```

- `requests`：发 HTTP 请求，带回网页 HTML
- `beautifulsoup4`：把 HTML 解析成可查询的树结构
- `lxml`：更快的解析器，soup 的底层引擎

## 实战一：爬 GitHub Trending

第一个案例，爬 GitHub Trending 页面，拿到当天的热门仓库名、描述、Stars 数。这个页面不需要登录，反爬宽松，适合练手。

### 第一步：看页面结构

先打开 https://github.com/trending ，按 F12 打开开发者工具，找到仓库列表的 HTML 结构。你会看到每个仓库是一个 `<article>` 标签，里面包含标题链接、描述、Stars 数等信息。

### 第二步：写代码

```python
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

url = "https://github.com/trending"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
resp = requests.get(url, headers=headers)
soup = BeautifulSoup(resp.text, "lxml")

repos = []
for article in soup.find_all("article", class_="Box-row"):
    # 仓库名
    h2 = article.find("h2", class_="h3")
    if not h2:
        continue
    repo_name = h2.get_text(strip=True).replace("\n", "").replace(" ", "")

    # 描述
    desc_tag = article.find("p", class_="col-9")
    description = desc_tag.get_text(strip=True) if desc_tag else ""

    # Stars
    stars_tag = article.find("span", class_="d-inline-block float-sm-right")
    stars = stars_tag.get_text(strip=True) if stars_tag else "0"

    repos.append({
        "name": repo_name,
        "description": description,
        "stars": stars,
    })

# 存 CSV
filename = f"github_trending_{datetime.now().strftime('%Y%m%d')}.csv"
with open(filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "description", "stars"])
    writer.writeheader()
    writer.writerows(repos)

print(f"抓到 {len(repos)} 个仓库，已保存到 {filename}")
```

### 关键点

**User-Agent 必须设**。GitHub 会检查这个头，不带 UA 直接返回 403。这在爬虫里是基本操作——几乎所有正经网站都会检查 UA。

**CSS 选择器靠观察**。`article.Box-row`、`h2.h3` 这些类名不是猜出来的，是打开 DevTools 看到的。写爬虫之前花 5 分钟看页面结构，比写代码重要。

**存 CSV 而不是 print**。你把数据打印到终端，下次还想用就得重新爬。存成 CSV，后面分析、画图、做产品都用得上。

## 实战二：价格监控器

上一个案例是「一次性抓取」。但很多场景需要**持续监控变化**——价格、库存、更新。下面写一个简单的价格监控器。

场景：监控一个产品页面的价格，价格变化时推送通知。

```python
import requests
from bs4 import BeautifulSoup
import time
import hashlib
import smtplib
from email.mime.text import MIMEText

URL = "https://example.com/product-page"
CHECK_INTERVAL = 3600  # 每小时检查一次

def get_price():
    """从页面提取价格，返回 float"""
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(URL, headers=headers, timeout=10)
    soup = BeautifulSoup(resp.text, "lxml")

    # 假设价格在 class="price" 的 span 里
    price_tag = soup.find("span", class_="price")
    if not price_tag:
        return None

    # "¥ 1,299.00" → 1299.0
    price_text = price_tag.get_text(strip=True)
    price_text = price_text.replace("¥", "").replace(",", "").replace(" ", "")
    return float(price_text)

def send_alert(old_price, new_price):
    """价格变化时发邮件通知"""
    msg = MIMEText(f"价格变动: ¥{old_price} → ¥{new_price}")
    msg["Subject"] = f"价格提醒 - {URL}"
    msg["From"] = "your@email.com"
    msg["To"] = "your@email.com"

    with smtplib.SMTP_SSL("smtp.qq.com", 465) as s:
        s.login("your@email.com", "授权码")
        s.send_message(msg)

# 主循环
last_price = None
while True:
    try:
        current_price = get_price()
        if current_price is None:
            print("提取价格失败，等待下次检查")
        elif last_price is not None and current_price != last_price:
            send_alert(last_price, current_price)
            print(f"价格变化: ¥{last_price} → ¥{current_price}")
        else:
            print(f"价格未变: ¥{current_price}")

        last_price = current_price
    except Exception as e:
        print(f"检查出错: {e}")

    time.sleep(CHECK_INTERVAL)
```

这个脚本的逻辑很清楚：拿当前价格 → 和上次价格比较 → 有变化就通知 → 等一小时再来。你可以扔到服务器上用 `nohup` 跑，或者配上 cron 定时触发。

## 常见障碍与解法

爬虫写着写着就会踩坑。我总结几个高频问题和解决方案：

### 1. 403 Forbidden / 反爬拦截

**原因**：网站检测到你没有浏览器特征（UA、Cookie、Referer）。

**解法**：
```python
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://www.google.com/",
}
session = requests.Session()
session.headers.update(headers)

# 先访问首页拿 Cookie，再访问目标页
session.get("https://example.com")
resp = session.get("https://example.com/target-page")
```

关键技巧：**先访问首页**。很多网站的 Cookie 是在首页种的，带着 Cookie 再请求目标页就不会被拦。

### 2. 页面内容是 JS 渲染的

**症状**：`requests.get()` 拿到的 HTML 里没有数据，但在浏览器里能看到。

**判断方法**：`print(resp.text[:500])` 看看 HTML 里有没有你要的数据。如果只有空壳和 `<script>` 标签，那就是 JS 渲染的问题。

**解法**：用 Playwright 或 Selenium 模拟浏览器：

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://spa-website.com")
    page.wait_for_selector(".data-loaded")  # 等数据加载完
    html = page.content()
    soup = BeautifulSoup(html, "lxml")
    # 后续解析正常进行
```

Playwright 比 Selenium 快，API 更现代。代价是比纯 requests 慢很多——一个页面 2-5 秒 vs 0.2 秒。

### 3. 请求太频繁被限流

**解法**：加延迟 + 随机抖动。

```python
import time
import random

time.sleep(random.uniform(2, 5))  # 随机等 2-5 秒
```

不要用固定间隔。`time.sleep(3)` 是明显的机器人特征，`random.uniform(2, 5)` 更像人类。

### 4. 数据存哪？

三个选择，从简单到复杂：

| 方案 | 适用场景 | 容量 |
|------|---------|------|
| JSON 文件 | 少量数据、快速原型 | < 1万条 |
| CSV 文件 | 表格数据、Excel 分析 | < 10万条 |
| SQLite | 需要查询过滤、持续采集 | > 10万条 |

SQLite 是 Python 标准库自带的，一行配置都不用写：

```python
import sqlite3

conn = sqlite3.connect("scraped_data.db")
conn.execute("""
    CREATE TABLE IF NOT EXISTS prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        price REAL,
        checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.execute(
    "INSERT INTO prices (url, price) VALUES (?, ?)",
    (URL, current_price)
)
conn.commit()
```

我自己的数据项目超过一周的采集基本都切到 SQLite，不用操心 MySQL/PostgreSQL 的配置和维护。

## 爬虫的边界

写到最后必须聊这件事。我做爬虫有一条底线：**只爬公开数据，不绕过付费墙，不碰用户隐私**。

具体来说：

- ✅ 爬取公开的列表页、产品页、文章页
- ✅ 用于信息聚合、个人分析、价格监控
- ❌ 绕过登录才能看到的内容
- ❌ 大量爬取并原样转载（版权问题）
- ❌ 把爬取的用户数据用于商业用途

访问 `网站.com/robots.txt` 看看网站的爬虫规则。遵守 `Disallow` 指令，设置合理的请求间隔。做一个有礼貌的爬虫。

另外，如果网站有公开 API，**优先用 API 而不是爬页面**。API 更稳定、解析更轻松、不会因为页面改版而挂掉。很多网站（GitHub、Reddit、各种开放数据平台）都有免费 API。爬虫是最后手段，不是第一选择。

## 从这里开始

这两个案例——GitHub Trending 和价格监控——覆盖了爬虫 80% 的场景。剩下的是你具体要爬什么、解析什么、怎么存的问题。

建议今天就动手：找一个你经常手动查看的网页（产品页、列表页、排行榜），写 30 行代码让它自动抓下来。第一个脚本可能丑、可能慢、可能只跑一次就挂了——没关系，跑起来就是胜利。

下一篇我会继续这个系列，讲 **API 自动化**——如何调用 50+ 免费 API 来增强你的产品。很多数据其实不需要爬，直接调 API 更干净。

---

**系列导航**：[01 日常任务自动化](/posts/python-automation-daily-tasks/) | **02 Web Scraping 实战** | [03 API 自动化（即将更新）](/posts/)

*Python 自动化实战系列，下一篇：API 自动化——把你产品接上 50+ 免费数据源。*
