---
title: "Python 自动化实战：定时任务 & 监控脚本"
date: 2026-06-26
description: "把前四篇文章写的脚本全部串起来，用 Cron 让它们定时自动跑。加上系统监控和异常告警，打造一个不需要你管的自动化流水线。"
tags: [Python, 自动化, Cron, 监控, 独立开发]
draft: false
---

## 你写的那堆脚本还活着吗？
回顾一下前面四篇文章你写了什么：- **第一篇**：10 个日常自动化脚本——文件整理、批量改名、邮件发送- **第二篇**：GitHub Trending 爬虫 + 价格监控器- **第三篇**：调用 50+ 免费 API 拉数据- **第四篇**：Pandas 数据分析模板，自动出报表现在我问你一个扎心的问题：**这些脚本，你现在还在跑吗？**

我自己的教训是这样的：写完前三篇的脚本后，我把它们扔在服务器上，手动跑了两次，觉得效果不错。然后一个月没碰。等我想起来再跑一次，发现爬虫脚本因为目标网站改版挂了，API key 过期了，数据分析脚本拉到的 CSV 还是一个月前的。

**脚本不自动跑，等于没写。**

这不是鸡汤，是实打实的时间账。你花 2 小时写了个竞品价格监控器，然后每次都手动 `python monitor.py`，两个月跑了 3 次——平摊下来每次花费 40 分钟。如果写成 Cron 任务每小时自动跑一次，它在一个月内替你执行了 720 次检查。成本摊到每次检查，几乎为零。

这篇文章就是解决这个问题的。我会把你前面的所有脚本串起来，配上系统监控和异常告警，搭一个完整的自动化流水线。
## 自动化调度架构

整套架构分四层：**数据获取层**负责拉数据（爬虫、API、数据库导出），**分析处理层**负责把原始数据变成洞察（Pandas 聚合、异常检测），**系统监控层**保证服务器本身不出问题（磁盘、服务、SSL），**通知层**负责在你需要知道的时候把消息推到你的手机上。

Cron 是所有层的总调度器——它会按你设的时间表，准时把每一层的脚本叫起来干活。
## Cron 基础：别怕，五分钟学会
很多人听到 Cron 就觉得是运维的活。其实它简单到可笑——就一个文本文件，每行一条规则。# 编辑你的 crontab
crontab -e

# 格式：分 时 日 月 星期 命令
# ┌──── 分钟 (0-59)
# │ ┌──── 小时 (0-23)
# │ │ ┌──── 日期 (1-31)
# │ │ │ ┌──── 月份 (1-12)
# │ │ │ │ ┌──── 星期 (0=周日, 6=周六)
# │ │ │ │ │
# * * * * * 要执行的命令
`五个时间字段加一个命令。下面是最常用的几种写法：# 每天早上 8 点跑一次
0 8 * * * /usr/bin/python3 /home/ubuntu/scripts/daily_report.py

# 每小时跑一次（在整点）
0 * * * * /usr/bin/python3 /home/ubuntu/scripts/check_prices.py

# 每 30 分钟跑一次
*/30 * * * * /usr/bin/python3 /home/ubuntu/scripts/heartbeat.py

# 每周一早上 9 点
0 9 * * 1 /usr/bin/python3 /home/ubuntu/scripts/weekly_analysis.py

# 每月 1 号凌晨 2 点
0 2 1 * * /usr/bin/python3 /home/ubuntu/scripts/monthly_cleanup.py
`几个关键点：

**一定要写绝对路径**。`python3` 不行，写 `/usr/bin/python3`。脚本路径也一样，Cron 的环境变量和你登录 shell 不一样，`~` 和相对路径都不可靠。

**Cron 不会帮你管理虚拟环境**。如果你用 venv，要显式指定解释器路径：0 8 * * * /home/ubuntu/venv/bin/python /home/ubuntu/scripts/daily_report.py
`或者用个 shell 包装脚本，先 `source venv/bin/activate` 再跑 Python。我个人偏好前者——少一层中间文件，出问题更容易定位。

**Cron 日志去哪了？** Cron 默认把 stdout/stderr 发邮件给当前用户。如果你没配邮件服务（大部分 VPS 默认没配），这些输出就丢了。最简单的做法是手动重定向：0 8 * * * /usr/bin/python3 /home/ubuntu/scripts/daily_report.py &gt;&gt; /var/log/cron-daily.log 2&gt;&1
`但是这样日志会无限膨胀。更好的方案后面会说。
## 场景一：把爬虫变成定时任务
第二篇文章写了两个爬虫——GitHub Trending 抓取器和价格监控器。价格监控器里有个 `while True` 循环自己靠 `time.sleep()` 保持运行。这种方式有两个问题：- 脚本挂了就彻底停了，没有人会重启它- `while True` + `sleep(3600)` 太粗糙，你想改间隔还得改代码正确的做法：把循环去掉，每次跑一次检查，让 Cron 来控制节奏。#!/usr/bin/env python3
&#34;&#34;&#34;price_check.py —— 由 Cron 每小时调用一次&#34;&#34;&#34;
import requests
from bs4 import BeautifulSoup
import sys
import json
from pathlib import Path
from datetime import datetime

URL = &#34;https://example.com/product-page&#34;
STATE_FILE = Path(&#34;/home/ubuntu/data/last_price.json&#34;)
LOG_FILE = Path(&#34;/var/log/price_check.log&#34;)

def log(msg: str):
    timestamp = datetime.now().strftime(&#34;%Y-%m-%d %H:%M:%S&#34;)
    with open(LOG_FILE, &#34;a&#34;) as f:
        f.write(f&#34;[{timestamp}] {msg}\n&#34;)
    print(msg)

def get_price():
    headers = {
        &#34;User-Agent&#34;: &#34;Mozilla/5.0 (Windows NT 10.0; Win64; x64) &#34;
                      &#34;AppleWebKit/537.36 (KHTML, like Gecko) &#34;
                      &#34;Chrome/120.0.0.0 Safari/537.36&#34;
    }
    resp = requests.get(URL, headers=headers, timeout=15)
    soup = BeautifulSoup(resp.text, &#34;lxml&#34;)
    price_tag = soup.find(&#34;span&#34;, class_=&#34;price&#34;)
    if not price_tag:
        raise ValueError(&#34;未找到价格元素&#34;)
    price_text = price_tag.get_text(strip=True).replace(&#34;¥&#34;, &#34;&#34;).replace(&#34;,&#34;, &#34;&#34;).replace(&#34; &#34;, &#34;&#34;)
    return float(price_text)

def notify_change(old: float, new: float):
    # 直接调飞书的 Webhook（比 SMTP 邮件快得多，也更可靠）
    webhook_url = &#34;https://open.feishu.cn/open-apis/bot/v2/hook/xxx&#34;
    msg = {
        &#34;msg_type&#34;: &#34;text&#34;,
        &#34;content&#34;: {&#34;text&#34;: f&#34;📉 价格变动: ¥{old} → ¥{new}\n{URL}&#34;}
    }
    requests.post(webhook_url, json=msg, timeout=10)

def main():
    try:
        current_price = get_price()
        log(f&#34;当前价格: ¥{current_price}&#34;)

        if STATE_FILE.exists():
            last_data = json.loads(STATE_FILE.read_text())
            last_price = last_data[&#34;price&#34;]

            if current_price != last_price:
                notify_change(last_price, current_price)
                log(f&#34;价格变动: ¥{last_price} → ¥{current_price}&#34;)

        STATE_FILE.write_text(json.dumps({
            &#34;price&#34;: current_price,
            &#34;checked_at&#34;: datetime.now().isoformat()
        }))
    except Exception as e:
        log(f&#34;检查失败: {e}&#34;)
        sys.exit(1)

if __name__ == &#34;__main__&#34;:
    main()
`关键改动：- **状态持久化到文件**。每次跑完把当前价格写到 `last_price.json`，下次跑的时候读出来比较。这比依赖进程内变量可靠一万倍——脚本重启、机器重启都不丢状态。- **异常退出码**。`sys.exit(1)` 让 Cron 知道这次执行失败了。配合后面的监控方案，你会在失败时收到告警。- **飞书 Webhook 代替 SMTP 邮件**。Webhook 比 SMTP 快，不需要配邮件服务，而且消息直接推到手机。飞书、企业微信、钉钉都支持 Incoming Webhook，注册一个 bot 就能拿 URL。Cron 配置：# 每小时检查一次价格
0 * * * * /usr/bin/python3 /home/ubuntu/scripts/price_check.py
`
## 场景二：数据分析定期产出
第四篇文章写了 Pandas 分析模板。现在让它每周自动跑一次，产出报告。#!/usr/bin/env python3
&#34;&#34;&#34;weekly_analysis.py —— 每周一早上自动跑&#34;&#34;&#34;
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
from datetime import datetime, timedelta
from pathlib import Path

plt.rcParams[&#39;font.sans-serif&#39;] = [&#39;Noto Sans CJK SC&#39;]
plt.rcParams[&#39;axes.unicode_minus&#39;] = False

OUTPUT_DIR = Path(&#34;/home/ubuntu/reports&#34;)
OUTPUT_DIR.mkdir(exist_ok=True)

def pull_data_from_db():
    &#34;&#34;&#34;从 SQLite 拉取最近 7 天的用户行为数据&#34;&#34;&#34;
    import sqlite3
    conn = sqlite3.connect(&#34;/home/ubuntu/data/app_events.db&#34;)
    query = &#34;&#34;&#34;
        SELECT user_id, event, date, duration_sec
        FROM user_events
        WHERE date &gt;= date(&#39;now&#39;, &#39;-7 days&#39;)
    &#34;&#34;&#34;
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def analyze(df: pd.DataFrame):
    df[&#39;date&#39;] = pd.to_datetime(df[&#39;date&#39;])
    
    # 每日活跃用户
    dau = df.groupby(&#39;date&#39;)[&#39;user_id&#39;].nunique()
    
    # 事件分布
    event_counts = df.groupby(&#39;event&#39;).size().sort_values(ascending=False)
    
    # 用户留存
    user_days = df.groupby(&#39;user_id&#39;)[&#39;date&#39;].nunique()
    retention = (user_days &gt;= 3).mean() * 100  # 3日留存
    
    return dau, event_counts, retention

def plot_and_save(dau, event_counts):
    &#34;&#34;&#34;生成 PNG 图表&#34;&#34;&#34;
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    dau.plot(ax=axes[0], marker=&#39;o&#39;, color=&#39;#4A90D9&#39;)
    axes[0].set_title(&#39;过去7天 DAU&#39;)
    axes[0].set_ylabel(&#39;活跃用户数&#39;)
    
    event_counts.plot(kind=&#39;barh&#39;, ax=axes[1], color=&#39;#E85D3F&#39;)
    axes[1].set_title(&#39;事件分布&#39;)
    
    plt.tight_layout()
    chart_path = OUTPUT_DIR / f&#34;weekly_report_{datetime.now().strftime(&#39;%Y%W&#39;)}.png&#34;
    plt.savefig(chart_path, dpi=150)
    return chart_path

def push_to_feishu(chart_path, dau, retention):
    &#34;&#34;&#34;把图表和关键指标推到飞书&#34;&#34;&#34;
    today = datetime.now().strftime(&#34;%m月%d日&#34;)
    avg_dau = dau.mean()
    
    # 先发文本指标
    webhook = &#34;https://open.feishu.cn/open-apis/bot/v2/hook/xxx&#34;
    msg = {
        &#34;msg_type&#34;: &#34;interactive&#34;,
        &#34;card&#34;: {
            &#34;header&#34;: {&#34;title&#34;: {&#34;content&#34;: f&#34;📊 周报 {today}&#34;, &#34;tag&#34;: &#34;plain_text&#34;}},
            &#34;elements&#34;: [
                {&#34;tag&#34;: &#34;div&#34;, &#34;text&#34;: {&#34;content&#34;: f&#34;平均 DAU：**{avg_dau:.0f}**\n3日留存：**{retention:.1f}%**&#34;, &#34;tag&#34;: &#34;lark_md&#34;}},
                {&#34;tag&#34;: &#34;img&#34;, &#34;img_key&#34;: &#34;NEED_UPLOAD_FIRST&#34;, &#34;alt&#34;: {&#34;content&#34;: &#34;周趋势图&#34;, &#34;tag&#34;: &#34;plain_text&#34;}}
            ]
        }
    }
    requests.post(webhook, json=msg, timeout=10)

def main():
    df = pull_data_from_db()
    dau, event_counts, retention = analyze(df)
    chart_path = plot_and_save(dau, event_counts)
    push_to_feishu(chart_path, dau, retention)
    print(f&#34;周报已生成: {chart_path}&#34;)

if __name__ == &#34;__main__&#34;:
    main()
`Cron 配置：# 每周一早上 8 点跑周报
0 8 * * 1 /usr/bin/python3 /home/ubuntu/scripts/weekly_analysis.py
`这里有一个实际经验：**飞书卡片消息内嵌图片需要先上传图片获取 image_key**。上面代码里我写了 `"NEED_UPLOAD_FIRST"` 占位，生产代码需要调用飞书的图片上传 API。如果嫌麻烦，最简单的方式是用飞书文本消息只发数据指标，图存在服务器上你手动看，或者用 Telegram Bot——Telegram 可以直接通过 `sendPhoto` 接口传本地文件，不需要预上传。# Telegram 发图片——比飞书省一步
def push_to_telegram(chart_path, text):
    bot_token = &#34;YOUR_BOT_TOKEN&#34;
    chat_id = &#34;YOUR_CHAT_ID&#34;
    
    # 发文字
    requests.post(
        f&#34;https://api.telegram.org/bot{bot_token}/sendMessage&#34;,
        json={&#34;chat_id&#34;: chat_id, &#34;text&#34;: text}
    )
    # 直接发图
    with open(chart_path, &#34;rb&#34;) as f:
        requests.post(
            f&#34;https://api.telegram.org/bot{bot_token}/sendPhoto&#34;,
            data={&#34;chat_id&#34;: chat_id},
            files={&#34;photo&#34;: f}
        )
`
## 场景三：系统监控——你的服务器还活着吗？
前面讲的都是业务脚本。但还有一个问题：就算脚本写对了、Cron 配对了，**服务器挂了就全完蛋**。你需要几个最基础的监控脚本。
### 磁盘使用率告警
最常见的翻车场景：爬虫跑了几周，存了一堆数据，磁盘满了。SQLite 写入失败、日志写不进去，你完全不知道，直到某天用户说功能坏了。#!/usr/bin/env python3
&#34;&#34;&#34;disk_monitor.py —— 每小时检查磁盘&#34;&#34;&#34;
import shutil
import requests
import sys

THRESHOLD = 80  # 超过 80% 就告警

def check_and_alert():
    usage = shutil.disk_usage(&#34;/&#34;)
    used_pct = (usage.used / usage.total) * 100
    
    if used_pct &gt; THRESHOLD:
        webhook = &#34;https://open.feishu.cn/open-apis/bot/v2/hook/xxx&#34;
        msg = {
            &#34;msg_type&#34;: &#34;text&#34;,
            &#34;content&#34;: {
                &#34;text&#34;: (
                    f&#34;🚨 磁盘告警\n&#34;
                    f&#34;使用率：{used_pct:.1f}%（阈值 {THRESHOLD}%）\n&#34;
                    f&#34;已用：{usage.used // (1024**3)}GB / {usage.total // (1024**3)}GB\n&#34;
                    f&#34;主机：price-monitor-server&#34;
                )
            }
        }
        requests.post(webhook, json=msg, timeout=10)
        return False
    return True

if __name__ == &#34;__main__&#34;:
    ok = check_and_alert()
    if not ok:
        print(f&#34;磁盘使用率超过 {THRESHOLD}%&#34;)
    sys.exit(0 if ok else 1)
`
### 服务健康检查
如果你还跑了 Web 服务（比如 Flask API、爬虫管理面板），需要确认它还活着：#!/usr/bin/env python3
&#34;&#34;&#34;health_check.py —— 每5分钟检查服务是否响应&#34;&#34;&#34;
import requests
import sys
import time

SERVICES = [
    {&#34;name&#34;: &#34;API 服务&#34;, &#34;url&#34;: &#34;http://localhost:5000/health&#34;},
    {&#34;name&#34;: &#34;爬虫面板&#34;, &#34;url&#34;: &#34;http://localhost:8080/ping&#34;},
]

def check_services():
    all_ok = True
    for svc in SERVICES:
        try:
            r = requests.get(svc[&#34;url&#34;], timeout=5)
            if r.status_code != 200:
                print(f&#34;❌ {svc[&#39;name&#39;]} 返回 {r.status_code}&#34;)
                all_ok = False
            else:
                print(f&#34;✅ {svc[&#39;name&#39;]} OK&#34;)
        except Exception as e:
            print(f&#34;❌ {svc[&#39;name&#39;]} 不可达: {e}&#34;)
            all_ok = False
    return all_ok

if __name__ == &#34;__main__&#34;:
    ok = check_services()
    sys.exit(0 if ok else 1)
`
### SSL 证书到期检查
如果你的产品有自己的域名，证书到期后用户访问会看到安全警告——这对独立产品的转化是致命的。#!/usr/bin/env python3
&#34;&#34;&#34;ssl_check.py —— 每天检查 SSL 证书到期日&#34;&#34;&#34;
import ssl
import socket
from datetime import datetime, timedelta
import requests
import sys

DOMAINS = [&#34;zhouyang.dev&#34;, &#34;your-product.com&#34;]
WARN_DAYS = 30

def get_cert_expiry(domain: str):
    ctx = ssl.create_default_context()
    with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
        s.settimeout(10)
        s.connect((domain, 443))
        cert = s.getpeercert()
        expiry_str = cert[&#39;notAfter&#39;]
        # &#39;Jun 26 23:59:59 2026 GMT&#39; → datetime
        return datetime.strptime(expiry_str, &#34;%b %d %H:%M:%S %Y %Z&#34;)

def main():
    alerts = []
    for domain in DOMAINS:
        try:
            expiry = get_cert_expiry(domain)
            days_left = (expiry - datetime.now()).days
            print(f&#34;{domain}: {days_left} 天后到期 ({expiry.date()})&#34;)
            if days_left &lt;= WARN_DAYS:
                alerts.append(f&#34;⚠️ {domain} 证书 {days_left} 天后到期&#34;)
        except Exception as e:
            alerts.append(f&#34;❌ {domain} 证书检查失败: {e}&#34;)
    
    if alerts:
        webhook = &#34;https://open.feishu.cn/open-apis/bot/v2/hook/xxx&#34;
        requests.post(webhook, json={
            &#34;msg_type&#34;: &#34;text&#34;,
            &#34;content&#34;: {&#34;text&#34;: &#34;🔒 SSL 证书提醒\n&#34; + &#34;\n&#34;.join(alerts)}
        }, timeout=10)
        sys.exit(1)

if __name__ == &#34;__main__&#34;:
    main()
`Cron 配置汇总：# 系统监控
0 * * * * /usr/bin/python3 /home/ubuntu/scripts/disk_monitor.py
*/5 * * * * /usr/bin/python3 /home/ubuntu/scripts/health_check.py
0 9 * * * /usr/bin/python3 /home/ubuntu/scripts/ssl_check.py

# 业务脚本
0 * * * * /usr/bin/python3 /home/ubuntu/scripts/price_check.py
0 8 * * 1 /usr/bin/python3 /home/ubuntu/scripts/weekly_analysis.py
0 6 * * * /usr/bin/python3 /home/ubuntu/scripts/github_trending.py
`
## 最佳实践：三个要命的问题
写了 5 篇自动化文章，我发现有三个问题如果不提前处理，会在你上线两三周后集中爆发。
### 1. 日志管理
每个脚本都往日志文件追加，几周后你能收获一个 2GB 的纯文本文件。用 `logrotate` 解决：# /etc/logrotate.d/python-cron
/var/log/cron-*.log {
    daily               # 每天转储一次
    rotate 14           # 保留 14 天
    compress            # 压缩旧日志
    delaycompress       # 延迟一天再压缩
    missingok           # 文件不存在不报错
    notifempty          # 空文件不转储
    copytruncate        # 复制后清空（不中断正在写入的进程）
}
`然后统一日志格式：import logging

logging.basicConfig(
    filename=&#39;/var/log/cron-price_check.log&#39;,
    level=logging.INFO,
    format=&#39;%(asctime)s [%(levelname)s] %(message)s&#39;,
    datefmt=&#39;%Y-%m-%d %H:%M:%S&#39;
)

logger = logging.getLogger(__name__)
logger.info(f&#34;价格检查完成: ¥{current_price}&#34;)
`
### 2. 告警风暴
凌晨三点磁盘满了一次，你的飞书就收到一条告警。但如果脚本有问题，每次跑都失败，你会在一小时内收到 60 条同样的消息。这叫告警风暴——我亲身经历过，手机直接被震到没电。

解法是加简单的去重：import hashlib
from pathlib import Path

def should_alert(message: str, cooldown_minutes: int = 60) -&gt; bool:
    &#34;&#34;&#34;相同消息在 cooldown 时间内不重复发送&#34;&#34;&#34;
    alert_dir = Path(&#34;/tmp/alerts_sent&#34;)
    alert_dir.mkdir(exist_ok=True)
    
    msg_hash = hashlib.md5(message.encode()).hexdigest()
    alert_file = alert_dir / msg_hash
    
    if alert_file.exists():
        mtime = alert_file.stat().st_mtime
        if time.time() - mtime &lt; cooldown_minutes * 60:
            return False  # 冷却期内，跳过
    
    alert_file.touch()
    return True

# 使用
msg = f&#34;磁盘使用率 {used_pct:.1f}%&#34;
if should_alert(msg, cooldown_minutes=60):
    send_notification(msg)
`
### 3. Cron 任务互相踩踏
如果你的数据分析脚本要跑 10 分钟，但 Cron 每小时跑一次——没问题，它们不会重叠。除非你设了 `*/5 * * * *`，脚本却要跑 10 分钟。这时新的实例会启动，和旧实例一起跑，两份分析结果互相覆盖。

用文件锁防止重叠执行：import fcntl
import sys

def acquire_lock():
    &#34;&#34;&#34;确保同一时间只有一个实例在跑&#34;&#34;&#34;
    lock_file = open(&#34;/tmp/weekly_analysis.lock&#34;, &#34;w&#34;)
    try:
        fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return lock_file
    except BlockingIOError:
        print(&#34;上一个实例还在跑，跳过本次执行&#34;)
        sys.exit(0)

# 脚本开头
lock = acquire_lock()
# ... 业务逻辑 ...
``fcntl.LOCK_NB` 是非阻塞锁——如果拿不到锁就立刻退出，不做任何事，等 Cron 下一次调度。
## 从这里开始
这篇文章是整个 Python 自动化系列的终点。回顾一下你学到了什么：篇目能力你能做什么01 日常任务文件系统操作批量改名、整理文件、自动发邮件02 Web Scraping数据获取爬公开网页、价格监控、信息聚合03 API 自动化结构化数据调用 50+ 免费 API，接入外部数据源04 Pandas 分析数据洞察用户行为分析、趋势图、留存报表05 定时调度自动化运行让上面所有脚本定时跑，配上监控告警五篇文章串起来就是一条完整的自动化流水线：**获取数据 → 分析数据 → 产出洞察 → 推送通知**。你现在有模板和工具，差的只是找到一个你想持续追踪的数据源。

今天建议做的事：从你之前写的脚本里挑一个最有价值的（比如价格监控、数据分析），按这篇文章的方式改写成无状态单次执行脚本，配到 Cron 里，让它明天早上自己跑一次。看着飞书/Telegram 弹出第一条自动化消息的时候，你会感谢自己花了一个小时做这件事的。**系列导航**：01 日常任务自动化
| 02 Web Scraping 实战
| 03 API 自动化
| 04 数据分析自动化
| **05 定时任务 & 监控**

*Python 自动化实战系列完结。下一篇系列预告：AI 编程工具链——Prompt Engineering 实战手册。*