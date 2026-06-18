#!/bin/bash
# Content Site Deploy Script
# Build Hugo site and deploy to GitHub Pages
set -e

SITE_DIR="$HOME/side-hustle/content-site"
OUTPUT_DIR="$SITE_DIR/public"

cd "$SITE_DIR"

echo "=== Building Hugo site ==="
hugo --minify
echo "✅ Build done ($(du -sh "$OUTPUT_DIR" | cut -f1))"

# Check if git remote is configured
REMOTE=$(git remote get-url origin 2>/dev/null || echo "")

if [ -n "$REMOTE" ]; then
    echo ""
    echo "=== Deploying to GitHub Pages ==="
    git add .
    git commit -m "Deploy: $(date '+%Y-%m-%d %H:%M')" || echo "(nothing to commit)"
    git push origin master 2>&1 || echo "⚠️  Push failed. Check your SSH key and remote config."
    echo "Remote: $REMOTE"
else
    echo ""
    echo "⚠️  No git remote set. Skipping deploy."
    echo "To deploy, run:"
    echo "  cd $SITE_DIR"
    echo "  git remote add origin git@github.com:zhouyang/zhouyang.github.io.git"
    echo "  git push -u origin master"
    echo "Then enable GitHub Pages in repo Settings."
fi

echo ""
echo "=== Done ==="
