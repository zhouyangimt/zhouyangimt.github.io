---
title: "Python 自动化实战：API 自动化——调用50+免费API"
date: 2026-06-24
description: "不用爬虫也能拿到海量数据——天气、汇率、新闻、AI大模型、图片搜索，50+免费API让你的产品能力翻倍。"
tags: [Python, API, 自动化, 独立开发]
draft: false
---

## 为什么你应该优先用 API 而不是爬虫？
上篇文章讲了 Web Scraping，结尾我留了一句话：**如果网站有公开 API，优先用 API 而不是爬页面**。

这不是敷衍。我做独立开发这几年，在 API 和爬虫之间来回横跳过太多次，教训深刻。

说一个真实例子：2024 年我写了个币圈信息聚合器，一开始爬了三个交易所的页面。每个页面结构不一样，写解析逻辑就花了两天。上线两周后，其中一家改了 CSS class 名，数据全挂了。连夜修兼容，刚修好，另一家加了 Cloudflare 盾。那一刻我真的想砸键盘。

后来发现这些交易所都有公开 API，免费，还带文档。切过去只花了半天，之后再也没挂过。

API 和爬虫的核心区别：API爬虫稳定性契约保证，极少变动随时会挂数据结构直接返回 JSON需要自己解析 HTML反爬风险无有速度快（几十ms）慢（几百ms以上）上手门槛需要读文档需要懂 HTML/CSS 选择器这篇文章教你用 Python 调动 50+ 免费 API，附带完整代码。更重要的是，教你建立一套**通用的 API 调用框架**——以后碰到任何新 API，10 分钟内就能接上。
## API 调用的通用流程

不管什么 API，核心就是上面这个流程。新手最容易卡在第三步"读文档"直接跳过——拿到 API key 就开始瞎试。我吃过这个亏，所以多说一句：**花 5 分钟读文档比调试 2 小时划算一万倍**。
## 基础篇：requests 三板斧
Python 调 API 的核心库就一个——`requests`。不需要装第三方 SDK，标准 HTTP 库足够覆盖 95% 的场景。pip install requests
`三个最常用的模式：import requests

# 1. GET 请求（拿数据）
resp = requests.get(
    &#34;https://api.example.com/data&#34;,
    headers={&#34;Authorization&#34;: &#34;Bearer YOUR_API_KEY&#34;},
    params={&#34;page&#34;: 1, &#34;limit&#34;: 20}  # 查询参数
)

# 2. POST 请求（提交数据）
resp = requests.post(
    &#34;https://api.example.com/create&#34;,
    headers={&#34;Authorization&#34;: &#34;Bearer YOUR_API_KEY&#34;},
    json={&#34;name&#34;: &#34;test&#34;, &#34;value&#34;: 42}  # JSON body
)

# 3. 解析响应
if resp.status_code == 200:
    data = resp.json()  # 直接拿到 dict
    print(data[&#34;results&#34;])
else:
    print(f&#34;请求失败: {resp.status_code} - {resp.text}&#34;)
`就这三板斧。GET 拿数据，POST 发数据，`resp.json()` 解析。剩下全是业务逻辑。
## 实战一：天气 API（无需注册，零门槛）
Open-Meteo
是我最喜欢的免费 API——不需要注册、不需要 API Key、不限调用次数。独立开发者做天气类小工具的首选。import requests

def get_weather(lat, lon):
    &#34;&#34;&#34;获取指定坐标的7天天气预报&#34;&#34;&#34;
    url = &#34;https://api.open-meteo.com/v1/forecast&#34;
    params = {
        &#34;latitude&#34;: lat,
        &#34;longitude&#34;: lon,
        &#34;daily&#34;: [&#34;temperature_2m_max&#34;, &#34;temperature_2m_min&#34;,
                   &#34;precipitation_sum&#34;, &#34;weathercode&#34;],
        &#34;timezone&#34;: &#34;Asia/Shanghai&#34;,
        &#34;forecast_days&#34;: 7
    }
    resp = requests.get(url, params=params)
    data = resp.json()

    print(f&#34;📍 坐标 ({lat}, {lon}) 未来7天预报：&#34;)
    for i, date in enumerate(data[&#34;daily&#34;][&#34;time&#34;]):
        high = data[&#34;daily&#34;][&#34;temperature_2m_max&#34;][i]
        low = data[&#34;daily&#34;][&#34;temperature_2m_min&#34;][i]
        rain = data[&#34;daily&#34;][&#34;precipitation_sum&#34;][i]
        print(f&#34;  {date} | {low}°C ~ {high}°C | 降水 {rain}mm&#34;)

# 上海坐标
get_weather(31.23, 121.47)
`输出：`📍 坐标 (31.23, 121.47) 未来7天预报：
  2026-06-24 | 23°C ~ 31°C | 降水 0.0mm
  2026-06-25 | 24°C ~ 33°C | 降水 2.5mm
  ...
`这个 API 还支持历史天气、空气质量、海洋数据。URL 拼参数就行，不用看半天文档。
## 实战二：汇率 API（同样是零门槛）
做过多币种定价的产品，一定需要实时汇率。Frankfurter
基于欧洲央行数据，免费，无需注册。import requests
from datetime import datetime

def convert_currency(amount, from_currency, to_currency):
    &#34;&#34;&#34;实时汇率转换&#34;&#34;&#34;
    url = &#34;https://api.frankfurter.app/latest&#34;
    params = {
        &#34;amount&#34;: amount,
        &#34;from&#34;: from_currency,
        &#34;to&#34;: to_currency
    }
    resp = requests.get(url, params=params)
    data = resp.json()

    rate = data[&#34;rates&#34;][to_currency]
    result = data[&#34;rates&#34;][to_currency]  # amount * rate 已在响应中
    print(f&#34;💱 {amount} {from_currency} = {result} {to_currency}&#34;)
    print(f&#34;   汇率: 1 {from_currency} = {rate} {to_currency}&#34;)
    return result

# 100 美元换人民币
convert_currency(100, &#34;USD&#34;, &#34;CNY&#34;)

# 查看所有支持币种
def list_currencies():
    resp = requests.get(&#34;https://api.frankfurter.app/currencies&#34;)
    currencies = resp.json()
    print(f&#34;支持 {len(currencies)} 种货币:&#34;)
    for code, name in list(currencies.items())[:10]:
        print(f&#34;  {code}: {name}&#34;)

list_currencies()
`这个 API 还支持历史汇率：`/2025-01-01?from=USD&to=CNY` 能查到任意日期的汇率。做财务报表或价格分析的时候特别有用。
## 实战三：GitHub API（开发者必备）
GitHub REST API 免费，不登录每小时 60 次请求，登录后 5000 次。对个人项目完全够用。import requests

def get_trending_repos(language=&#34;python&#34;, per_page=5):
    &#34;&#34;&#34;获取 GitHub 上某语言的热门仓库&#34;&#34;&#34;
    url = &#34;https://api.github.com/search/repositories&#34;
    params = {
        &#34;q&#34;: f&#34;language:{language}&#34;,
        &#34;sort&#34;: &#34;stars&#34;,
        &#34;order&#34;: &#34;desc&#34;,
        &#34;per_page&#34;: per_page
    }
    headers = {&#34;Accept&#34;: &#34;application/vnd.github.v3+json&#34;}

    resp = requests.get(url, headers=headers, params=params)
    data = resp.json()

    print(f&#34;🔥 {language} 语言 Stars 最高的仓库：&#34;)
    for repo in data[&#34;items&#34;]:
        print(f&#34;  ⭐ {repo[&#39;stargazers_count&#39;]:,} | {repo[&#39;full_name&#39;]}&#34;)
        print(f&#34;     {repo[&#39;description&#39;][:80] if repo[&#39;description&#39;] else &#39;无描述&#39;}&#34;)
        print(f&#34;     {repo[&#39;html_url&#39;]}\n&#34;)

get_trending_repos(&#34;rust&#34;, 5)
`进阶：监控仓库动态。你关注的项目发了新 Release，自动通知你：def check_latest_release(owner, repo):
    &#34;&#34;&#34;检查仓库最新 Release&#34;&#34;&#34;
    url = f&#34;https://api.github.com/repos/{owner}/{repo}/releases/latest&#34;
    resp = requests.get(url)
    if resp.status_code == 200:
        release = resp.json()
        print(f&#34;📦 {owner}/{repo}&#34;)
        print(f&#34;   最新版本: {release[&#39;tag_name&#39;]}&#34;)
        print(f&#34;   发布时间: {release[&#39;published_at&#39;]}&#34;)
        print(f&#34;   下载地址: {release[&#39;html_url&#39;]}&#34;)
    else:
        print(f&#34;该仓库没有 Release&#34;)

check_latest_release(&#34;tauri-apps&#34;, &#34;tauri&#34;)
`这个例子可以配合上一篇的 cron 定时任务——每天跑一次，有新版就飞书/Telegram 通知你。
## 实战四：AI 大模型 API（免费额度管够）
现在做大模型 API 的厂商太多了，而且每家都有免费额度：平台免费额度兼容格式Groq多模型免费OpenAI 兼容DeepSeek注册送 500 万 tokensOpenAI 兼容硅基流动多模型免费额度OpenAI 兼容Google Gemini免费 tier自有格式**好消息**：这些平台都兼容 OpenAI 的 API 格式，一套代码全搞定。import requests

def call_llm(api_key, base_url, model, prompt):
    &#34;&#34;&#34;通用大模型调用函数——兼容 OpenAI 格式的所有平台&#34;&#34;&#34;
    url = f&#34;{base_url}/chat/completions&#34;
    headers = {
        &#34;Authorization&#34;: f&#34;Bearer {api_key}&#34;,
        &#34;Content-Type&#34;: &#34;application/json&#34;
    }
    payload = {
        &#34;model&#34;: model,
        &#34;messages&#34;: [
            {&#34;role&#34;: &#34;system&#34;, &#34;content&#34;: &#34;你是 Python 技术专家，回答简洁&#34;},
            {&#34;role&#34;: &#34;user&#34;, &#34;content&#34;: prompt}
        ],
        &#34;temperature&#34;: 0.7,
        &#34;max_tokens&#34;: 500
    }

    resp = requests.post(url, headers=headers, json=payload)
    data = resp.json()
    return data[&#34;choices&#34;][0][&#34;message&#34;][&#34;content&#34;]

# 示例：调用 DeepSeek（替换成你自己的 key）
# result = call_llm(
#     api_key=&#34;sk-your-deepseek-key&#34;,
#     base_url=&#34;https://api.deepseek.com/v1&#34;,
#     model=&#34;deepseek-chat&#34;,
#     prompt=&#34;用 3 句话解释什么是装饰器&#34;
# )
# print(result)
`做产品的时候，可以把 AI 能力嵌入到任何地方——自动总结、智能分类、内容生成、代码审查。因为有免费额度，前期验证成本基本为零。
## 实战五：Unsplash 图片 API（让你的产品好看）
独立开发者的产品最大的问题之一是"看着像 demo"。Unsplash 免费 API 可以提供高质量配图。import requests

def search_photos(query, per_page=5):
    &#34;&#34;&#34;搜索 Unsplash 高质量图片&#34;&#34;&#34;
    url = &#34;https://api.unsplash.com/search/photos&#34;
    # 注册 https://unsplash.com/developers 获取 Access Key
    headers = {&#34;Authorization&#34;: &#34;Client-ID YOUR_ACCESS_KEY&#34;}
    params = {&#34;query&#34;: query, &#34;per_page&#34;: per_page}

    resp = requests.get(url, headers=headers, params=params)
    data = resp.json()

    print(f&#34;🖼️ 搜索 &#39;{query}&#39; 的结果：&#34;)
    for photo in data[&#34;results&#34;]:
        print(f&#34;  📷 {photo[&#39;description&#39;][:60] if photo[&#39;description&#39;] else &#39;无描述&#39;}&#34;)
        print(f&#34;     作者: {photo[&#39;user&#39;][&#39;name&#39;]}&#34;)
        print(f&#34;     原图: {photo[&#39;urls&#39;][&#39;regular&#39;]}&#34;)
        print(f&#34;     缩略图: {photo[&#39;urls&#39;][&#39;thumb&#39;]}\n&#34;)

# search_photos(&#34;coding setup&#34;)
`Unsplash 免费额度是每小时 50 次请求。对于博客配图、产品 Landing Page、文章封面这些场景绰绰有余。
## 进阶：打造通用 API 调用框架
上面 5 个例子覆盖了常见模式。但真实项目中你需要同时调多个 API，每个 API 的错误处理、重试、超时配置都不一样。下面是我在生产环境用的通用框架：import requests
import time
from functools import wraps
from typing import Callable

class APIClient:
    &#34;&#34;&#34;通用 API 客户端——错误处理 + 重试 + 限流 + 超时&#34;&#34;&#34;

    def __init__(self, base_url: str, headers: dict = None,
                 timeout: int = 10, max_retries: int = 3):
        self.base_url = base_url.rstrip(&#34;/&#34;)
        self.headers = headers or {}
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _request(self, method: str, path: str, **kwargs):
        &#34;&#34;&#34;核心请求方法——自动重试 + 指数退避&#34;&#34;&#34;
        url = f&#34;{self.base_url}{path}&#34;
        kwargs.setdefault(&#34;timeout&#34;, self.timeout)

        for attempt in range(self.max_retries):
            try:
                resp = self.session.request(method, url, **kwargs)

                # 限流：等到 Retry-After 再重试
                if resp.status_code == 429:
                    wait = int(resp.headers.get(&#34;Retry-After&#34;, 5))
                    print(f&#34;⚠️ 限流，{wait}s 后重试 (第 {attempt+1}/{self.max_retries} 次)&#34;)
                    time.sleep(wait)
                    continue

                # 服务端错误：指数退避
                if resp.status_code &gt;= 500:
                    wait = 2 ** attempt
                    print(f&#34;⚠️ 服务端错误 {resp.status_code}，{wait}s 后重试&#34;)
                    time.sleep(wait)
                    continue

                resp.raise_for_status()
                return resp.json()

            except requests.exceptions.Timeout:
                print(f&#34;⏱️ 请求超时 (第 {attempt+1}/{self.max_retries} 次)&#34;)
                if attempt == self.max_retries - 1:
                    raise
                time.sleep(2 ** attempt)

            except requests.exceptions.RequestException as e:
                print(f&#34;❌ 请求失败: {e}&#34;)
                if attempt == self.max_retries - 1:
                    raise
                time.sleep(2 ** attempt)

        raise Exception(f&#34;超过最大重试次数 {self.max_retries}&#34;)

    def get(self, path: str, **kwargs):
        return self._request(&#34;GET&#34;, path, **kwargs)

    def post(self, path: str, **kwargs):
        return self._request(&#34;POST&#34;, path, **kwargs)

# 使用示例
weather_client = APIClient(
    base_url=&#34;https://api.open-meteo.com/v1&#34;,
    timeout=5
)

data = weather_client.get(&#34;/forecast&#34;, params={
    &#34;latitude&#34;: 31.23,
    &#34;longitude&#34;: 121.47,
    &#34;daily&#34;: &#34;temperature_2m_max&#34;,
    &#34;forecast_days&#34;: 3
})
print(data[&#34;daily&#34;])
`这个框架你复制到任何项目里就能用。核心思想：**不要在每个 API 调用的地方重复写 try/except 和 retry 逻辑**——抽象成一层，所有 API 共用。

重试策略是关键：- **429 限流**：等 `Retry-After` 头指定的时间，不要不管不顾地重试- **5xx 服务端错误**：指数退避（1s → 2s → 4s）- **超时**：同样指数退避，每次翻倍等待
## 50+ 免费 API 速查表
下面这个表是我用过的、确认能用的免费 API。按场景分类：
### 天气 & 地理
API免费额度需要 Key亮点Open-Meteo无限否天气/历史/空气质量OpenWeatherMap1000次/天是当前天气 + 5天预报WeatherAPI100万次/月是天气 + 天文 + 时区IP-API45次/分钟否IP 转地理位置Nominatim1次/秒否地址 ↔ 坐标转换
### 金融 & 汇率
API免费额度需要 Key亮点Frankfurter无限否汇率 + 历史ExchangeRate-API1500次/月是多币种CoinGecko30次/分钟否加密货币全数据Alpha Vantage25次/天是股票数据
### 开发 & 工具
API免费额度需要 Key亮点GitHub REST API60次/时（无登录）否仓库/Issues/搜索GitLab API无限否私有仓库也支持JSONPlaceholder无限否假数据，开发测试用httpbin无限否调试 HTTP 请求
### AI & 机器学习
API免费额度需要 Key亮点Groq多模型免费是速度极快DeepSeek500万 tokens是性价比高Google Gemini免费 tier是多模态HuggingFace免费推理是海量开源模型Remove.bg50次/月是一键去背景
### 新闻 & 内容
API免费额度需要 Key亮点NewsAPI100次/天是全球新闻聚合HackerNews无限否科技圈热门Reddit JSON无限否任何 subreddit 加 .jsonDev.to无限否开发者文章
### 图片 & 媒体
API免费额度需要 Key亮点Unsplash50次/时是高质量图库Pexels200次/时是图片 + 视频Lorem Picsum无限否随机占位图Dog API无限否随机狗图
### 文本 & 翻译
API免费额度需要 Key亮点LibreTranslate无限（自部署）否开源翻译Lingva无限否Google 翻译代理Quotes REST无限否随机名言
### 其他实用
API免费额度需要 Key亮点Public APIs无限否API 目录本身也是个 APITheCatAPI无限是猫图 + 品种信息Pokemon API无限否宝可梦全数据OpenAI API$5 试用金是GPT 全家桶总量超过 50 个。其中带 "无限" 标记的可以直接上手，不需要注册。
## 真实场景组合：天气推送机器人
光看 API 列表没用，组合起来才有力量。我用 3 个免费 API 拼了一个天气预报推送：from APIClient import APIClient  # 上面写的通用框架
import json
from datetime import datetime

# 1. 坐标转城市名（Nominatim）
geo = APIClient(&#34;https://nominatim.openstreetmap.org&#34;)
geo.session.headers[&#34;User-Agent&#34;] = &#34;WeatherBot/1.0&#34;  # Nominatim 要求

# 2. 天气数据（Open-Meteo）
weather = APIClient(&#34;https://api.open-meteo.com/v1&#34;)

# 3. 推送通知（假设你有一个 webhook）
# notify = APIClient(&#34;https://your-webhook.com&#34;)

def daily_weather_report(lat, lon):
    &#34;&#34;&#34;每日天气报告&#34;&#34;&#34;
    # 获取城市名
    location = geo.get(&#34;/reverse&#34;, params={
        &#34;lat&#34;: lat, &#34;lon&#34;: lon, &#34;format&#34;: &#34;json&#34;
    })
    city = location.get(&#34;address&#34;, {}).get(&#34;city&#34;, &#34;未知城市&#34;)

    # 获取天气
    data = weather.get(&#34;/forecast&#34;, params={
        &#34;latitude&#34;: lat, &#34;longitude&#34;: lon,
        &#34;daily&#34;: [&#34;temperature_2m_max&#34;, &#34;temperature_2m_min&#34;,
                   &#34;precipitation_sum&#34;, &#34;weathercode&#34;],
        &#34;forecast_days&#34;: 1,
        &#34;timezone&#34;: &#34;Asia/Shanghai&#34;
    })

    today = data[&#34;daily&#34;]
    report = f&#34;&#34;&#34;
📅 {today[&#39;time&#39;][0]} {city}天气预报
━━━━━━━━━━━━━━━━━━
🌡️ 温度: {today[&#39;temperature_2m_min&#39;][0]}°C ~ {today[&#39;temperature_2m_max&#39;][0]}°C
🌧️ 降水: {today[&#39;precipitation_sum&#39;][0]}mm
💡 {&#39;今天有雨，出门带伞&#39; if today[&#39;precipitation_sum&#39;][0] &gt; 0 else &#39;天气不错&#39;}
&#34;&#34;&#34;

    print(report)
    # 推送到飞书/Telegram/邮件（具体代码见系列第 01 篇）
    return report

daily_weather_report(31.23, 121.47)
`三个 API，零费用，每天早上跑一次。配合上一篇文章的 cron 示例，这就是一个完整产品。
## 踩坑记录
写 API 调用这几年，有些坑重复踩：

**1. API Key 写死在代码里**

绝对不要。用环境变量：import os
api_key = os.environ[&#34;OPENAI_API_KEY&#34;]  # 正确
# api_key = &#34;sk-xxxxxxxx&#34;  # 错误：一推 GitHub 就泄露
`**2. 不检查 rate limit**

每个 API 都有额度。调用前查 `X-RateLimit-Remaining` 响应头：resp = requests.get(url)
remaining = resp.headers.get(&#34;X-RateLimit-Remaining&#34;)
if remaining and int(remaining) &lt; 10:
    print(&#34;⚠️ 额度预警，暂停使用&#34;)
    time.sleep(60)
`**3. 同步调多个 API，一个超时全卡住**

用 `concurrent.futures` 并行请求：from concurrent.futures import ThreadPoolExecutor

def fetch_all(urls):
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(
            lambda u: requests.get(u, timeout=5).json(),
            urls
        ))
    return results
`**4. API 改版不知道**

定时跑一次测试脚本，监控响应结构变化。最简单的办法：import hashlib

# 记录响应 key 结构的哈希
resp = requests.get(&#34;https://api.example.com/data&#34;).json()
structure_hash = hashlib.md5(
    str(sorted(resp.keys())).encode()
).hexdigest()

# 存到文件，下次对比，变了就告警
`
## 从这里开始
这篇文章和你上篇学的爬虫组合在一起，就是你作为独立开发者获取数据的全部武器：- **有 API → 用本文的方法调**- **没 API 但页面是静态的 → 用上篇的 BeautifulSoup 爬**- **页面是 SPA/JS 渲染的 → 用 Playwright**建议今天就找 2-3 个感兴趣的 API，用上面 `APIClient` 框架接一下。10 行代码就能把一个免费数据源接到你的项目里。接得多了，你会发现很多产品想法根本不需要自己造数据——世界上已经有免费的 API 在等你用了。**系列导航**：01 日常任务自动化
| 02 Web Scraping 实战
| **03 API 自动化** | 04 数据分析自动化

*Python 自动化实战系列，下一篇：数据分析自动化——Pandas 实战，把 API 拿回来的数据变成洞察。*