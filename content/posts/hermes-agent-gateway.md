---
title: "Hermes Agent 深度指南 05：多平台集成——飞书/Telegram/Discord"
date: 2026-06-21
tags: ["AI", "Hermes", "工具教程", "自动化"]
description: "一个 Hermes 实例同时接入飞书、Telegram、Discord，多平台消息智能路由，让 AI 助手真正无处不在。配置详解 + 实战踩坑全记录。"
---

这是 Hermes Agent 深度指南系列的第五篇。前四篇分别是[入门指南](/posts/hermes-agent-guide/)、[配置详解](/posts/hermes-agent-config/)、[Skills 系统](/posts/hermes-agent-skills/)和 [Cron 定时任务](/posts/hermes-agent-cron/)。

上一篇文章讲了 Cron——Hermes 到点自动干活，但干完活的结果得让你收到。你不可能天天盯着终端看吧？你得在手机上、飞书上、Telegram 上收到消息。这就是今天要解决的问题：**多平台集成**。

## 为什么需要多平台

先说说真实场景。我自己是这样用的：

- **飞书**：工作相关。代码审查结果、服务器告警、每日 AI 资讯，这些跟团队有关的东西走飞书群聊。
- **Telegram**：个人助理。博客部署通知、RSS 摘要、临时让 AI 搜个东西，走 Telegram Bot——轻量、手机通知即时。
- **Discord**：社区互动。偶尔在 Discord 群里接一些朋友的问题，让 Hermes 帮忙回。

三个平台，三种场景，一个 Hermes 实例。不是三个实例，不是一个平台配一次——**一个实例接入所有平台，按规则智能分发**。

## Gateway 架构

先搞清楚 Hermes Gateway 是怎么工作的：

![Hermes Gateway 多平台架构图](/images/hermes-gateway-architecture.png)

Gateway 是一个独立的进程，它做的事很简单：

1. **接收消息**：监听各平台的 webhook 或长连接
2. **标准化**：把飞书的富文本、Telegram 的 Markdown、Discord 的 Embed 统一转成内部格式
3. **路由判断**：看这条消息来自哪、内容是什么、发消息的人是谁，决定交给哪个 Agent 处理
4. **返回结果**：把 Agent 的回复转回对应平台的格式，发回去

关键设计：**Gateway 和 Agent 是解耦的**。Gateway 挂了不影响 Agent 推理，Agent 推理慢不影响 Gateway 收消息。两者通过内部 API 通信。

## 接入飞书

飞书的接入相对复杂，因为涉及应用创建和权限审批。但好处是飞书的富文本能力最强，卡片消息、按钮交互都能搞。

### Step 1：创建飞书应用

先去 [飞书开放平台](https://open.feishu.cn) 创建一个企业自建应用：

1. 创建应用 → 选「企业自建应用」→ 随便起个名（比如「Hermes 助手」）
2. 添加能力：**机器人**
3. 权限配置，至少勾选：
   - `im:message` — 获取消息
   - `im:message:send_as_bot` — 发送消息
   - `im:chat` — 获取群聊信息（可选）
4. 安全设置里配好 IP 白名单（你的服务器 IP）
5. 发布应用 → 让管理员审批通过

### Step 2：在 Hermes 里配置

拿到 App ID 和 App Secret 之后，用 CLI 配置：

```bash
hermes gateway setup
# 选 Feishu → 输入 App ID → 输入 App Secret → 输入 Verification Token
```

或者直接改配置文件：

```yaml
# ~/.hermes/config.yaml
gateway:
  enabled: true
  listen: "0.0.0.0:8080"

  platforms:
    feishu:
      enabled: true
      app_id: "cli_xxxxxxxxxxxx"
      app_secret: ${FEISHU_APP_SECRET}
      verification_token: ${FEISHU_VERIFY_TOKEN}
      encrypt_key: ${FEISHU_ENCRYPT_KEY}  # 如果启用了加密
```

启动后，Hermes 会自己处理飞书的事件订阅 URL 验证——不用你手动配回调地址。

### Step 3：启动并测试

```bash
hermes gateway run
# 输出：Gateway listening on :8080
#       ✅ Feishu connected
#       ✅ Telegram connected
#       ⚠️  Discord not configured
```

然后在飞书里 @机器人 发一条消息「你好」，应该能看到回复。

### 飞书特有的能力

飞书的富文本消息格式比文字强太多。你可以让 Hermes 发卡片消息：

```
Hermes，把我的服务器巡检结果用飞书卡片发到运维群。
卡片格式：
- 标题：🖥️ 服务器巡检 | 2026-06-21 14:00
- 内容用表格展示，异常项标红
- 底部加一个「查看详情」按钮，链接到 Grafana
```

Hermes 会自动调用飞书的卡片消息 API，效果是：

```
┌─────────────────────────────────┐
│ 🖥️ 服务器巡检 | 2026-06-21 14:00 │
│                                 │
│ 服务器    CPU   内存   磁盘  状态 │
│ web-01   23%   45%   62%   ✅   │
│ db-01    87%   91%   94%   🔴   │
│ cache-01 12%   38%   18%   ✅   │
│                                 │
│       [查看 Grafana 详情]        │
└─────────────────────────────────┘
```

## 接入 Telegram

Telegram 的配置简单很多——BotFather 创建机器人，拿 Token，完事。

### Step 1：创建 Bot

在 Telegram 里搜索 `@BotFather`，对话：

```
/newbot
→ 输入 bot 名字：Hermes Assistant
→ 输入 bot 用户名：hermes_my_bot（必须以 bot 结尾）
→ 拿到 Token：1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

建议顺手设几个命令：

```
/setcommands
→ 选你的 bot
→ 输入：
start - 开始对话
help - 查看帮助
model - 切换模型
status - 查看状态
```

### Step 2：配置

```yaml
gateway:
  platforms:
    telegram:
      enabled: true
      token: ${TELEGRAM_BOT_TOKEN}
      # 可选：限制只有这些用户能用
      allowed_users:
        - 123456789   # 你的 Telegram user ID
        - 987654321
```

如果你想让 bot 加入群聊也能用，去 BotFather 里 `/setprivacy` 设为 Disabled。

### Step 3：设置 Webhook

Telegram 支持两种模式：长轮询（polling）和 Webhook。Hermes 推荐 Webhook，你需要一个公网域名或 IP：

```yaml
gateway:
  platforms:
    telegram:
      webhook_url: "https://your-server.com/hermes/telegram"
```

如果没有公网 IP，可以用 Cloudflare Tunnel 或 ngrok 临时穿透：

```bash
# 用 ngrok 临时测试
ngrok http 8080
# 拿到 https://xxxx.ngrok.io 后填到 webhook_url
```

Hermes 启动时会自动调用 Telegram API 注册 webhook，不用手动 curl。

### Telegram 特有的坑

**坑 1：消息长度限制**。Telegram 单条消息最多 4096 字符。Hermes 遇到长回复会自动分段，但如果你的回复是代码块，分段会截断代码块标记。解决办法：在任务描述里加一句「如果回复超过 3000 字符，优先精简而不是分段」。

**坑 2：Markdown 解析**。Telegram 的 Markdown 是阉割版——支持 `**粗体**`、`_斜体_`、`` `代码` ``，但不支持表格、标题。Hermes 会自动降级格式，但你写 prompt 的时候注意别让 Agent 输出表格。

## 接入 Discord

Discord 的配置介于飞书和 Telegram 之间：比 Telegram 复杂（OAuth2 那一套），比飞书简单（不用等审批）。

### Step 1：创建应用

去 [Discord Developer Portal](https://discord.com/developers/applications)：

1. New Application → 起名
2. 左侧 Bot → Add Bot → Reset Token（复制下来）
3. 开启 Privileged Gateway Intents：
   - MESSAGE CONTENT INTENT（必须，否则收不到消息内容）
   - SERVER MEMBERS INTENT（可选，识别用户）
4. OAuth2 → URL Generator：
   - 勾选 `bot` + `applications.commands`
   - Bot Permissions：Send Messages, Read Messages, Read Message History, Use Slash Commands
   - 用生成的 URL 邀请 bot 进服务器

### Step 2：配置

```yaml
gateway:
  platforms:
    discord:
      enabled: true
      token: ${DISCORD_BOT_TOKEN}
      application_id: "1234567890123456789"
      # 可选：监听特定频道
      allowed_channels:
        - "1234567890123456789"   # #hermes-test
        - "9876543210987654321"   # #dev-chat
      # 可选：只回复 @mention 的消息
      mention_only: false
```

Discord 走的是 WebSocket 长连接，不需要你提供 webhook URL。Hermes 启动后自动连接 Discord Gateway。

### Step 3：Slash Commands

Discord 支持 Slash Commands，配置完 Hermes 可以注册一批命令：

```yaml
gateway:
  platforms:
    discord:
      slash_commands: true
      commands:
        - name: ask
          description: "直接问 Hermes 一个问题"
        - name: summarize
          description: "总结最近的聊天内容"
        - name: translate
          description: "翻译消息"
```

注册完后，在 Discord 里打 `/ask 怎么用 Python 写一个 WebSocket 客户端`，Hermes 就会回复。

### Discord 的小细节

Discord 的 Embed 消息很炫，Hermes 也能发。在 prompt 里可以这样写：

```
用 Discord Embed 格式回复，颜色用 #00ff00，标题加粗，字段用 inline 排列。
```

但别滥用——Embed 在手机上显示效果一般，大段文字还是用普通消息。

## 多平台消息路由

三个平台接好了，但有个问题：Cron 任务跑完的结果该发到哪？你在 Telegram 上问的东西不该跑到飞书群里去。这就涉及到**消息路由规则**。

Hermes Gateway 的路由逻辑：

```yaml
gateway:
  routing:
    # 规则从上到下匹配，命中即停止
    rules:
      # 规则 1：Cron 任务的输出，按任务配置的通知渠道发
      - source: cron
        notify: "{{.task.notify.channel}}"

      # 规则 2：来自飞书运维群的消息，只路由到运维相关的 Skills
      - source: feishu
        chat_id: "oc_xxxxxxxxxxxx"
        skills: [server-health, deployment]
        model: deepseek-v4-pro

      # 规则 3：来自 Discord 的消息，用便宜模型
      - source: discord
        model: gemini-3-flash
        provider: google

      # 规则 4：Telegram 私聊，完整能力
      - source: telegram
        chat_type: private
        skills: [*]          # 所有 Skills 都可用
        toolsets: [*]        # 所有 toolsets

      # 默认：兜底规则
      - default: true
        model: deepseek-v4-pro
```

这个规则表的价值在于：不同场景用不同模型，既保证体验又控制成本。Discord 上随便聊用 Gemini Flash（便宜），飞书工作群用 DeepSeek V4（能打），Telegram 私聊给自己干活也上满配。

### 按人员权限控制

你不想让 Discord 群里的任何陌生人都能调你的 terminal 工具吧？

```yaml
gateway:
  permissions:
    admin:
      - telegram:123456789          # 你自己，完整权限
    trusted:
      - feishu:ou_xxxxxxx           # 同事，可以用 web_search 但不能写文件
      - discord:987654321098765432
    guest:
      - discord:*                   # 其他人，只能聊天
```

每个人群的权限对应不同的 toolsets：

```yaml
  permission_sets:
    admin:
      toolsets: [*]
      skills: [*]
    trusted:
      toolsets: [web, file, search]
      skills: [public-*]            # 只有 public- 开头的 Skills
    guest:
      toolsets: [web]
      skills: []                    # 没有任何 Skills
```

## 实战：用 Gateway + Cron 搭建个人助理

把前几篇的东西串起来。假设你现在想做一个个人助理，配置如下：

```yaml
# ~/.hermes/config.yaml 完整配置
gateway:
  enabled: true
  listen: "0.0.0.0:8080"

  platforms:
    feishu:
      enabled: true
      app_id: ${FEISHU_APP_ID}
      app_secret: ${FEISHU_APP_SECRET}
      verification_token: ${FEISHU_VERIFY_TOKEN}

    telegram:
      enabled: true
      token: ${TELEGRAM_BOT_TOKEN}
      webhook_url: "https://hermes.yourdomain.com/telegram"
      allowed_users: [123456789]

    discord:
      enabled: false  # 先不开

  routing:
    rules:
      - source: cron
        notify: "{{.task.notify.channel}}"

      - source: feishu
        chat_id: "oc_xxxxx"
        skills: [server-health]
        model: deepseek-v4-pro

      - source: telegram
        chat_type: private
        skills: [blog-deploy, news-digest, rss-reader]
        model: deepseek-v4-pro
        toolsets: [terminal, web, file]

  permissions:
    admin:
      - telegram:123456789
    admin_toolsets: [*]

cron:
  enabled: true
  tasks:
    - name: daily-ai-digest
      schedule: "30 8 * * *"
      description: "每日 AI 资讯摘要"
      model: deepseek-v4-pro
      toolsets: [web]
      skills: [news-digest]
      notify:
        channel: feishu
        webhook_url: ${FEISHU_WEBHOOK}

    - name: blog-auto-deploy
      schedule: "0 22 * * *"
      description: "博客自动部署"
      toolsets: [terminal, file, web]
      skills: [blog-deploy]
      notify:
        channel: telegram
        chat_id: "123456789"
```

配置完，你的生活变成这样：

- **早上 8:30**：飞书群里自动收到 AI 资讯摘要
- **随时**：在 Telegram 上问 Hermes 搜东西、查资料、写代码
- **晚上 10:00**：Telegram 上收到博客部署结果
- **服务器出问题**：飞书运维群收到告警

全程你不需要打开终端。

## 安全和运维

### 不要裸奔

Gateway 监听在 `0.0.0.0:8080` 上，如果你的服务器有公网 IP，**必须加反向代理**：

```bash
# 最简单的方案：Caddy 反向代理 + 自动 HTTPS
sudo apt install caddy

# /etc/caddy/Caddyfile
hermes.yourdomain.com {
    reverse_proxy localhost:8080
}
```

Telegram 和飞书的 webhook 指到 `https://hermes.yourdomain.com`，中间走 HTTPS，Token 不会在明文中传。

### 环境变量隔离

别把 Token 硬编码在配置文件里。用环境变量：

```bash
# ~/.bashrc 或 ~/.zshrc
export FEISHU_APP_SECRET="your-secret"
export TELEGRAM_BOT_TOKEN="1234567890:ABCdef..."
export DISCORD_BOT_TOKEN="your-discord-token"
```

配置文件里用 `${VAR}` 引用。这样配置文件可以提交到 Git，Token 不会泄露。

### 监控 Gateway 状态

Gateway 是个独立进程，偶尔会挂（网络波动、平台 API 变更）。建议配一个 cron 健康检查：

```bash
hermes cron create "*/5 * * * *" "
检查 Gateway 是否在运行：
1. 用 terminal 执行：curl -s http://localhost:8080/health
2. 如果返回不是 200，或者连接失败，用 gateway 推送到 Telegram：
   '⚠️ Hermes Gateway 挂了，快去重启'
3. 如果返回 200，什么都不做
"
```

或者直接用 systemd 的自动重启：

```ini
# /etc/systemd/system/hermes-gateway.service
[Unit]
Description=Hermes Gateway
After=network.target

[Service]
Type=simple
User=ubuntu
ExecStart=/usr/local/bin/hermes gateway run
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable --now hermes-gateway
```

## 一个 Gateway 的边界在哪

最后聊一个容易被忽略的问题：**哪些事该让 Gateway 做，哪些事不要**。

正确的边界：

| ✅ 让 Gateway 做 | ❌ 不要让 Gateway 做 |
|---|---|
| 消息格式转换 | 业务逻辑判断 |
| 用户身份识别 | 复杂数据处理 |
| 路由分发 | 长时间推理（那是 Agent 的事） |
| 平台 API 限流 | 文件存储 |

记住：Gateway 是**消息管道**，不是业务引擎。它只负责「把正确的消息交给正确的 Agent，再把正确的回复送回正确的平台」。任何需要「思考」的事情，交给 Agent 的模型去做。

## 下一站

这篇文章把 Gateway 讲透了。下一篇是 Hermes 系列最后一篇——**实战：搭建你的第一个 AI 工作流**。我们会把六篇里讲到的所有东西（配置、Skills、Cron、Gateway）全部串起来，从零搭建一个完整可用的 AI 自动化流程。

系列导航：[01 入门指南](/posts/hermes-agent-guide/) | [02 配置详解](/posts/hermes-agent-config/) | [03 Skills 系统](/posts/hermes-agent-skills/) | [04 Cron 定时任务](/posts/hermes-agent-cron/) | **05 多平台集成** | [06 实战工作流](/posts/hermes-agent-workflow/)
