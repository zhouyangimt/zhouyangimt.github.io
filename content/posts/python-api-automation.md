---
title: "Python 自动化实战：API 自动化——调用50+免费API"
date: 2026-06-24
tags: ["Python", "API", "自动化", "独立开发"]
description: "不用爬虫也能拿到海量数据——天气、汇率、新闻、AI大模型、图片搜索，50+免费API让你的产品能力翻倍。"
---

## 为什么你应该优先用 API 而不是爬虫？

上篇文章讲了 Web Scraping，结尾我留了一句话：**如果网站有公开 API，优先用 API 而不是爬页面**。

这不是敷衍。我做独立开发这几年，在 API 和爬虫之间来回横跳过太多次，教训深刻。

说一个真实例子：2024 年我写了个币圈信息聚合器，一开始爬了三个交易所的页面。每个页面结构不一样，写解析逻辑就花了两天。上线两周后，其中一家改了 CSS class 名，数据全挂了。连夜修兼容，刚修好，另一家加了 Cloudflare 盾。那一刻我真的想砸键盘。

后来发现这些交易所都有公开 API，免费，还带文档。切过去只花了半天，之后再也没挂过。

API 和爬虫的核心区别：

| | API | 爬虫 |
|---|---|---|
| 稳定性 | 契约保证，极少变动 | 随时会挂 |
| 数据结构 | 直接返回 JSON | 需要自己解析 HTML |
| 反爬风险 | 无 | 有 |
| 速度 | 快（几十ms） | 慢（几百ms以上） |
| 上手门槛 | 需要读文档 | 需要懂 HTML/CSS 选择器 |

这篇文章教你用 Python 调动 50+ 免费 API，附带完整代码。更重要的是，教你建立一套**通用的 API 调用框架**——以后碰到任何新 API，10 分钟内就能接上。

## API 调用的通用流程

![API 调用流程图](/images/api-automation-flow.png)

不管什么 API，核心就是上面这个流程。新手最容易卡在第三步"读文档"直接跳过——拿到 API key 就开始瞎试。我吃过这个亏，所以多说一句：**花 5 分钟读文档比调试 2 小时划算一万倍**。

## 基础篇：requests 三板斧

Python 调 API 的核心库就一个——`requests`。不需要装第三方 SDK，标准 HTTP 库足够覆盖 95% 的场景。

```bash
pip install requests
```

三个最常用的模式：

```python
import requests

# 1. GET 请求（拿数据）
resp = requests.get(
    "https://api.example.com/data",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    params={"page": 1, "limit": 20}  # 查询参数
)

# 2. POST 请求（提交数据）
resp = requests.post(
    "https://api.example.com/create",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={"name": "test", "value": 42}  # JSON body
)

# 3. 解析响应
if resp.status_code == 200:
    data = resp.json()  # 直接拿到 dict
    print(data["results"])
else:
    print(f"请求失败: {resp.status_code} - {resp.text}")
```

就这三板斧。GET 拿数据，POST 发数据，`resp.json()` 解析。剩下全是业务逻辑。

## 实战一：天气 API（无需注册，零门槛）

[Open-Meteo](https://open-meteo.com/) 是我最喜欢的免费 API——不需要注册、不需要 API Key、不限调用次数。独立开发者做天气类小工具的首选。

```python
import requests

def get_weather(lat, lon):
    """获取指定坐标的7天天气预报"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": ["temperature_2m_max", "temperature_2m_min",
                   "precipitation_sum", "weathercode"],
        "timezone": "Asia/Shanghai",
        "forecast_days": 7
    }
    resp = requests.get(url, params=params)
    data = resp.json()

    print(f"📍 坐标 ({lat}, {lon}) 未来7天预报：")
    for i, date in enumerate(data["daily"]["time"]):
        high = data["daily"]["temperature_2m_max"][i]
        low = data["daily"]["temperature_2m_min"][i]
        rain = data["daily"]["precipitation_sum"][i]
        print(f"  {date} | {low}°C ~ {high}°C | 降水 {rain}mm")

# 上海坐标
get_weather(31.23, 121.47)
```

输出：

```
📍 坐标 (31.23, 121.47) 未来7天预报：
  2026-06-24 | 23°C ~ 31°C | 降水 0.0mm
  2026-06-25 | 24°C ~ 33°C | 降水 2.5mm
  ...
```

这个 API 还支持历史天气、空气质量、海洋数据。URL 拼参数就行，不用看半天文档。

## 实战二：汇率 API（同样是零门槛）

做过多币种定价的产品，一定需要实时汇率。[Frankfurter](https://www.frankfurter.app/) 基于欧洲央行数据，免费，无需注册。

```python
import requests
from datetime import datetime

def convert_currency(amount, from_currency, to_currency):
    """实时汇率转换"""
    url = "https://api.frankfurter.app/latest"
    params = {
        "amount": amount,
        "from": from_currency,
        "to": to_currency
    }
    resp = requests.get(url, params=params)
    data = resp.json()

    rate = data["rates"][to_currency]
    result = data["rates"][to_currency]  # amount * rate 已在响应中
    print(f"💱 {amount} {from_currency} = {result} {to_currency}")
    print(f"   汇率: 1 {from_currency} = {rate} {to_currency}")
    return result

# 100 美元换人民币
convert_currency(100, "USD", "CNY")

# 查看所有支持币种
def list_currencies():
    resp = requests.get("https://api.frankfurter.app/currencies")
    currencies = resp.json()
    print(f"支持 {len(currencies)} 种货币:")
    for code, name in list(currencies.items())[:10]:
        print(f"  {code}: {name}")

list_currencies()
```

这个 API 还支持历史汇率：`/2025-01-01?from=USD&to=CNY` 能查到任意日期的汇率。做财务报表或价格分析的时候特别有用。

## 实战三：GitHub API（开发者必备）

GitHub REST API 免费，不登录每小时 60 次请求，登录后 5000 次。对个人项目完全够用。

```python
import requests

def get_trending_repos(language="python", per_page=5):
    """获取 GitHub 上某语言的热门仓库"""
    url = "https://api.github.com/search/repositories"
    params = {
        "q": f"language:{language}",
        "sort": "stars",
        "order": "desc",
        "per_page": per_page
    }
    headers = {"Accept": "application/vnd.github.v3+json"}

    resp = requests.get(url, headers=headers, params=params)
    data = resp.json()

    print(f"🔥 {language} 语言 Stars 最高的仓库：")
    for repo in data["items"]:
        print(f"  ⭐ {repo['stargazers_count']:,} | {repo['full_name']}")
        print(f"     {repo['description'][:80] if repo['description'] else '无描述'}")
        print(f"     {repo['html_url']}\n")

get_trending_repos("rust", 5)
```

进阶：监控仓库动态。你关注的项目发了新 Release，自动通知你：

```python
def check_latest_release(owner, repo):
    """检查仓库最新 Release"""
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    resp = requests.get(url)
    if resp.status_code == 200:
        release = resp.json()
        print(f"📦 {owner}/{repo}")
        print(f"   最新版本: {release['tag_name']}")
        print(f"   发布时间: {release['published_at']}")
        print(f"   下载地址: {release['html_url']}")
    else:
        print(f"该仓库没有 Release")

check_latest_release("tauri-apps", "tauri")
```

这个例子可以配合上一篇的 cron 定时任务——每天跑一次，有新版就飞书/Telegram 通知你。

## 实战四：AI 大模型 API（免费额度管够）

现在做大模型 API 的厂商太多了，而且每家都有免费额度：

| 平台 | 免费额度 | 兼容格式 |
|------|---------|---------|
| Groq | 多模型免费 | OpenAI 兼容 |
| DeepSeek | 注册送 500 万 tokens | OpenAI 兼容 |
| 硅基流动 | 多模型免费额度 | OpenAI 兼容 |
| Google Gemini | 免费 tier | 自有格式 |

**好消息**：这些平台都兼容 OpenAI 的 API 格式，一套代码全搞定。

```python
import requests

def call_llm(api_key, base_url, model, prompt):
    """通用大模型调用函数——兼容 OpenAI 格式的所有平台"""
    url = f"{base_url}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "你是 Python 技术专家，回答简洁"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }

    resp = requests.post(url, headers=headers, json=payload)
    data = resp.json()
    return data["choices"][0]["message"]["content"]

# 示例：调用 DeepSeek（替换成你自己的 key）
# result = call_llm(
#     api_key="sk-your-deepseek-key",
#     base_url="https://api.deepseek.com/v1",
#     model="deepseek-chat",
#     prompt="用 3 句话解释什么是装饰器"
# )
# print(result)
```

做产品的时候，可以把 AI 能力嵌入到任何地方——自动总结、智能分类、内容生成、代码审查。因为有免费额度，前期验证成本基本为零。

## 实战五：Unsplash 图片 API（让你的产品好看）

独立开发者的产品最大的问题之一是"看着像 demo"。Unsplash 免费 API 可以提供高质量配图。

```python
import requests

def search_photos(query, per_page=5):
    """搜索 Unsplash 高质量图片"""
    url = "https://api.unsplash.com/search/photos"
    # 注册 https://unsplash.com/developers 获取 Access Key
    headers = {"Authorization": "Client-ID YOUR_ACCESS_KEY"}
    params = {"query": query, "per_page": per_page}

    resp = requests.get(url, headers=headers, params=params)
    data = resp.json()

    print(f"🖼️ 搜索 '{query}' 的结果：")
    for photo in data["results"]:
        print(f"  📷 {photo['description'][:60] if photo['description'] else '无描述'}")
        print(f"     作者: {photo['user']['name']}")
        print(f"     原图: {photo['urls']['regular']}")
        print(f"     缩略图: {photo['urls']['thumb']}\n")

# search_photos("coding setup")
```

Unsplash 免费额度是每小时 50 次请求。对于博客配图、产品 Landing Page、文章封面这些场景绰绰有余。

## 进阶：打造通用 API 调用框架

上面 5 个例子覆盖了常见模式。但真实项目中你需要同时调多个 API，每个 API 的错误处理、重试、超时配置都不一样。下面是我在生产环境用的通用框架：

```python
import requests
import time
from functools import wraps
from typing import Callable

class APIClient:
    """通用 API 客户端——错误处理 + 重试 + 限流 + 超时"""

    def __init__(self, base_url: str, headers: dict = None,
                 timeout: int = 10, max_retries: int = 3):
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _request(self, method: str, path: str, **kwargs):
        """核心请求方法——自动重试 + 指数退避"""
        url = f"{self.base_url}{path}"
        kwargs.setdefault("timeout", self.timeout)

        for attempt in range(self.max_retries):
            try:
                resp = self.session.request(method, url, **kwargs)

                # 限流：等到 Retry-After 再重试
                if resp.status_code == 429:
                    wait = int(resp.headers.get("Retry-After", 5))
                    print(f"⚠️ 限流，{wait}s 后重试 (第 {attempt+1}/{self.max_retries} 次)")
                    time.sleep(wait)
                    continue

                # 服务端错误：指数退避
                if resp.status_code >= 500:
                    wait = 2 ** attempt
                    print(f"⚠️ 服务端错误 {resp.status_code}，{wait}s 后重试")
                    time.sleep(wait)
                    continue

                resp.raise_for_status()
                return resp.json()

            except requests.exceptions.Timeout:
                print(f"⏱️ 请求超时 (第 {attempt+1}/{self.max_retries} 次)")
                if attempt == self.max_retries - 1:
                    raise
                time.sleep(2 ** attempt)

            except requests.exceptions.RequestException as e:
                print(f"❌ 请求失败: {e}")
                if attempt == self.max_retries - 1:
                    raise
                time.sleep(2 ** attempt)

        raise Exception(f"超过最大重试次数 {self.max_retries}")

    def get(self, path: str, **kwargs):
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs):
        return self._request("POST", path, **kwargs)


# 使用示例
weather_client = APIClient(
    base_url="https://api.open-meteo.com/v1",
    timeout=5
)

data = weather_client.get("/forecast", params={
    "latitude": 31.23,
    "longitude": 121.47,
    "daily": "temperature_2m_max",
    "forecast_days": 3
})
print(data["daily"])
```

这个框架你复制到任何项目里就能用。核心思想：**不要在每个 API 调用的地方重复写 try/except 和 retry 逻辑**——抽象成一层，所有 API 共用。

重试策略是关键：
- **429 限流**：等 `Retry-After` 头指定的时间，不要不管不顾地重试
- **5xx 服务端错误**：指数退避（1s → 2s → 4s）
- **超时**：同样指数退避，每次翻倍等待

## 50+ 免费 API 速查表

下面这个表是我用过的、确认能用的免费 API。按场景分类：

### 天气 & 地理
| API | 免费额度 | 需要 Key | 亮点 |
|-----|---------|---------|------|
| Open-Meteo | 无限 | 否 | 天气/历史/空气质量 |
| OpenWeatherMap | 1000次/天 | 是 | 当前天气 + 5天预报 |
| WeatherAPI | 100万次/月 | 是 | 天气 + 天文 + 时区 |
| IP-API | 45次/分钟 | 否 | IP 转地理位置 |
| Nominatim | 1次/秒 | 否 | 地址 ↔ 坐标转换 |

### 金融 & 汇率
| API | 免费额度 | 需要 Key | 亮点 |
|-----|---------|---------|------|
| Frankfurter | 无限 | 否 | 汇率 + 历史 |
| ExchangeRate-API | 1500次/月 | 是 | 多币种 |
| CoinGecko | 30次/分钟 | 否 | 加密货币全数据 |
| Alpha Vantage | 25次/天 | 是 | 股票数据 |

### 开发 & 工具
| API | 免费额度 | 需要 Key | 亮点 |
|-----|---------|---------|------|
| GitHub REST API | 60次/时（无登录） | 否 | 仓库/Issues/搜索 |
| GitLab API | 无限 | 否 | 私有仓库也支持 |
| JSONPlaceholder | 无限 | 否 | 假数据，开发测试用 |
| httpbin | 无限 | 否 | 调试 HTTP 请求 |

### AI & 机器学习
| API | 免费额度 | 需要 Key | 亮点 |
|-----|---------|---------|------|
| Groq | 多模型免费 | 是 | 速度极快 |
| DeepSeek | 500万 tokens | 是 | 性价比高 |
| Google Gemini | 免费 tier | 是 | 多模态 |
| HuggingFace | 免费推理 | 是 | 海量开源模型 |
| Remove.bg | 50次/月 | 是 | 一键去背景 |

### 新闻 & 内容
| API | 免费额度 | 需要 Key | 亮点 |
|-----|---------|---------|------|
| NewsAPI | 100次/天 | 是 | 全球新闻聚合 |
| HackerNews | 无限 | 否 | 科技圈热门 |
| Reddit JSON | 无限 | 否 | 任何 subreddit 加 .json |
| Dev.to | 无限 | 否 | 开发者文章 |

### 图片 & 媒体
| API | 免费额度 | 需要 Key | 亮点 |
|-----|---------|---------|------|
| Unsplash | 50次/时 | 是 | 高质量图库 |
| Pexels | 200次/时 | 是 | 图片 + 视频 |
| Lorem Picsum | 无限 | 否 | 随机占位图 |
| Dog API | 无限 | 否 | 随机狗图 |

### 文本 & 翻译
| API | 免费额度 | 需要 Key | 亮点 |
|-----|---------|---------|------|
| LibreTranslate | 无限（自部署） | 否 | 开源翻译 |
| Lingva | 无限 | 否 | Google 翻译代理 |
| Quotes REST | 无限 | 否 | 随机名言 |

### 其他实用
| API | 免费额度 | 需要 Key | 亮点 |
|-----|---------|---------|------|
| Public APIs | 无限 | 否 | API 目录本身也是个 API |
| TheCatAPI | 无限 | 是 | 猫图 + 品种信息 |
| Pokemon API | 无限 | 否 | 宝可梦全数据 |
| OpenAI API | $5 试用金 | 是 | GPT 全家桶 |

总量超过 50 个。其中带 "无限" 标记的可以直接上手，不需要注册。

## 真实场景组合：天气推送机器人

光看 API 列表没用，组合起来才有力量。我用 3 个免费 API 拼了一个天气预报推送：

```python
from APIClient import APIClient  # 上面写的通用框架
import json
from datetime import datetime

# 1. 坐标转城市名（Nominatim）
geo = APIClient("https://nominatim.openstreetmap.org")
geo.session.headers["User-Agent"] = "WeatherBot/1.0"  # Nominatim 要求

# 2. 天气数据（Open-Meteo）
weather = APIClient("https://api.open-meteo.com/v1")

# 3. 推送通知（假设你有一个 webhook）
# notify = APIClient("https://your-webhook.com")


def daily_weather_report(lat, lon):
    """每日天气报告"""
    # 获取城市名
    location = geo.get("/reverse", params={
        "lat": lat, "lon": lon, "format": "json"
    })
    city = location.get("address", {}).get("city", "未知城市")

    # 获取天气
    data = weather.get("/forecast", params={
        "latitude": lat, "longitude": lon,
        "daily": ["temperature_2m_max", "temperature_2m_min",
                   "precipitation_sum", "weathercode"],
        "forecast_days": 1,
        "timezone": "Asia/Shanghai"
    })

    today = data["daily"]
    report = f"""
📅 {today['time'][0]} {city}天气预报
━━━━━━━━━━━━━━━━━━
🌡️ 温度: {today['temperature_2m_min'][0]}°C ~ {today['temperature_2m_max'][0]}°C
🌧️ 降水: {today['precipitation_sum'][0]}mm
💡 {'今天有雨，出门带伞' if today['precipitation_sum'][0] > 0 else '天气不错'}
"""

    print(report)
    # 推送到飞书/Telegram/邮件（具体代码见系列第 01 篇）
    return report

daily_weather_report(31.23, 121.47)
```

三个 API，零费用，每天早上跑一次。配合上一篇文章的 cron 示例，这就是一个完整产品。

## 踩坑记录

写 API 调用这几年，有些坑重复踩：

**1. API Key 写死在代码里**

绝对不要。用环境变量：

```python
import os
api_key = os.environ["OPENAI_API_KEY"]  # 正确
# api_key = "sk-xxxxxxxx"  # 错误：一推 GitHub 就泄露
```

**2. 不检查 rate limit**

每个 API 都有额度。调用前查 `X-RateLimit-Remaining` 响应头：

```python
resp = requests.get(url)
remaining = resp.headers.get("X-RateLimit-Remaining")
if remaining and int(remaining) < 10:
    print("⚠️ 额度预警，暂停使用")
    time.sleep(60)
```

**3. 同步调多个 API，一个超时全卡住**

用 `concurrent.futures` 并行请求：

```python
from concurrent.futures import ThreadPoolExecutor

def fetch_all(urls):
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(
            lambda u: requests.get(u, timeout=5).json(),
            urls
        ))
    return results
```

**4. API 改版不知道**

定时跑一次测试脚本，监控响应结构变化。最简单的办法：

```python
import hashlib

# 记录响应 key 结构的哈希
resp = requests.get("https://api.example.com/data").json()
structure_hash = hashlib.md5(
    str(sorted(resp.keys())).encode()
).hexdigest()

# 存到文件，下次对比，变了就告警
```

## 从这里开始

这篇文章和你上篇学的爬虫组合在一起，就是你作为独立开发者获取数据的全部武器：

- **有 API → 用本文的方法调**
- **没 API 但页面是静态的 → 用上篇的 BeautifulSoup 爬**
- **页面是 SPA/JS 渲染的 → 用 Playwright**

建议今天就找 2-3 个感兴趣的 API，用上面 `APIClient` 框架接一下。10 行代码就能把一个免费数据源接到你的项目里。接得多了，你会发现很多产品想法根本不需要自己造数据——世界上已经有免费的 API 在等你用了。

---

**系列导航**：[01 日常任务自动化](/posts/python-automation-daily-tasks/) | [02 Web Scraping 实战](/posts/python-web-scraping/) | **03 API 自动化** | [04 数据分析自动化](/posts/python-pandas-analysis/)

*Python 自动化实战系列，下一篇：数据分析自动化——Pandas 实战，把 API 拿回来的数据变成洞察。*
