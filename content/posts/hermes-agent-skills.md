---
title: "Hermes Agent 深度指南 03：Skills 系统 — 打造可复用能力"
date: 2026-06-19
description: "Skills 是 Hermes Agent 最特别的设计——把你教会 AI 的东西保存下来，下次自动加载。这篇拆解 Skill 的结构、怎么写、怎么用、怎么让它越用越聪明。"
tags: [AI, Hermes, 工具教程, 自动化]
draft: false
---

这是 Hermes Agent 深度指南系列的第三篇。前两篇分别是入门指南
和配置详解
——建议先看完那两篇再回来看这篇，因为本文默认你已经有跑起来的 Hermes 了。

前两篇聊了安装和配置。但有一个问题我一直没回答：**你教会 Hermes 的东西，下次还能用吗？**

大部分 AI 助手是金鱼——每次对话结束就清零了。你费劲调好的工作流，下次得从头教。但 Hermes 的设计思路不一样：它有一个 Skills 系统，让你把「怎么干活」写成标准化文档，下次自动加载。

换句话说，Skills 就是 Hermes 的 SOP。
## Skills 是什么
简单说：**一个 Skill 就是一个 Markdown 文件**，放在 `~/.hermes/skills/` 下面，里面写清楚「什么场景下用」「怎么一步步做」「常见的坑在哪」。Hermes 每次回答之前，会自动扫一遍 Skill 列表，遇到匹配的场景就把对应 Skill 的内容注入到上下文中。

三个关键特性：- **渐进式加载**（progressive disclosure）。Hermes 不会一股脑把所有 Skill 全塞进 prompt。先只加载名字和简介（约 3K token），只有真正轮到用时才展开完整内容。这解决了「技能越多速度越慢」的问题。- **Agent 可以自己创建 Skill**。做完一个复杂任务后，如果 Hermes 觉得「这个工作流值得保存」，它自己会产生一个 Skill。你有审批权。- **Skill Hub**。内置 + 社区共享，几十个现成 Skill 可以直接装。
## 看一眼 Skill 长什么样
随便看两个实际例子。

**系统级 Skill：《systematic-debugging》**

这个 Skill 定义了四阶段调试法——根因分析→模式比对→假设验证→实施修复。核心就一条铁律：`NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
`加载这个 Skill 后，Hermes 遇到 bug 不会上来就改代码，而是先读错误信息、尝试复现、查 git diff 找最近改动、追踪数据流找到源头。然后才动手。

这个 Skill 有 350+ 行，但 Hermes 只在用户报 bug 时才加载它，平时不占 token。

**用户自建 Skill：《douyin-copy-extract》**

这是我见过的一个实用案例——从抖音/快手/小红书链接提取文案。Skill 里定义了固定的输出格式：`【标题】
(提取的标题)

【简介】
(提取的简介)

【口播文案 · 原版提取】
(完整原文)

【违禁 / 敏感词提醒】
(检测结果)

【口播文案 · 优化朗读版】
(通顺断句版本)

【口播文案 · 精简浓缩版】
(核心精炼版本)

【文案时长参考】
总字数：XXX 字 / 建议口播时长：约 XX 秒
`用法贼简单：在 Hermes 里输入 `/douyin-copy-extract https://v.douyin.com/xxxxx`，它就按这个格式给你输出全套文案。
## Skill 的目录结构
一个 Skill 不只是一个 Markdown 文件，它还可以带一堆辅助资源：~/.hermes/skills/
├── software-development/
│   └── systematic-debugging/
│       ├── SKILL.md           # 主文件（必须有）
│       ├── references/        # 参考资料
│       ├── templates/         # 输出模板
│       ├── scripts/           # 辅助脚本
│       └── assets/            # 附件
`其中 `scripts/` 特别有用。如果你的 Skill 需要调外部 API 或者做 JSON 解析，你可以放一个 Python 脚本在里面，然后在 SKILL.md 里写：运行辅助脚本：
  python3 ${HERMES_SKILL_DIR}/scripts/fetch_data.py &lt;参数&gt;
``${HERMES_SKILL_DIR}` 是 Hermes 自动替换的变量，指向 Skill 目录的绝对路径。Agent 拿到后直接用 terminal 工具执行，不用自己做路径拼接。
## SKILL.md 怎么写
最简版：---
name: my-skill
description: 这个 Skill 做什么
---

# Skill Title

## When to Use
什么场景下应该加载这个 Skill。

## Procedure
1. 第一步
2. 第二步
3. 第三步

## Pitfalls
- 常见错误1：怎么解决
- 常见错误2：怎么解决

## Verification
怎么确认它做对了。
`更完整的版本可以加这些元数据：---
name: my-skill
description: &#34;一句话描述&#34;
version: 1.0.0
platforms: [macos, linux]       # 限定平台，可选
metadata:
  hermes:
    tags: [tag1, tag2]          # 方便搜索
    category: devops             # 分类目录名
    related_skills: [other-skill-name]
    requires_toolsets: [web]     # 只在有 web 工具集时显示
    fallback_for_toolsets: [browser]  # 只在没有 browser 时显示
required_environment_variables:  # 需要的 API Key
  - name: MY_API_KEY
    prompt: &#34;请输入你的 API Key&#34;
    help: &#34;去 https://example.com 获取&#34;
---
`几个值得展开的细节：

**`requires_toolsets` vs `fallback_for_toolsets`**

这两个控制 Skill 什么时候出现。`requires_toolsets` 是「我有这些工具才出现」，`fallback_for_toolsets` 是「没有这些工具才出现」。

举个例子：Hermes 内置了一个 `duckduckgo-search` Skill，它的 frontmatter 里写着 `fallback_for_toolsets: [web]`。意思就是：**如果你配了 Web 搜索 API Key，web 工具集可用，那这个 DuckDuckGo Skill 自动隐藏**——因为更高级的 web_search 工具已经在了。但如果你没配 Key，web 工具集不可用，DuckDuckGo Skill 就自动出现，充当免费后备。

这个设计很干净：常用场景用高端方案，没配好也有一条可用路径，用户不用手动切换。

**`required_environment_variables`**

如果你的 Skill 要调第三方 API，用这个声明需要的环境变量。Hermes 在加载 Skill 时如果发现缺 Key，会在本地 CLI 弹出提示让你输入，但不会在飞书/Telegram 这类聊天界面里问——聊天界面会提示你去用 `hermes setup` 或者直接编辑 `~/.hermes/.env`。

配好之后还有一个加分项：Hermes 会把这些 env var **透传到执行沙箱**里。也就是说你在 Skill 里让 Agent 跑一个 Python 脚本，脚本里 `os.environ["MY_API_KEY"]` 可以直接拿到值——不用额外配置。
## 实战：写一个静态博客自动发布的 Skill
光说不练假把式。我们写一个实际的 Skill：自动发布 Hugo 静态博客文章到 GitHub Pages。
### 场景
我有一个 Hugo 博客，文章是 Markdown 格式。每次写完文章后需要：- 用 `hugo --minify` 构建- 把 `public/` 目录推送到 GitHub Pages每次手动跑这两步很烦。写个 Skill 让 Hermes 一键搞定。
### SKILL.md
---
name: blog-deploy
description: &#34;构建 Hugo 静态博客并推送到 GitHub Pages&#34;
version: 1.0.0
platforms: [linux, macos]
metadata:
  hermes:
    tags: [blog, hugo, github, deploy]
    category: productivity
---

# Blog Deploy

## When to Use
- 刚写完一篇博客文章，需要部署上线
- 修改了博客主题或配置，需要重新构建
- `hugo server` 预览没问题，准备推送

## Prerequisites
- Hugo 已安装（`which hugo`）
- 博客目录有 `hugo.toml` 或 `config.toml`
- `public/` 目录已初始化 git 并关联远程仓库

## Procedure

### 1. 确认环境
```bash
cd ~/side-hustle/content-site
hugo version
git -C public remote -v
`
### 2. 构建
cd ~/side-hustle/content-site
hugo --minify --cleanDestinationDir
`检查输出：如果看到 `Total in XX ms` 说明构建成功。
### 3. 检查是否有变更
cd ~/side-hustle/content-site/public
git status --short
`如果输出为空，说明没有新内容需要推送。
### 4. 推送
cd ~/side-hustle/content-site/public
git add -A
git commit -m &#34;deploy: $(date +%Y-%m-%d)&#34;
git push origin main --force-with-lease
`
### 5. 验证
部署后等 1-2 分钟，确认线上已更新：curl -sI https://你的域名/index.html | grep last-modified
`
## Pitfalls
- **Hugo 不给构建未来日期的文章**：如果文章 `date` 设的是今天但 Hugo 还没到那个时间点构建，检查 `hugo.toml` 里有没有 `buildFuture = true`- **push 被拒绝**：GitHub Pages 会自动在远程生成提交，导致本地落后。用 `--force-with-lease`，不要 rebase- **remote 丢失**：如果 `git -C public remote -v` 没输出，手动添加：`git -C public remote add origin git@github.com:用户名/用户名.github.io.git`
## Verification
- `hugo --minify` 退出码为 0- `git push` 返回 `main -> main`- `curl -sI` 返回 200 且 `last-modified` 是今天的`
### 安装和使用

把 SKILL.md 放到 `~/.hermes/skills/productivity/blog-deploy/SKILL.md`，然后：

```bash
# 交互模式里直接用
/blog-deploy

# 或者命令行里
hermes chat -t &#34;terminal,file&#34; -q &#34;用 blog-deploy skill 部署博客&#34;
`Hermes 加载这个 Skill 后，会严格按 Procedure 一步步走：确认环境→构建→检查变更→推送→验证。不会跳过任何步骤，也不会在构建失败的情况下强行推送。
## Agent 自己创建 Skill
Hermes 最有意思的设计之一：它在完成一个复杂任务后，**会自己总结工作流写成 Skill**。

触发条件：- 任务调用了 5 次以上工具- 中间遇到错误并找到了正确的解决方案- 你纠正过它的方法- 它发现了一个非标准但有效的流程比如你让 Hermes 帮你把 50 个 Markdown 文件转成 PDF 并排版。它先尝试了 `pandoc` 发现中文渲染有问题，换成 `wkhtmltopdf` 好了，又发现标题层级不统一得先用脚本预处理。折腾完这个任务后，它可能会产生一个 Skill 叫 `markdown-to-pdf-batch`，把这些踩过的坑都记下来。

下次你或其他人让 Hermes 做同样的事，它直接加载这个 Skill，不会重新踩坑。

不过你也不用担心它乱写。默认情况下 Agent 写 Skill 是自动的，但你可以打开审批模式：# ~/.hermes/config.yaml
skills:
  write_approval: true   # 每次写 Skill 都需要你审批
`然后通过 `/skills pending` 查看待审批的 Skill，`/skills diff &lt;id>` 看具体改动，`/skills approve &lt;id>` 批准。
## Skill Hub：社区共享能力
除了自己写，Hermes 还有一个 Skill Hub——可以从社区安装现成的 Skill：# 搜索
hermes skills search kubernetes

# 预览
hermes skills inspect openai/skills/k8s

# 安装
hermes skills install openai/skills/k8s

# 查看已安装的
hermes skills list

# 升级
hermes skills update
`安装前 Hermes 会自动做安全扫描：检查有没有数据外泄模式、有没有 prompt injection 攻击、有没有危险的 shell 命令。信任级别分四档：级别来源行为`builtin`随 Hermes 发布免检`official`官方可选 Skills免检`trusted`OpenAI/Anthropic/HuggingFace 官方源检查但放行`community`社区源标记风险，需 `--force`
## Skill Bundles：技能组合技
如果一个任务固定需要加载好几个 Skill，你可以把它们打包成 Bundle：hermes bundles create backend-dev \
  --skill systematic-debugging \
  --skill test-driven-development \
  --skill github-code-review \
  -d &#34;后端开发全流程：调试→测试→代码审查&#34;
`然后 `/backend-dev` 一次加载三个 Skill。Bundle 就是一个 YAML 文件，放在 `~/.hermes/skill-bundles/` 下面，团队共享也方便——往共享文件夹里一扔，大家 symlink 过去就行。
## 我目前的 Skill 配置
分享一下我的实际配置，供参考。在我的场景里（维护静态博客 + 写技术文章 + 偶尔做 Web QA），用的 Skills 是这几类：

**系统级（默认就装好了，不用管）：**- `plan`：复杂任务先出方案再执行- `test-driven-development`：写测试→实现→重构- `systematic-debugging`：四阶段调试法**内容相关（我自己写的 + Hub 装的）：**- `static-blog-automation`：Hugo 博客自动发布- `hugo-github-pages`：GitHub Pages 部署细节**工具类：**- `douyin-copy-extract`：短视频文案提取- `dogfood`：Web 应用 QA 测试（加载后用 browser 工具系统性地测试网站）这几个加起来覆盖了 80% 的日常使用场景。剩下的 20% 靠 Hermes 的通用能力 + `skill_manage` 动态补充。
## 动手试试
看完别走，动手做一个：- **装一个现成的 Skill**：`hermes skills browse` 翻翻目录，装一个你觉得用得上的。比如 `github-code-review` 或者 `arxiv`。- **写一个你自己的 Skill**：挑一个你每周至少做两次的重复任务，按 SKILL.md 格式写下来。文件放在 `~/.hermes/skills/&lt;分类>/&lt;你的skill名>/SKILL.md`。- **跑一遍**：在 Hermes 里 `/你的skill名` 试试，看它会不会严格按你写的流程执行。如果某个步骤它跳过了，检查 Procedure 部分的描述是不是不够明确——Skill 的写法是「指令式」的，不是「建议式」的。- **看看 Agent 会不会自己生 Skill**：给 Hermes 一个复杂的多步骤任务（比如「分析我最近 50 个 git commit，按功能分类，找出写得最烂的 3 段代码并给出重写建议」），任务结束后用 `ls ~/.hermes/skills/` 看看有没有新 Skill 出现。下一篇文章预告：**Cron 定时任务——让 AI 替你值班**。到时候用 Skill + Cron 结合，实现「每天早上 9 点，Hermes 自动检查 RSS 订阅、写一篇文章、推送到博客」。不用你动手，一条命令都不用敲。