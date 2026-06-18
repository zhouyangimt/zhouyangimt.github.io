---
title: "用Python自动化你的10个日常重复工作（附完整代码）"
date: 2026-06-05
tags: ["Python", "自动化", "独立开发"]
description: "文件整理、邮件发送、数据报表……这些烦人的重复工作，让Python替你干。"
---

![Python自动化编程](https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=1200&h=630&fit=crop)

## 你每天在浪费多少时间？

想一想：重命名一堆文件、整理下载文件夹、定时发邮件、从Excel里提取数据……这些事每天都在消耗你。

Python最擅长干这个。下面10个脚本，复制即用。

## 1. 批量重命名文件

```python
import os
path = "./images"
for i, f in enumerate(os.listdir(path)):
    os.rename(f"{path}/{f}", f"{path}/photo_{i+1:03d}.jpg")
```

## 2. 自动整理下载文件夹

```python
import os, shutil
downloads = os.path.expanduser("~/Downloads")
for f in os.listdir(downloads):
    ext = f.split(".")[-1].lower()
    dest = os.path.join(downloads, ext)
    os.makedirs(dest, exist_ok=True)
    shutil.move(os.path.join(downloads, f), dest)
```

## 3. 定时发送邮件

```python
import smtplib
from email.mime.text import MIMEText

msg = MIMEText("这是自动发送的日报")
msg["Subject"] = "每日报告"
msg["From"] = "you@qq.com"
msg["To"] = "boss@qq.com"

with smtplib.SMTP_SSL("smtp.qq.com", 465) as s:
    s.login("you@qq.com", "授权码")
    s.send_message(msg)
```

## 4. 批量压缩图片

```python
from PIL import Image
import os

for f in os.listdir("photos"):
    if f.endswith((".jpg", ".png")):
        img = Image.open(f"photos/{f}")
        img.save(f"compressed/{f}", quality=60, optimize=True)
```

## 5. Excel数据提取

```python
import pandas as pd
df = pd.read_excel("sales.xlsx")
summary = df.groupby("region")["revenue"].sum()
summary.to_csv("summary.csv")
```

## 6. 网页定时截图

```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://your-site.com")
    page.screenshot(path="screenshot.png")
```

## 7. 批量下载文件

```python
import requests
urls = ["https://example.com/file1.pdf", "https://example.com/file2.pdf"]
for i, url in enumerate(urls):
    r = requests.get(url)
    with open(f"download_{i}.pdf", "wb") as f:
        f.write(r.content)
```

## 8. 监控网站变化

```python
import requests, hashlib, time

url = "https://target-site.com"
prev = ""
while True:
    content = requests.get(url).text
    h = hashlib.md5(content.encode()).hexdigest()
    if h != prev:
        print("网站更新了!")
        prev = h
    time.sleep(3600)
```

## 9. 自动生成周报

```python
from datetime import datetime, timedelta
week = datetime.now() - timedelta(days=7)
start = week.strftime("%m.%d")
end = datetime.now().strftime("%m.%d")
print(f"本周工作总结 ({start} - {end})")
print("完成事项:")
print("1. ")
print("2. ")
print("下周计划:")
print("1. ")
```

## 10. 数据备份脚本

```python
import shutil, os
from datetime import datetime

src = "/path/to/important/data"
dst = f"/backup/backup_{datetime.now().strftime('%Y%m%d')}"
shutil.copytree(src, dst)
print(f"备份完成: {dst}")
```

## 把这些串起来

用cron定时任务每天跑一遍:

```bash
# 每天早8点自动整理、备份
0 8 * * * python3 /path/to/auto.py
```

依赖安装: `pip install pillow pandas openpyxl playwright`

> 这些脚本任何一个单独拎出来都能省你每天至少10分钟。10个加起来就是小半天。

![让代码替你工作](https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=1200&h=630&fit=crop)
