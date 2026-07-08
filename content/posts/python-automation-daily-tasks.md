---
title: "用Python自动化你的10个日常重复工作（附完整代码）"
date: 2026-06-05
description: "文件整理、邮件发送、数据报表……这些烦人的重复工作，让Python替你干。"
tags: [Python, 自动化, 独立开发]
draft: false
---

![](https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=1200&h=630&fit=crop)
## 你每天在浪费多少时间？
想一想：重命名一堆文件、整理下载文件夹、定时发邮件、从Excel里提取数据……这些事每天都在消耗你。

Python最擅长干这个。下面10个脚本，复制即用。
## 1. 批量重命名文件
import os
path = &#34;./images&#34;
for i, f in enumerate(os.listdir(path)):
    os.rename(f&#34;{path}/{f}&#34;, f&#34;{path}/photo_{i+1:03d}.jpg&#34;)
`
## 2. 自动整理下载文件夹
import os, shutil
downloads = os.path.expanduser(&#34;~/Downloads&#34;)
for f in os.listdir(downloads):
    ext = f.split(&#34;.&#34;)[-1].lower()
    dest = os.path.join(downloads, ext)
    os.makedirs(dest, exist_ok=True)
    shutil.move(os.path.join(downloads, f), dest)
`
## 3. 定时发送邮件
import smtplib
from email.mime.text import MIMEText

msg = MIMEText(&#34;这是自动发送的日报&#34;)
msg[&#34;Subject&#34;] = &#34;每日报告&#34;
msg[&#34;From&#34;] = &#34;you@qq.com&#34;
msg[&#34;To&#34;] = &#34;boss@qq.com&#34;

with smtplib.SMTP_SSL(&#34;smtp.qq.com&#34;, 465) as s:
    s.login(&#34;you@qq.com&#34;, &#34;授权码&#34;)
    s.send_message(msg)
`
## 4. 批量压缩图片
from PIL import Image
import os

for f in os.listdir(&#34;photos&#34;):
    if f.endswith((&#34;.jpg&#34;, &#34;.png&#34;)):
        img = Image.open(f&#34;photos/{f}&#34;)
        img.save(f&#34;compressed/{f}&#34;, quality=60, optimize=True)
`
## 5. Excel数据提取
import pandas as pd
df = pd.read_excel(&#34;sales.xlsx&#34;)
summary = df.groupby(&#34;region&#34;)[&#34;revenue&#34;].sum()
summary.to_csv(&#34;summary.csv&#34;)
`
## 6. 网页定时截图
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(&#34;https://your-site.com&#34;)
    page.screenshot(path=&#34;screenshot.png&#34;)
`
## 7. 批量下载文件
import requests
urls = [&#34;https://example.com/file1.pdf&#34;, &#34;https://example.com/file2.pdf&#34;]
for i, url in enumerate(urls):
    r = requests.get(url)
    with open(f&#34;download_{i}.pdf&#34;, &#34;wb&#34;) as f:
        f.write(r.content)
`
## 8. 监控网站变化
import requests, hashlib, time

url = &#34;https://target-site.com&#34;
prev = &#34;&#34;
while True:
    content = requests.get(url).text
    h = hashlib.md5(content.encode()).hexdigest()
    if h != prev:
        print(&#34;网站更新了!&#34;)
        prev = h
    time.sleep(3600)
`
## 9. 自动生成周报
from datetime import datetime, timedelta
week = datetime.now() - timedelta(days=7)
start = week.strftime(&#34;%m.%d&#34;)
end = datetime.now().strftime(&#34;%m.%d&#34;)
print(f&#34;本周工作总结 ({start} - {end})&#34;)
print(&#34;完成事项:&#34;)
print(&#34;1. &#34;)
print(&#34;2. &#34;)
print(&#34;下周计划:&#34;)
print(&#34;1. &#34;)
`
## 10. 数据备份脚本
import shutil, os
from datetime import datetime

src = &#34;/path/to/important/data&#34;
dst = f&#34;/backup/backup_{datetime.now().strftime(&#39;%Y%m%d&#39;)}&#34;
shutil.copytree(src, dst)
print(f&#34;备份完成: {dst}&#34;)
`
## 把这些串起来
用cron定时任务每天跑一遍:# 每天早8点自动整理、备份
0 8 * * * python3 /path/to/auto.py
`依赖安装: `pip install pillow pandas openpyxl playwright`这些脚本任何一个单独拎出来都能省你每天至少10分钟。10个加起来就是小半天。![](https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=1200&h=630&fit=crop)