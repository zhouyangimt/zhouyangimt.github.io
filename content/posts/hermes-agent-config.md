---
title: "Hermes Agent 深度指南 02：配置详解 — 模型选择、providers 与 toolsets"
date: 2026-06-19
tags: ["AI", "Hermes", "工具教程", "自动化"]
description: "深入拆解 Hermes Agent 的配置系统：20+ providers 怎么选、模型怎么搭、toolsets 怎么配出最强组合。"
---

这是 Hermes Agent 深度指南系列的第二篇。如果你还没看过第一篇，先去[入门指南](/posts/hermes-agent-guide/)把 Hermes 装上跑起来，本文默认你已经有了一个能用的 Hermes 实例。

上一篇我们讲了安装和基础用法——一行 curl 装好，进交互模式聊两句就上手了。但这只是 Hermes 的「默认皮肤」。真正让它变成你得力助手的，是配置系统。

Hermes 的核心优势之一是**不绑定任何模型厂商**。OpenRouter、Anthropic、DeepSeek、OpenAI、Google Gemini……20+ 提供商随便换，而且可以混搭——干活用一个模型，复查用另一个模型，甚至一个任务里跑一半切模型。

今天咱们把 providers、模型选择、toolsets 三个核心配置项拆开讲透。

![Hermes Agent 整体架构：用户层 → 消息路由 → 模型层](/images/hermes-architecture.png)

## 配置文件在哪

Hermes 的配置分布在两个文件：

```
~/.hermes/config.yaml   # 主配置：模型、工具集、人格、安全策略等
~/.hermes/.env          # 密钥（API Key、Token），单独存放防止泄露
```

直接编辑也行，但 Hermes 提供了更安全的方式：

```bash
# 查看当前配置
hermes config

# 用编辑器打开 config.yaml
hermes config edit

# 逐项设置（推荐，不会搞乱缩进）
hermes config set model.default "anthropic/claude-sonnet-4"
hermes config set agent.max_turns 90

# 管理密钥（更安全，会做本地加密）
hermes auth
```

先说最重要的 providers。

## Providers：20+ 模型提供商怎么选

Hermes 支持的 providers 可以分三类：

**第一类：聚合平台（性价比首选）**

| Provider | 特点 | 适合场景 |
|----------|------|---------|
| **OpenRouter** | 聚合 200+ 模型，按用量计费 | 日常主力，模型随便试 |
| **Nous Portal** | Hermes 官方配套，OAuth 登录 | 想省事的默认选择 |
| **Hugging Face** | 开源模型托管，免费额度 | 跑开源模型、研究调试 |

**第二类：厂商直连（性能最优）**

| Provider | 招牌模型 | 适合场景 |
|----------|---------|---------|
| **Anthropic** | Claude Sonnet 4 / Opus 4 | 复杂推理、长文分析、架构设计 |
| **OpenAI** | GPT-5 / o4-mini / Codex | 编码、工具调用、多模态 |
| **Google Gemini** | Gemini 3 Pro / Flash | 超长上下文（1M token）、免费额度大 |
| **DeepSeek** | DeepSeek V4 Pro / Flash | 性价比极高，编码和推理均衡 |
| **xAI / Grok** | Grok 4 | 实时信息、创意任务 |

**第三类：国内厂商**

| Provider | 特点 |
|----------|------|
| **通义千问 / DashScope** | 阿里系，API 稳定，中文能力强 |
| **Kimi / Moonshot** | 月之暗面，超长上下文 |
| **GLM / Z.AI** | 智谱，开源生态好 |
| **MiniMax** | 性价比不错 |

怎么配？两个方法：

**方法一：交互式配置**

```bash
# 进入交互式模型选择器，上下箭头选
hermes model

# 或者走完整配置向导
hermes setup
```

**方法二：命令行直设（适合脚本/切换）**

```bash
# 切到 Claude Sonnet
hermes config set model.default "anthropic/claude-sonnet-4"
hermes config set model.provider anthropic

# 切到 Gemini Flash（便宜、快）
hermes config set model.default "gemini-3-flash"
hermes config set model.provider google

# 用 OpenRouter 中转（一次配好，后面随便换模型名）
hermes config set model.provider openrouter
hermes config set model.default "anthropic/claude-sonnet-4"
```

API Key 怎么设：

```bash
# 直接写 .env 文件（推荐，跟 config 分离）
echo "OPENROUTER_API_KEY=sk-or-v1-xxxx" >> ~/.hermes/.env
echo "ANTHROPIC_API_KEY=sk-ant-xxxx" >> ~/.hermes/.env
echo "DEEPSEEK_API_KEY=sk-xxxx" >> ~/.hermes/.env

# 或者用 auth 命令（会做本地加密存储）
hermes auth add openrouter
hermes auth add deepseek
```

### Credential Pools：多 Key 轮转

如果你一个 provider 有多个 API Key（比如多个 OpenRouter 账号，或者团队共享额度），Hermes 支持 credential pool——自动轮转 Key，一个限额了用下一个：

```bash
# 多次执行 auth add，同一个 provider 会累积成池
hermes auth add openrouter   # 第一个 Key
hermes auth add openrouter   # 第二个 Key
hermes auth add openrouter   # 第三个 Key

# 查看池子
hermes auth list openrouter

# Key 0 超限被压了？手动重置
hermes auth reset openrouter
```

这个机制对重度用户特别实用——不用担心写着写着突然撞限额。

## 模型选择：不是越贵越好

选模型的核心原则：**用最便宜的模型能搞定的活，不浪费贵的模型**。

Hermes 切换模型的成本几乎为零——一行命令就切了。所以最佳实践是**根据任务类型挑模型**：

### 实际场景：三模型分工

我在日常开发中用了三个模型配比：

```bash
# 1. 日常主力 — DeepSeek V4 Pro
#    性价比最高，编码、问答、文档全包了
#    每天 80% 的交互用它
hermes config set model.default "deepseek-v4-pro"
hermes config set model.provider deepseek

# 2. 重度推理 — Claude Sonnet 4
#    架构设计、大规模重构、复杂 Debug
#    context 200K，理解力强
hermes chat -m "anthropic/claude-sonnet-4" --provider anthropic

# 3. 快扫任务 — Gemini 3 Flash
#    读日志、格式转换、批量小任务
#    免费额度大，响应快
hermes chat -m "gemini-3-flash" --provider google
```

**省钱的实操**：

```bash
# 比如我要让 AI 读 50 个日志文件找错误
# 这种活用 Gemini Flash（谷歌免费额度多），别用 Claude

# 但架构重构、写核心逻辑，用 Claude 或 GPT-5
# 因为少返工一次就值回差价
```

### Delegation：主模型 + 子代理模型

Hermes 支持 delegation——主模型把子任务分派给另一个模型：

```yaml
# ~/.hermes/config.yaml
delegation:
  model: "gemini-3-flash"      # 子代理用便宜模型
  provider: google
  max_iterations: 50           # 子代理最多跑 50 轮
  reasoning_effort: low        # 子代理少推理，快速执行
```

这样主模型（比如 Claude）负责思考决策，子代理（Gemini Flash）负责机械执行——搜索、读文件、跑命令。既能保证质量，又省不少钱。

### 实际配置参考

这是我 ~/.hermes/config.yaml 里 model 部分的简化版：

```yaml
model:
  default: deepseek-v4-pro
  provider: deepseek
  base_url: https://api.deepseek.com/v1
  api_mode: chat_completions

# 用环境变量放 Key，不写死在 config 里
# ~/.hermes/.env:
#   DEEPSEEK_API_KEY=sk-xxxx
#   ANTHROPIC_API_KEY=sk-ant-xxxx
#   GOOGLE_API_KEY=AIza-xxxx
```

这样就配出一个最常见的方案：日常用 DeepSeek，关键时刻指定 `--provider` 切到别的模型。

## Toolsets：给你的 AI 装上瑞士军刀

models 管「谁在想」，toolsets 管「能做什么」。

Hermes 有 30+ 个 toolsets，默认启用的核心 set 包含 terminal、文件操作、web 搜索、代码执行等基本能力。你还可以按需加减。

### 常用 toolsets 速查

| Toolset | 能力 | 建议 |
|---------|------|------|
| `terminal` | 执行 shell 命令、管理进程 | **必开** |
| `file` | 读写文件、搜索、打补丁 | **必开** |
| `web` | 网页搜索 + 内容提取 | **必开** |
| `code_execution` | 沙箱 Python 执行 | 写代码时开 |
| `vision` | 图片分析 | 看图场景开 |
| `browser` | 浏览器自动化 | 爬取动态页面时开 |
| `memory` | 跨会话长期记忆 | 重度用户开 |
| `delegation` | 子代理任务分发 | 复杂任务开 |
| `cronjob` | 定时任务管理 | 自动化场景开 |
| `session_search` | 搜索历史对话 | 项目多了开 |
| `safe` | 受限最低权限 | 给别人用时开 |

### 怎么管 toolsets

```bash
# 交互式开关（有 TUI 菜单，最方便）
hermes tools

# 查看所有 toolsets 及状态
hermes tools list

# 命令行直接开关
hermes tools enable browser     # 开浏览器自动化
hermes tools enable delegation  # 开子代理
hermes tools disable vision     # 关图片分析（省 token）

# 启动时指定 toolsets
hermes chat -t "terminal,file,web,browser"
```

注意：toolset 变更要 `/reset`（新会话）才生效，设计如此——为了不破坏已缓存的 prompt。

### 三个实战组合

**组合一：轻量日常（省钱、快）**

```bash
hermes tools enable terminal
hermes tools enable file
hermes tools enable web
hermes tools disable vision
hermes tools disable browser
hermes tools disable code_execution
```

写写文档、搜搜资料、管管文件够用了，token 消耗最少。

**组合二：全栈开发**

```bash
hermes tools enable terminal
hermes tools enable file
hermes tools enable web
hermes tools enable code_execution   # 跑 Python 验证逻辑
hermes tools enable delegation       # 大任务拆小任务
hermes tools enable memory           # 记住项目上下文
```

写项目时用这套，Hermes 能读写代码、跑测试、查文档、拆任务——基本覆盖开发全流程。

**组合三：自动化值班**

```bash
hermes tools enable terminal
hermes tools enable file
hermes tools enable web
hermes tools enable cronjob          # 定时触发
hermes tools enable session_search   # 回溯之前干了啥
```

设好 cron 任务后，Hermes 到点自己拉数据、写报告、发飞书——一套全自动。

### MCP 扩展：无限工具

如果你觉得内置 toolsets 不够，Hermes 还支持 MCP 协议——接入外部工具服务器：

```yaml
# ~/.hermes/config.yaml
mcp_servers:
  # 接 GitHub：让 Hermes 直接管理 Issue/PR
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_xxx"

  # 接文件系统（指定目录范围）
  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/ubuntu/projects"]

  # 接远程 API
  company_api:
    url: "https://mcp.mycompany.com/mcp"
    headers:
      Authorization: "Bearer sk-xxx"
```

接上之后，Hermes 的工具列表会自动多出 `mcp_github_create_issue`、`mcp_filesystem_read_file` 这些新工具，用法跟内置的一样。这个我们后面会单独写一篇展开讲。

## 安全配置：别忽略

配置里还有几个跟安全相关的选项，顺手设了：

```bash
# 密钥脱敏（默认开，别关）
hermes config set security.redact_secrets true

# 命令审批模式
# manual: 危险命令弹出确认（默认）
# smart:  让子模型判断风险级别，低风险自动过（推荐）
# off:    跳过所有确认（等同 --yolo，不推荐）
hermes config set approvals.mode smart

# 给没用过的人用？切到 safe toolset
hermes tools enable safe   # 只开放最低风险工具
```

## 动手试试

看到这你应该已经有一个不一样的 Hermes 了。别光看，试试这几步：

1. `hermes model` 切换到 DeepSeek，跑两个任务感受下
2. `hermes tools` 打开/关掉几个 toolset，看看 `/reset` 后工具列表变化
3. 试一下 delegation：把 config 里设好子代理模型，然后扔一个「帮我研究 X 主题」的任务

**下一篇预告**：Skills 系统。这是 Hermes 最特别的功能——学会的东西**保存下来**，下次自动加载。相当于你给 Hermes 写 SOP，越用越顺手。我们下一篇拆解怎么写一个好用的 Skill。
