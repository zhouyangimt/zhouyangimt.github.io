# zhouyang.dev 博客 · 四大板块完整架构

> 最后更新：2026-07-15

---

## 一、Tech · 技术文章

**定位**：深度原创技术文章，像过来人在跟你聊天。不写教科书。

**发布**：每周二 09:00（cron）
**规格**：2000-3500 字/篇 · Kroki 架构图配图 · 有实际可运行代码
**路线图**：`~/side-hustle/tech_ROADMAP.md`

### 系列 1：AI Agent 全解析（23 篇）

**逻辑线**：认知 → 架构 → 开源拆解 → 代码 Agent → 企业平台 → 龙虾 → 评估与未来

| 板块 | # | 标题 |
|------|---|------|
| **基础认知** | 1 | AI Agent 是什么：从 LLM 到自主智能体的进化 |
| | 2 | Agent 的四大核心能力：规划、记忆、工具、执行 |
| | 3 | 2026 AI Agent 全景图：谁在做什么，谁能用 |
| | 4 | 选 Agent 还是选 Copilot？不同场景的决策框架 |
| **架构与机制** | 5 | Agent 的架构模式：ReAct、Plan-Execute、Multi-Agent |
| | 6 | 工具调用深度解析：Function Calling、MCP 协议与插件生态 |
| | 7 | Agent 的记忆系统：短期记忆、长期记忆与 RAG |
| **开源 Agent 深度拆解** | 8 | Hermes Agent 入门：你的 24 小时 AI 助手 |
| | 9 | Hermes Agent 配置详解：模型、providers、toolsets |
| | 10 | Hermes Agent Skills 系统：打造可复用能力 |
| | 11 | LangChain vs CrewAI vs AutoGPT：三大开源框架横评 |
| | 12 | 用 LangGraph 构建多步骤 Agent 工作流 |
| **代码 Agent + IDE** | 13 | Claude Code vs Cursor vs GitHub Copilot：2026 横评 |
| | 14 | Cline + Aider：开源代码 Agent 双子星 |
| **企业级 Agent 平台** | 15 | Dify 实战：零代码搭建企业 AI 工作流 |
| | 16 | 钉钉 AI + Coze：中国市场的 Agent 生态 |
| **🦞 龙虾篇** | 17 | 疯狂又好用的 Agent 实测：Manus、Browser-use、Devin、GPT Researcher |
| | 18 | 垂直领域 Agent：法律、医疗、金融——AI 正在吃掉哪些白领工作 |
| | 19 | 中国 Agent 生态大乱斗：Kimi、豆包、文心、通义千问 |
| | 20 | 开源 Agent 奇行种：GitHub 上小但惊艳的项目 |
| | 21 | 2026 最值得关注的 25 个 AI Agent 项目 |
| **评估与未来** | 22 | Agent 的测试与评估：怎么判断一个 Agent 好不好用 |
| | 23 | Agent 的未来：多模态、具身智能与 AGI 之路 |

### 系列 2：独立开发者全栈指南（17 篇）

| 板块 | # | 标题 |
|------|---|------|
| **2A 副业入门** | 1 | 2026 年程序员的 6 个副业方向：从接私活到被动收入 |
| | 2 | 技术写作与内容站：程序员最被低估的复利资产 |
| | 3 | 独立开发者 2026 技术栈选择指南：少即是多 |
| **2B SaaS 从零到一** | 4 | 找到一个值得做的 SaaS 点子：需求验证全流程 |
| | 5 | 从零构建 SaaS：技术选型、MVP 开发与上线 |
| | 6 | SaaS 定价的底层逻辑：免费、订阅还是一次性买断 |
| | 7 | Notion 模板到 Gumroad：小产品赚钱的完整链路 |
| **2C 一人公司运营** | 8 | 零预算推广：Reddit、Product Hunt、Twitter 实战 |
| | 9 | 用户支持一人搞定：文档、Chatbot 与自动化 |
| | 10 | 一人公司的法律、税务与财务底线 |
| **2D 效率工具箱** | 11 | Hugo + GitHub Pages：程序员博客从零到上线 |
| | 12 | 博客 SEO 与变现：让搜索引擎找到你，让广告主付你钱 |
| | 13 | AI 编程实战：用 AI 助手提速 10 倍 |
| | 14 | AI 辅助代码审查：让 AI 帮你找 Bug |
| | 15 | Python 自动化：10 个日常重复工作一键搞定 |
| | 16 | Python 爬虫与报表：数据采集到可视化一条龙 |
| | 17 | 自动化部署：GitHub Actions + Cron 让你睡觉也在赚钱 |

### 系列 3：大厂程序员的工程思维（9 篇）

| 公司 | # | 标题 | 视角 |
|------|---|------|------|
| **微软** | 1 | 微软教会我的代码审查：为什么每一行代码都要有人看 | 硬核工程 |
| | 2 | 兼容性的艺术：Windows 三十年不崩的秘密 | 行业洞察 |
| | 3 | 从封闭到开放：我亲历的微软转型十年 | 人性叙事 |
| **谷歌** | 4 | Google SRE：为什么你的服务需要 SLI/SLO/SLA | 硬核工程 |
| | 5 | 设计文档文化：Google 如何用文字驱动工程 | 工程文化 |
| | 6 | OKR 的真相：Google 的目标管理到底是怎么回事 | 管理洞察 |
| **英伟达** | 7 | 英伟达的速度：黄仁勋的"光速文化"如何改变我 | 人性叙事 |
| | 8 | CUDA 的豪赌：一家显卡公司如何绑定了整个 AI 时代 | 行业洞察 |
| | 9 | 离开大厂之后：我带走的和丢掉的 | 人性收尾 |

### 汇总

| 系列 | 篇数 |
|------|------|
| 1. AI Agent 全解析 | 23 |
| 2. 独立开发者全栈指南 | 17 |
| 3. 大厂工程思维 | 9 |
| **合计** | **49** |

---

## 二、Chinese Cuisine · 美食

**定位**：英文叙事美食写作 + 科普带货。让外国人先爱上中国文化，再产生购买欲望。

**发布**：叙事文每天 12:00（cron，当前暂停中，推科普系列）

**图片**：叙事文 3 张/篇（用户提供），1200px≤200KB RGB JPG，OCR 铁门禁

**铁律**：叙事文禁 Amazon 链接 · 禁 emoji · 禁自动交叉链接 · 先飞书审→确认→部署

**路线图**：`~/side-hustle/cuisine_ROADMAP.md`

### A. 叙事文：109 Dishes of China

#### 一、The Classics · 世界名片（10 道）

| # | Dish | Chinese | 状态 |
|---|------|---------|------|
| 1 | Mapo Tofu | 麻婆豆腐 | ✅ |
| 2 | Kung Pao Chicken | 宫保鸡丁 | ✅ |
| 3 | Peking Duck | 北京烤鸭 | ✅ |
| 4 | Xiaolongbao | 小笼包 | ✅ |
| 5 | Sweet and Sour Pork | 咕咾肉 | ✅ |
| 6 | Yangzhou Fried Rice | 扬州炒饭 | ✅ |
| 7 | Dumplings | 饺子 | ⬜ |
| 8 | Hot Pot | 火锅 | ⬜ |
| 9 | Spring Rolls | 春卷 | ⬜ |
| 10 | Chow Mein | 炒面 | ⬜ |

#### 二、Sichuan & The Spice Belt · 川湘渝（12 道）

| # | Dish | Chinese | 状态 |
|---|------|---------|------|
| 11 | Dan Dan Noodles | 担担面 | ✅ |
| 12 | Twice-Cooked Pork | 回锅肉 | ✅ |
| 13 | Chongqing Spicy Chicken (Laziji) | 辣子鸡 | ✅ |
| 14 | Fish-Fragrant Eggplant | 鱼香茄子 | ⬜ |
| 15 | Yu Xiang Rou Si | 鱼香肉丝 | ✅ |
| 16 | Sichuan Boiled Fish | 水煮鱼 | ✅ |
| 17 | Couple's Beef Offal | 夫妻肺片 | ⬜ |
| 18 | Mouth-Watering Chicken (Kou Shui Ji) | 口水鸡 | ✅ |
| 19 | Chongqing Xiaomian | 重庆小面 | ⬜ |
| 20 | Chairman Mao's Red-Braised Pork | 毛氏红烧肉 | ⬜ |
| 21 | Duo Jiao Fish Head | 剁椒鱼头 | ⬜ |
| 22 | Changsha Stinky Tofu | 长沙臭豆腐 | ⬜ |

#### 三、Cantonese · 镬气与点心（12 道）

| # | Dish | Chinese | 状态 |
|---|------|---------|------|
| 23 | Dim Sum 全解 | 点心 | ⬜ |
| 24 | Char Siu | 叉烧 | ✅ |
| 25 | Wonton Noodles | 云吞面 | ⬜ |
| 26 | Beef Chow Fun (Gan Chao Niu He) | 干炒牛河 | ✅ |
| 27 | White Cut Chicken | 白切鸡 | ⬜ |
| 28 | Claypot Rice | 煲仔饭 | ⬜ |
| 29 | Roast Goose | 深井烧鹅 | ⬜ |
| 30 | Salt-Baked Chicken | 盐焗鸡 | ⬜ |
| 31 | Poon Choi | 盆菜 | ⬜ |
| 32 | Egg Tart | 蛋挞 | ⬜ |
| 33 | Double-Skin Milk | 双皮奶 | ⬜ |
| 34 | Mango Pomelo Sago | 杨枝甘露 | ⬜ |

#### 四、Shanghai & The Water Towns · 江南（12 道）

| # | Dish | Chinese | 状态 |
|---|------|---------|------|
| 35 | Shengjianbao | 生煎包 | ✅ |
| 36 | Hairy Crab | 大闸蟹 | ⬜ |
| 37 | Drunken Crab | 醉蟹 | ⬜ |
| 38 | Yan Du Xian | 腌笃鲜 | ⬜ |
| 39 | Lion's Head Meatball | 狮子头 | ✅ |
| 40 | Dongpo Pork | 东坡肉 | ✅ |
| 41 | Beggar's Chicken | 叫花鸡 | ⬜ |
| 42 | Squirrel Mandarin Fish | 松鼠桂鱼 | ⬜ |
| 43 | Sweet and Sour Ribs (Tang Cu Pai Gu) | 糖醋排骨 | ✅ |
| 44 | Wensi Tofu | 文思豆腐 | ⬜ |
| 45 | Crab Roe Soup Dumpling | 蟹黄汤包 | ⬜ |
| 46 | Crayfish | 小龙虾 | ⬜ |

#### 五、The Noodle Belt · 面食帝国（10 道）

| # | Dish | Chinese | 状态 |
|---|------|---------|------|
| 47 | Lanzhou Hand-Pulled Noodles | 兰州拉面 | ✅ |
| 48 | Biang Biang Noodles | 裤带面 | ⬜ |
| 49 | Oil-Splash Noodles (You Po Mian) | 油泼面 | ✅ |
| 50 | Beijing Zhajiang Noodles | 炸酱面 | ✅ |
| 51 | Qishan Saozi Noodles | 岐山臊子面 | ⬜ |
| 52 | Shanxi Sliced Noodles | 刀削面 | ⬜ |
| 53 | Sweet Water Noodles | 甜水面 | ⬜ |
| 54 | Wuhan Hot-Dry Noodles | 热干面 | ⬜ |
| 55 | Luosifen | 螺蛳粉 | ⬜ |
| 56 | Guilin Rice Noodles | 桂林米粉 | ⬜ |

#### 六、The Imperial North · 帝都·齐鲁·东北（10 道）

| # | Dish | Chinese | 状态 |
|---|------|---------|------|
| 57 | Beijing Mutton Hot Pot | 铜锅涮肉 | ⬜ |
| 58 | Braised Sea Cucumber | 葱烧海参 | ⬜ |
| 59 | Nine-Turn Intestine | 九转大肠 | ⬜ |
| 60 | Sweet-and-Sour Yellow River Carp | 糖醋鲤鱼 | ⬜ |
| 61 | Dezhou Braised Chicken | 德州扒鸡 | ⬜ |
| 62 | Oil-Braised Prawns | 油焖大虾 | ⬜ |
| 63 | Guo Bao Rou | 锅包肉 | ✅ |
| 64 | Earth's Three Fresh | 地三鲜 | ⬜ |
| 65 | Chicken & Mushroom Stew | 小鸡炖蘑菇 | ⬜ |
| 66 | Suan Cai Bai Rou | 酸菜白肉 | ⬜ |

#### 七、Into the Mountains · 云贵皖桂（10 道）

| # | Dish | Chinese | 状态 |
|---|------|---------|------|
| 67 | Crossing-Bridge Noodles | 过桥米线 | ⬜ |
| 68 | Steam-Pot Chicken | 汽锅鸡 | ⬜ |
| 69 | Xuanwei Ham | 宣威火腿 | ⬜ |
| 70 | Sour Soup Fish | 酸汤鱼 | ⬜ |
| 71 | Intestine Blood Noodles | 肠旺面 | ⬜ |
| 72 | Hairy Tofu | 毛豆腐 | ⬜ |
| 73 | Stinky Mandarin Fish | 臭鳜鱼 | ⬜ |
| 74 | Li Hongzhang Chop Suey | 李鸿章大杂烩 | ⬜ |
| 75 | Jinhua Ham | 金华火腿 | ⬜ |
| 76 | Hu La Tang | 胡辣汤 | ⬜ |

#### 八、The Far West · 新疆·陕西（8 道）

| # | Dish | Chinese | 状态 |
|---|------|---------|------|
| 77 | Xinjiang Lamb Skewers | 羊肉串 | ⬜ |
| 78 | Big-Plate Chicken | 大盘鸡 | ⬜ |
| 79 | Lamb Pilaf | 手抓饭 | ⬜ |
| 80 | Samsa / Kao Baozi | 烤包子 | ⬜ |
| 81 | Xi'an Roujiamo | 肉夹馍 | ✅ |
| 82 | Yangrou Paomo | 羊肉泡馍 | ⬜ |
| 83 | Liangpi | 凉皮 | ⬜ |
| 84 | Xinjiang Naan Bread | 馕 | ⬜ |

#### 九、Hot Pot, Cold Dishes & Dark Arts · 锅·冷·暗（10 道）

| # | Dish | Chinese | 状态 |
|---|------|---------|------|
| 85 | Chongqing Hot Pot | 重庆火锅 | ⬜ |
| 86 | Chaoshan Beef Hot Pot | 潮汕牛肉火锅 | ⬜ |
| 87 | Sichuan Chuan Chuan | 串串香 | ⬜ |
| 88 | Garlic-White Pork | 蒜泥白肉 | ⬜ |
| 89 | Century Egg Tofu | 皮蛋豆腐 | ⬜ |
| 90 | Century Egg | 皮蛋 | ⬜ |
| 91 | Chicken Feet | 凤爪 | ⬜ |
| 92 | Tanghulu | 冰糖葫芦 | ⬜ |
| 93 | Tianjin Jianbing | 煎饼果子 | ✅ |
| 94 | Buddha's Delight | 罗汉斋 | ⬜ |

#### 十、Sweet Endings & Morning Rituals · 早与甜（7 道）

| # | Dish | Chinese | 状态 |
|---|------|---------|------|
| 95 | Zongzi | 粽子 | ⬜ |
| 96 | Mooncake | 月饼 | ⬜ |
| 97 | Buddha Jumps Over the Wall | 佛跳墙 | ⬜ |
| 98 | Almond Tofu | 杏仁豆腐 | ⬜ |
| 99 | Fermented Mung Bean Milk | 豆汁儿 | ⬜ |
| 100 | Soy Milk + Youtiao | 豆浆油条 | ⬜ |
| 101 | Dragon's Beard Candy | 龙须糖 | ⬜ |

#### 十一、🆕 BBQ World · 烧烤江湖 — China on Charcoal（8 道）

| # | Dish | Chinese | 状态 |
|---|------|---------|------|
| 102 | Zhanjiang Grilled Oysters | 湛江烤生蚝 | ⬜ |
| 103 | Jinzhou BBQ Chicken Frame | 锦州烤鸡架 | ⬜ |
| 104 | Zibo BBQ | 淄博烧烤 | ⬜ |
| 105 | Yibin Hand-Held Roast | 宜宾把把烧 | ⬜ |
| 106 | Dai Minority Herb BBQ | 德宏傣味烧烤 | ⬜ |
| 107 | Grilled Pig Brain | 烤脑花 | ⬜ |
| 108 | Red Willow Branch Lamb | 红柳烤肉 | ⬜ |
| 109 | Grilled Pig Eyes | 烤猪眼 | ⬜ |

#### 其他已发（待归类）

| Dish | Chinese | 状态 |
|------|---------|------|
| Hong Shao Niu Rou Mian | 红烧牛肉面 | ✅ |
| Hong Shao Rou | 红烧肉 | ✅ |
| Steamed Fish Cantonese | 清蒸鱼 | ✅ |
| Suan Cai Yu | 酸菜鱼 | ✅ |
| Mei Cai Kou Rou | 梅菜扣肉 | ✅ |
| Scallion Oil Noodles | 葱油拌面 | ✅ |
| Tomato Egg Stir-Fry | 番茄炒蛋 | ✅ |

### B. 科普系列（带货，7 篇主力 + 5 篇次要）

**工作流**：先出结构 → 用户审核 → 调整 → 写草稿 → 推飞书中英文预览 → 用户确认 → 部署

**第一筛**："西方人会买吗？"——是则留，否则合并或砍掉

| # | 标题 | 格式 | 内容 | 状态 |
|---|------|------|------|------|
| **C01** | 11 件 Chinese Pantry 必备 | 产品导购 | 生抽/老抽/蚝油/料酒/香醋/豆瓣酱/花椒/五香粉/八角/干辣椒/冰糖 | 等用户发 11 图+11 链接 |
| **C02** | Wok 炒锅入门 | 装备导购 | 碳钢锅 vs 铸铁锅、平底 vs 圆底、开锅、养护 | 待出结构 |
| **C03** | Chinese Spices 101 | 产品导购 | 花椒/五香粉/八角/桂皮/丁香/草果/白芷/小茴香… | 待出结构 |
| **C04** | Chinese Vinegars | 产品导购 | 镇江香醋/山西老陈醋/米醋/白醋，每个的用途 | 待出结构 |
| **C05** | Dried Pantry 干货 | 产品导购 | 香菇/木耳/干贝/虾米/红枣/枸杞/腐竹… | 待出结构 |
| **C06** | Chinese Cleaver 菜刀 | 装备导购 | 中式片刀 vs 西式主厨刀、碳钢 vs 不锈钢、磨刀 | 待出结构 |
| **C07** | Bamboo Steamer 蒸笼 | 装备导购 | 竹蒸笼 vs 不锈钢、尺寸选型、蒸的技巧 | 待出结构 |

**次要 5 篇**（低优先）：

| 标题 | 内容 |
|------|------|
| Chinese Regional Cuisines Overview | 八大菜系概览 |
| Festival Foods of China | 春节/中秋/端午节日美食 |
| 12 Chinese Cooking Techniques | 爆炒蒸焖炖炸烧卤熘煸烩 |
| The Ultimate Hot Pot Guide | 火锅底料、蘸料、涮品选择 |
| How to Use Chopsticks | 筷子使用指南+礼仪 |

---

## 三、Chinese Tea · 茶

**定位**：把中国茶文化分享给全世界，内容先于带货。

**发布**：每周三、五 10:00（cron `1f2c1d51453f`）

**盈利**：Day 1 AdSense + Amazon Associates

**架构文件**：`~/side-hustle/content-site/_TEA-ARCHITECTURE.md`

### 五大支柱

| 支柱 | 定位 | 预估篇数 |
|------|------|----------|
| 茶 101 | 流量入口、AdSense 主力 | 5-8 |
| 茶种类 | 单品茶 + 集合文，精准转化 | 20+ 单品 + 5-8 集合 |
| 茶具 | 佣金主力 | 8-10 |
| 茶文化 | 权重、E-E-A-T | 10-15 |
| 送礼指南 | Phase 3 才上，季节性 | 3-5 |

### Phase 1：6 篇种子

| # | 标题 | 状态 |
|---|------|------|
| 1 | Six Types of Chinese Tea: A Beginner's Guide | ✅ 已发布 |
| 2 | Longjing: One Leaf, One Spring | ✅ 已发布 |
| 3 | Tieguanyin: The Iron Goddess in Your Cup | ✅ 已发布 |
| 4 | Ripe Pu'er: Old Libraries, Rain-Wet Earth | ✅ 已发布 |
| 5 | Gaiwan Brewing Guide | ⬜ 待写 |
| 6 | 1 篇文化文（工夫茶仪式 / 茶马古道 / 茶与禅——三选一） | ⬜ 待写 |

### Phase 2：扩展（目标 ~25 篇）

#### 茶种类 — 单品茶（20+ 篇）

| 大类 | 单品 |
|------|------|
| **绿茶** | 碧螺春 / 黄山毛峰 / 信阳毛尖 / 安吉白茶 / 太平猴魁 / 六安瓜片 / 恩施玉露 / 都匀毛尖 |
| **乌龙茶** | 大红袍 / 凤凰单丛 / 东方美人 / 冻顶乌龙 / 武夷肉桂 / 水仙 |
| **红茶** | 正山小种 / 金骏眉 / 祁门红茶 / 滇红 / 英红九号 |
| **黑茶** | 生普 / 六堡茶 / 安化黑茶 / 茯砖 |
| **白茶** | 白毫银针 / 白牡丹 / 寿眉 |
| **黄茶** | 君山银针 / 蒙顶黄芽 |

#### 茶种类 — 集合文（5-8 篇）

| 集合 |
|------|
| 中国绿茶合集 |
| 中国乌龙茶合集 |
| 中国黑茶合集 |
| 中国白茶合集 |
| 中国红茶合集 |
| 各省代表茶巡礼 |
| 中国花茶合集（茉莉花茶/桂花乌龙等） |

#### 茶 101（5-8 篇）

| 标题 |
|------|
| 中国茶叶入门：从零开始喝茶 |
| 泡茶水温指南：不同茶类的最佳温度 |
| 如何选购茶叶：品质判断的 5 个维度 |
| 茶叶储存：如何在最佳状态保存不同茶类 |
| 不同季节喝什么茶 |
| 功夫茶入门：一套茶具怎么用 |
| 茶桌礼仪速成 |

#### 茶具（8-10 篇）

| 标题 |
|------|
| 紫砂壶入门：泥料、壶型、养护 |
| 盖碗使用指南：三根手指泡出好茶（已有，P1#5） |
| 公道杯与品茗杯：选对茶器 |
| 茶盘选购指南 |
| 茶刀与茶针：撬开普洱茶的正确方式 |
| 茶宠：茶桌上的小玩意 |
| 建盏与天目：千年窑火 |
| 茶具套装推荐：不同预算 |
| 电陶炉 vs 随手泡：烧水设备选择 |
| 茶道六君子 |

#### 茶文化（10-15 篇）

| 标题 |
|------|
| 工夫茶仪式：潮汕人的日常 |
| 茶马古道：一条比丝绸之路更险的路 |
| 茶与禅：赵州和尚的"吃茶去" |
| 宋代点茶：被遗忘的喝茶方式 |
| 日本茶道与中国渊源 |
| 茶馆文化：成都 vs 北京 vs 广州 |
| 中国各地的喝茶习俗 |
| 茶叶外交：从鸦片战争到G20 |
| 陆羽与《茶经》 |
| 云南古茶树：活了上千年的茶树 |
| 茶山巡礼：武夷山/西湖/勐海 |

### Phase 3（DA 上来后）

| 支柱 | 内容 |
|------|------|
| **送礼指南** | 春节送茶指南 / 商务茶礼怎么选 / 不同预算茶礼推荐（3-5 篇） |
| **Best Of** | Best Green Tea 2026 / Best Oolong Tea 等搜索量驱动文章 |

---

## 四、Baijiu · 白酒

**定位**：专栏级深度内容，不是品类门户。叙事+文化路线。

**发布**：两周 1 篇 · 每周六 10:00（cron）

**禁做**：Amazon 酒类榜单、黄酒/啤酒/红酒扩展

| # | 内容 | 状态 |
|---|------|------|
| 1 | **The Moutai Puzzle: Why a Bottle Costs More Than Your Graphics Card** | ✅ 已发布 |
| 2 | **Baijiu 101：中国白酒入门** — 四大香型（酱香/浓香/清香/米香）、固态发酵工艺、产区地图、入门品鉴 | ⬜ 待写 |
| 3 | **人物故事** — 季克良与茅台的半个世纪 / 泸州老窖的 450 年窖池 / 一个酿酒师的日常 | ⬜ 待写 |
| 4 | **品鉴笔记** — 如何喝白酒：闻香/入口/回味 / 茅台 vs 五粮液 vs 国窖 1573 横评 / 白酒与餐食搭配 | ⬜ 待写 |
| 5 | **买酒指南** — 海外购买渠道（Drizly/Wine.com/当地中国超市）/ 入门口粮酒推荐（100-300 元档）/ 送礼场景选酒 | ⬜ 待写 |

---

## 全局 Cron 一览

| 时间 | 板块 | 频率 |
|------|------|------|
| 09:00 | Tech（周二） | 每周 1 篇 |
| 10:00 | 茶（周三/五） | 每周 2 篇 |
| 10:00 | 白酒（周六） | 两周 1 篇 |
| 12:00 | 美食叙事 | 每天 1 篇（当前暂停，推科普） |
| 22:00 | 每日复盘 | 每天 |
