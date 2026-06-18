---
title: "Hugo静态博客从入门到部署：比WordPress快10倍"
date: 2026-06-12
tags: ["独立开发", "工具教程", "Hugo"]
description: "为什么你应该用静态博客？Hugo安装、主题选择、部署到GitHub Pages完整教程。"
---

## WordPress vs 静态博客

WordPress的痛点：
- 需要服务器/PHP/MySQL
- 页面加载慢（除非花钱优化）
- 安全漏洞多（插件是重灾区）
- 编辑器卡顿

Hugo等静态博客：
- 纯HTML文件，加载飞起
- 免费托管（GitHub Pages / Cloudflare Pages）
- 没有数据库，没有后端，零漏洞
- Markdown写作，Git版本控制

**结论：做内容站，Hugo是正确答案。**

## Hugo是什么？

Go语言写的静态网站生成器。你把Markdown文章放进去，它输出一个完整的HTML网站。

**核心数据**：
- 构建速度：1000篇文章 < 1秒
- 主题数量：300+
- 配置文件：一个 `hugo.toml`

## 安装Hugo

```bash
# macOS
brew install hugo

# Linux (Ubuntu/Debian)
sudo snap install hugo

# 验证安装
hugo version
```

## 创建站点 - 5分钟

```bash
hugo new site my-blog
cd my-blog
```

目录结构：
```
my-blog/
  content/    ← 文章放这里
  themes/     ← 主题
  static/     ← 图片/CSS/JS
  hugo.toml   ← 配置文件
```

## 选主题

推荐几个适合中文博客的：

| 主题 | 风格 | 适合 |
|------|------|------|
| PaperMod | 极简 | 技术博客 |
| Stack | 卡片式 | 个人博客 |
| LoveIt | 功能多 | 中文博客 |
| Congo | 现代 | 综合 |

安装PaperMod：
```bash
git submodule add https://github.com/adityatelange/hugo-PaperMod themes/PaperMod
echo 'theme = "PaperMod"' >> hugo.toml
```

## 写文章

```bash
hugo new posts/my-first-post.md
```

文章格式（Front Matter + Markdown）：

```yaml
---
title: "文章标题"
date: 2026-06-12
tags: ["标签1", "标签2"]
description: "文章摘要"
---
正文内容（Markdown格式）……
```

## 本地预览

```bash
hugo server -D
```

浏览器打开 http://localhost:1313 ，边写边看。修改文章自动刷新。

## 部署到GitHub Pages

### 1. 创建仓库
在GitHub上创建 `你的用户名.github.io`

### 2. 配置GitHub Actions
创建 `.github/workflows/hugo.yml`:

```yaml
name: Deploy Hugo
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: true
      - uses: peaceiris/actions-hugo@v2
      - run: hugo --minify
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
```

### 3. 推送代码
```bash
git remote add origin git@github.com:你的用户名/你的用户名.github.io.git
git add .
git commit -m "init blog"
git push -u origin main
```

等待GitHub Actions跑完，访问 `https://你的用户名.github.io` 就能看到博客了。

## 进阶配置

### 自定义域名
1. 在 `static/` 下创建 `CNAME` 文件，写入你的域名
2. DNS里加CNAME记录指向 `你的用户名.github.io`
3. GitHub仓库Settings → Pages → 填入域名

### SEO优化
- 每篇文章写好 `description`
- 配置 `sitemap.xml`（Hugo默认生成）
- 提交到Google Search Console

### 评论系统
- Giscus（基于GitHub Discussions，免费）
- Disqus（有广告）

## 总结

| 对比项 | WordPress | Hugo |
|--------|-----------|------|
| 速度 | 慢 | 极快 |
| 费用 | 服务器$5-20/月 | $0 |
| 安全 | 需要维护 | 零漏洞 |
| 写作 | 网页编辑器 | Markdown |

**一个程序员的内容站，Hugo是起点也是终点。**
