---
title: "🍜 Chinese Cuisine"
description: "109 authentic Chinese dishes — from Sichuan street fire to Cantonese dim sum. Every dish has a story, every photo makes you hungry."
type: "cuisine"
---

<div class="cuisine-intro">

A visual encyclopedia of China's most iconic dishes. **14 published · 95 incoming.** Click a region to filter, or scroll through them all.

</div>

<style>
.cuisine-intro {
  max-width: 700px;
  margin: 0 0 30px 0;
  font-size: 1.05em;
  line-height: 1.7;
  color: #444;
}

.cuisine-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 0 0 25px 0;
  padding-bottom: 20px;
  border-bottom: 2px solid #eee;
}

.cuisine-tab {
  display: inline-block;
  padding: 6px 14px;
  border-radius: 20px;
  background: #f5f5f5;
  color: #555;
  text-decoration: none;
  font-size: 0.9em;
  transition: all 0.2s;
  border: 1px solid transparent;
}

.cuisine-tab:hover {
  background: #e8e8e8;
}

.cuisine-tab.active {
  background: #d4491c;
  color: #fff;
  border-color: #d4491c;
  font-weight: 600;
}

.cuisine-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin: 0 0 30px 0;
}

.cuisine-card {
  border-radius: 10px;
  overflow: hidden;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  transition: transform 0.2s, box-shadow 0.2s;
}

.cuisine-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
}

.cuisine-card a {
  text-decoration: none;
  color: inherit;
  display: block;
}

.cuisine-thumb {
  width: 100%;
  height: 180px;
  overflow: hidden;
  background: #f0f0f0;
}

.cuisine-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.cuisine-card:hover .cuisine-thumb img {
  transform: scale(1.05);
}

.cuisine-info {
  padding: 14px 16px;
}

.cuisine-info h3 {
  margin: 0 0 6px 0;
  font-size: 1em;
  font-weight: 700;
  line-height: 1.3;
  color: #222;
}

.cuisine-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin: 0 0 6px 0;
}

.cuisine-tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 10px;
  background: #fdf2ed;
  color: #d4491c;
  font-size: 0.72em;
  font-weight: 500;
}

.cuisine-desc {
  margin: 0;
  font-size: 0.82em;
  color: #888;
  line-height: 1.4;
}

.cuisine-empty {
  text-align: center;
  padding: 40px 0;
  color: #999;
}

@media (max-width: 640px) {
  .cuisine-grid {
    grid-template-columns: 1fr;
  }
  .cuisine-nav {
    justify-content: center;
  }
  .cuisine-tab {
    font-size: 0.82em;
    padding: 5px 10px;
  }
}
</style>
