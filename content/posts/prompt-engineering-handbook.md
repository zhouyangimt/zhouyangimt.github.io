---
title: "AI编程工具链：Prompt Engineering 实战手册"
date: 2026-06-27
tags: ["AI", "编程", "工具教程"]
description: "别再「帮我写个程序」了。系统化Prompt Engineering的方法论、模板和实战案例，让你的AI输出质量翻倍。"
---

## 你的Prompt，决定了AI的上限

很多人的认知还停留在「我直接告诉AI要干嘛就行了」。但实际情况是——**同样的模型，不同质量的prompt，产出的代码质量差距可以有10倍以上。**

一个真实的例子：

> ❌ 「帮我写一个爬虫」
> ✅ 「用 Python 写一个爬虫，抓取 https://example.com/news 的新闻标题和链接，用 requests + BeautifulSoup，输出为 JSON 文件，需要处理异常（超时、404），加上请求间隔（3秒）避免被封。」

第一个人得到的是几十行能跑但脆弱的代码。第二个人得到的是可以直接部署的生产级脚本。

这就是Prompt Engineering的威力：**把模糊的需求变成精确的指令。**

![Prompt Engineering 工作流](/images/prompt-engineering-workflow.png)

## 核心框架：四步法

我用了两年AI编程工具，总结出这套「四步法」。它能适配90%的编码场景。

### 第一步：角色设定（Role）

告诉AI「你是谁」和「AI是谁」，建立上下文边界。

```
你是一名有10年经验的Python后端工程师，擅长编写高可读性、
可维护的代码。你的代码风格遵循 PEP 8，并且你会主动添加
类型注解和 docstring。
```

**为什么有效？** AI模型的训练数据中，特定角色的输出质量远高于通用输出。「Senior Engineer」这个角色对应的训练样本本身就是高质量的。

### 第二步：任务拆解（Task Decomposition）

大任务拆成小任务，逐个击破。

> ❌ 「用React写一个电商网站」
> ✅ 「请分步骤完成以下任务：
> 1. 创建商品列表组件，支持分页
> 2. 实现购物车状态管理（zustand）
> 3. 添加搜索栏（防抖500ms）
> 4. 集成支付Mock接口
> 每完成一步，先让我确认再继续。」

**一个prompt只做一件事。** AI在单次对话中的注意力是有限的——任务越多，每个任务的质量就越低。

### 第三步：约束与范例（Constraints & Examples）

这可能是最被低估的一步。

```
要求：
- 使用 Python 3.11+
- 依赖：requests, pydantic v2
- 所有函数必须有类型注解
- 错误处理覆盖网络异常、解析异常、数据校验异常

参考风格：
```python
def fetch_data(url: str, timeout: int = 10) -> dict[str, Any]:
    """Fetch JSON data from URL with error handling."""
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        raise DataFetchError(f"Failed to fetch {url}: {e}")
```
```

**给AI看一段你满意的代码，比花500字描述风格要求更有效。**

### 第四步：产出规格（Output Spec）

明确告诉AI「输出成什么样」。

```
请输出以下文件结构：
src/
├── fetcher.py    # 数据抓取模块
├── parser.py     # 数据解析模块
├── models.py     # Pydantic 模型
└── main.py       # 入口，命令行参数支持

每个文件的完整代码，加上注释。
```

## 进阶技巧

### 1. Chain of Thought（思维链）

让AI「说出思考过程」再写代码，能显著提升复杂逻辑的准确率。

```
请先分析这个需求涉及哪些模块和数据结构，
列出你的设计思路，然后再写代码。
```

这在你用 Claude Code 或 Hermes Agent 做架构设计时特别有效——它会先输出设计文档，你可以review后再让它实现。

### 2. Few-Shot（少样本提示）

给2-3个「输入→期望输出」的例子。

```
示例1:
输入: "用户名字为空的错误"
输出: UserNameEmptyError(msg="用户名不能为空", code="E001")

示例2:
输入: "API超时30秒"
输出: APITimeoutError(msg="API请求超时", code="E002", timeout=30)

请按相同格式，为以下场景生成自定义异常类：
- 数据库连接失败
- 文件格式不支持
- 权限不足
```

### 3. Self-Refinement（自我修正）

让AI自己检查和改进输出。

```
写完代码后，请做以下检查：
1. 是否有未处理的异常路径？
2. 是否有硬编码的魔法数字？
3. 日志是否足够诊断问题？
4. 并发场景下是否存在竞态条件？

针对发现的问题，输出改进版代码。
```

### 4. 对抗性测试

让AI「攻击」自己写的代码。

```
请假设你是一个恶意用户，尝试找出上面代码的安全漏洞。
重点关注：SQL注入、XSS、路径遍历、未授权访问。
列出所有发现的问题和修复方案。
```

## 场景实战

### 场景一：重构遗留代码

```
你是一名高级重构工程师。以下是一段遗留的Python代码。
请完成：
1. 分析代码结构，指出存在哪些设计问题
2. 将全局变量重构为配置类
3. 将重复逻辑抽取为工具函数
4. 添加类型注解和单元测试框架
5. 输出重构后的完整代码

约束：
- 保持外部接口不变（向后兼容）
- 不引入新依赖
- 每个函数不超过30行

[粘贴代码]
```

### 场景二：Code Review

```
请以Tech Lead的身份审查以下Pull Request。
评审维度：
- 逻辑正确性
- 性能瓶颈
- 安全风险
- 可维护性

输出格式：
### 严重问题（必须修复）
### 建议改进（建议修复）
### 优秀实践（值得推广）

[粘贴diff]
```

### 场景三：从零搭建项目

```
我需要创建一个 FastAPI 项目，功能是「用户书签管理」。
请帮我搭建项目骨架，包括：

功能需求：
- 用户注册/登录（JWT）
- CRUD 书签（URL + 标题 + 标签）
- 搜索书签（按标题/标签）

技术栈：
- FastAPI + SQLAlchemy 2.0 (async)
- PostgreSQL
- Alembic 迁移
- Pydantic v2
- pytest

输出：
1. 项目目录结构
2. 所有文件的代码
3. docker-compose.yml（含PostgreSQL）
4. README.md

先输出架构设计，我确认后再写代码。
```

## 常见误区

| 误区 | 正确做法 |
|------|---------|
| Prompt越长越好 | 精准胜过冗长。去掉废话，保留关键约束 |
| 一个prompt搞定一切 | 拆成多步，每步一个prompt |
| 让AI猜你的意图 | 显式说明「不要做什么」 |
| 不问就不给上下文 | 主动提供：技术栈、版本、约束、范例 |
| 忽视输出格式 | 明确指定文件结构、代码风格 |

## 工具推荐

2026年，这些工具让Prompt Engineering更高效：

- **Claude Code**：支持 `/add-directory` 把整个项目作为上下文，prompt里可以直接引用文件
- **Cursor**：`.cursorrules` 文件定义项目级prompt规则，一次配置全项目生效
- **Hermes Agent**：Skills系统可以把好的prompt模板保存下来，下次直接用（见[配置详解](/posts/hermes-agent-config/)）

## 总结

Prompt Engineering 不是什么玄学，而是**系统化的需求表达**。核心就四个字：**精确、具体**。

记住这个原则：**你对AI投入多少思考，AI就回报你多少代码质量。**

写好prompt不是一个技巧，而是一个习惯。养成后，你的AI编程效率会提升一个量级。

---

> **AI编程工具链系列：**
> - [AI编程助手完全指南](/posts/ai-coding-assistant-guide-2026/)
> - [Claude vs Cursor vs Copilot 横评](/posts/claude-code-vs-cursor-vs-copilot/)
> - [零代码用AI搭建网站](/posts/ai-build-website-zero/)
> - 👉 Prompt Engineering 实战手册（本文）
> - [AI Debugging：让AI帮你修bug](/posts/ai-debugging-guide/)
> - 系列完结 ✅
