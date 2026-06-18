---
title: "Hermes Agent 入门指南：你的24小时AI助手"
date: 2026-06-18
tags: ["AI", "Hermes", "工具教程", "自动化"]
description: "从零开始配置 Hermes Agent，一个开源、支持多平台的 AI 编程助手，让你拥有一个永不休息的数字员工。"
---

## 什么是 Hermes Agent？

[Hermes Agent](https://github.com/NousResearch/hermes-agent) 是 Nous Research 开源的 AI 代理框架。它能跑在终端、飞书、Telegram、Discord 等十几个平台上，调用各种工具帮你干活——写代码、搜资料、管理文件、定时任务，甚至帮你赚点小钱。

和 Claude Code、Codex 相比，Hermes 有几个独特优势：

- **完全开源**，不绑定任何厂商
- **支持 20+ 模型提供商**，OpenRouter、Anthropic、DeepSeek、OpenAI 随便切
- **持久化记忆**——它会记住你是谁、你的偏好、你的项目
- **技能系统**——学会一个新技能就保存下来，越用越聪明

## 安装

一行命令搞定：

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

## 快速上手

```bash
# 进入交互模式
hermes

# 一句话提问
hermes chat -q "帮我写一个 Python 爬虫"

# 切换模型
hermes model
```

## 接入飞书

Hermes 原生支持飞书，配置好后你就能在飞书里和它聊天：

```bash
hermes gateway setup    # 选择 Feishu
hermes gateway run      # 启动网关
```

## 定时任务

让 Hermes 定期帮你干活——比如每天早上抓取最新 AI 资讯：

```bash
hermes cron create "0 8 * * *"  # 每天早上8点
```

## 总结

Hermes Agent 是开发者提升效率的利器。开源、免费、多平台，值得一试。

> 我后面会继续分享更多 Hermes 的高级用法和自动化副业思路，欢迎关注。
