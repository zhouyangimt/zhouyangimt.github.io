#!/bin/bash
# Auto-deploy script - rebuild and push to GitHub Pages
set -e

SITE_DIR="$HOME/side-hustle/content-site"
cd "$SITE_DIR"

echo "=== Building Hugo site ==="
hugo --minify

echo "=== Deploying to GitHub Pages ==="
cd public

# Ensure git is set up
if [ ! -d .git ]; then
    git init
    git checkout -b main
    git remote add origin git@github.com:zhouyangimt/zhouyangimt.github.io.git
fi

git add -A
git commit -m "deploy: $(date +%Y-%m-%d)" || echo "Nothing to commit"
git push origin main 2>&1

echo "=== Deployed! https://zhouyangimt.github.io ==="
