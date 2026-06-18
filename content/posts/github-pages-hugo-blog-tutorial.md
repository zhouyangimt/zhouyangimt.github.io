---
title: "GitHub Pages + Hugo 搭建免费博客完整教程（2026版）"
date: 2026-06-04
tags: ["独立开发", "工具教程", "Hugo"]
description: "从零开始用Hugo和GitHub Pages搭建免费、高速的个人博客，含自定义域名配置。"
---

## 为什么选 Hugo + GitHub Pages？

- **完全免费**：GitHub Pages 免费托管，无流量限制
- **极速**：Hugo 是Go写的，构建速度毫秒级
- **Markdown 写作**：用你熟悉的格式写文章
- **版本控制**：所有文章都在 Git 里，永远不丢

## 第一步：安装 Hugo

```bash
# macOS
brew install hugo

# Linux
sudo snap install hugo

# Windows
choco install hugo-extended
```

## 第二步：创建站点

```bash
hugo new site my-blog
cd my-blog
git init
```

## 第三步：选主题

推荐几个轻量中文友好的主题：
- **PaperMod**：简洁、功能全
- **Stack**：卡片式、颜值高
- **LoveIt**：中文社区最流行的主题

```bash
git submodule add https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
echo "theme = 'PaperMod'" >> hugo.toml
```

## 第四步：写第一篇文章

```bash
hugo new posts/my-first-post.md
```

用 Markdown 写内容，Front Matter 里设置标题、日期、标签：

```yaml
---
title: "我的第一篇文章"
date: 2026-06-04
tags: ["入门"]
---
```

## 第五步：本地预览

```bash
hugo server -D
```

浏览器打开 `http://localhost:1313`，边写边看效果。

## 第六步：部署到 GitHub Pages

1. 在 GitHub 创建仓库：`你的用户名.github.io`
2. 在仓库 Settings → Pages 里，Source 选 **GitHub Actions**
3. 创建 `.github/workflows/hugo.yml`：

```yaml
name: Deploy Hugo
on:
  push:
    branches: [main]
jobs:
  build-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: peaceiris/actions-hugo@v2
      - run: hugo --minify
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
```

4. `git push`，GitHub Actions 自动构建部署。

## 第七步：绑定自定义域名

1. 在域名 DNS 里加一条 CNAME 记录指向 `你的用户名.github.io`
2. 在 `static/` 目录下创建 `CNAME` 文件，写入你的域名
3. GitHub Pages Settings 里填入自定义域名

## 总结

| 项目 | 成本 |
|------|------|
| 托管 | $0 |
| 域名（可选） | ~$10/年 |
| 主题 | 免费 |
| 维护 | 写 Markdown 即可 |

一个完全免费、速度飞起的个人博客，就这么简单。
