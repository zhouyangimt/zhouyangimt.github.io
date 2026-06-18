#!/bin/bash
# Content Site Deploy Script
# Build Hugo site and deploy to GitHub Pages / local output
set -e

SITE_DIR="$HOME/side-hustle/content-site"
OUTPUT_DIR="$SITE_DIR/public"

cd "$SITE_DIR"

echo "=== Building Hugo site ==="
hugo --minify

echo "=== Site built to: $OUTPUT_DIR ==="
echo ""
echo "To deploy to GitHub Pages:"
echo "  1. Create a GitHub repo: zhouyang/zhouyang.github.io"
echo "  2. Run: cd $OUTPUT_DIR && git init && git add -A && git commit -m 'deploy'"
echo "  3. git remote add origin git@github.com:zhouyang/zhouyang.github.io.git"
echo "  4. git push -f origin main:gh-pages"
echo ""
echo "To preview locally:"
echo "  cd $SITE_DIR && hugo server"
