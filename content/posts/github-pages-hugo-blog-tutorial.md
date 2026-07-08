---
title: "GitHub Pages + Hugo 搭建免费博客完整教程（2026版）"
date: 2026-06-04
description: "从零开始用Hugo和GitHub Pages搭建免费、高速的个人博客，含自定义域名配置。"
tags: [独立开发, 工具教程, Hugo]
draft: false
---

## 为什么选 Hugo + GitHub Pages？
- **完全免费**：GitHub Pages 免费托管，无流量限制- **极速**：Hugo 是Go写的，构建速度毫秒级- **Markdown 写作**：用你熟悉的格式写文章- **版本控制**：所有文章都在 Git 里，永远不丢
## 第一步：安装 Hugo
# macOS
brew install hugo

# Linux
sudo snap install hugo

# Windows
choco install hugo-extended
`
## 第二步：创建站点
hugo new site my-blog
cd my-blog
git init
`
## 第三步：选主题
推荐几个轻量中文友好的主题：- **PaperMod**：简洁、功能全- **Stack**：卡片式、颜值高- **LoveIt**：中文社区最流行的主题git submodule add https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
echo &#34;theme = &#39;PaperMod&#39;&#34; &gt;&gt; hugo.toml
`
## 第四步：写第一篇文章
hugo new posts/my-first-post.md
`用 Markdown 写内容，Front Matter 里设置标题、日期、标签：---
title: &#34;我的第一篇文章&#34;
date: 2026-06-04
tags: [&#34;入门&#34;]
---
`
## 第五步：本地预览
hugo server -D
`浏览器打开 `http://localhost:1313`，边写边看效果。
## 第六步：部署到 GitHub Pages
- 在 GitHub 创建仓库：`你的用户名.github.io`- 在仓库 Settings → Pages 里，Source 选 **GitHub Actions**- 创建 `.github/workflows/hugo.yml`：name: Deploy Hugo
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
`- `git push`，GitHub Actions 自动构建部署。
## 第七步：绑定自定义域名
- 在域名 DNS 里加一条 CNAME 记录指向 `你的用户名.github.io`- 在 `static/` 目录下创建 `CNAME` 文件，写入你的域名- GitHub Pages Settings 里填入自定义域名
## 总结
项目成本托管$0域名（可选）~$10/年主题免费维护写 Markdown 即可一个完全免费、速度飞起的个人博客，就这么简单。