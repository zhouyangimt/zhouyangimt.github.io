---
title: "🍜 Chinese Cuisine"
description: "109 authentic Chinese dishes — from Sichuan street fire to Cantonese dim sum. Every dish has a story, every photo makes you hungry."
type: "cuisine"
---

<div class="cuisine-intro">

A visual encyclopedia of China's most iconic dishes. **14 published · 95 incoming.**

</div>

<div class="cuisine-taxonomy">
  <div class="taxonomy-section">
    <h3>🏛️ The Eight Great Cuisines</h3>
    <div class="cuisine-grid-taxonomy">
      <div class="taxo-card"><span class="taxo-badge sichuan">🌶</span><strong>Sichuan</strong><span class="taxo-sub">川</span><p>Mapo Tofu, Kung Pao Chicken, Twice-Cooked Pork, Boiled Fish</p></div>
      <div class="taxo-card"><span class="taxo-badge cantonese">🥡</span><strong>Cantonese</strong><span class="taxo-sub">粤</span><p>Char Siu, White Cut Chicken, Claypot Rice, Dim Sum</p></div>
      <div class="taxo-card"><span class="taxo-badge jiangsu">🦀</span><strong>Jiangsu</strong><span class="taxo-sub">苏</span><p>Squirrel Fish, Lion's Head Meatballs, Nanjing Salted Duck</p></div>
      <div class="taxo-card"><span class="taxo-badge zhejiang">🍖</span><strong>Zhejiang</strong><span class="taxo-sub">浙</span><p>Dongpo Pork, Longjing Shrimp, West Lake Vinegar Fish</p></div>
      <div class="taxo-card"><span class="taxo-badge fujian">🍲</span><strong>Fujian</strong><span class="taxo-sub">闽</span><p>Buddha Jumps Over the Wall, Lychee Pork</p></div>
      <div class="taxo-card"><span class="taxo-badge hunan">🌶️</span><strong>Hunan</strong><span class="taxo-sub">湘</span><p>Chopped Pepper Fish Head, Stir-Fried Pork</p></div>
      <div class="taxo-card"><span class="taxo-badge anhui">🧄</span><strong>Anhui</strong><span class="taxo-sub">徽</span><p>Stinky Mandarin Fish, Hairy Tofu</p></div>
      <div class="taxo-card"><span class="taxo-badge shandong">🧅</span><strong>Shandong</strong><span class="taxo-sub">鲁</span><p>Braised Intestines, Scallion Sea Cucumber</p></div>
    </div>
  </div>

  <div class="taxonomy-section">
    <h3>➕ Four Special Collections</h3>
    <div class="cuisine-grid-taxonomy extra">
      <div class="taxo-card extra"><span class="taxo-badge street">🍢</span><strong>Street Eats</strong><p>Jianbing, Roujiamo, Shengjianbao, Skewers</p></div>
      <div class="taxo-card extra"><span class="taxo-badge noodles">🍜</span><strong>Noodles</strong><p>Lanzhou Beef Noodles, Dan Dan Noodles, Zhajiangmian, Daoxiaomian</p></div>
      <div class="taxo-card extra"><span class="taxo-badge bbq">🔥</span><strong>Chinese BBQ</strong><p>Xinjiang Lamb Skewers, Zhanjiang Oysters, Northeast Cold Noodles</p></div>
      <div class="taxo-card extra"><span class="taxo-badge regional">🏮</span><strong>Regional Gems</strong><p>Peking Duck, Shanghai Benbang, Chongqing Hotpot, Yunnan Cross-Bridge Noodles</p></div>
    </div>
  </div>

  <p class="taxonomy-note">Filter by region with the tabs below, or use the blog&rsquo;s built-in tag search for ingredients and cooking methods.</p>
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

/* ── Classification Taxonomy ── */
.cuisine-taxonomy {
  max-width: 900px;
  margin: 0 0 30px 0;
  padding: 20px 24px;
  background: #fafaf8;
  border-radius: 12px;
  border: 1px solid #eee;
}

.taxonomy-section {
  margin: 0 0 20px 0;
}

.taxonomy-section:last-of-type {
  margin-bottom: 10px;
}

.taxonomy-section h3 {
  margin: 0 0 12px 0;
  font-size: 1em;
  font-weight: 700;
  color: #333;
}

.cuisine-grid-taxonomy {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}

.cuisine-grid-taxonomy.extra {
  grid-template-columns: repeat(4, 1fr);
}

.taxo-card {
  padding: 10px 12px;
  background: #fff;
  border-radius: 8px;
  border: 1px solid #eee;
  font-size: 0.82em;
  line-height: 1.5;
}

.taxo-card strong {
  display: block;
  font-size: 0.9em;
  color: #222;
  margin: 4px 0 2px 0;
}

.taxo-card p {
  margin: 2px 0 0 0;
  color: #999;
  font-size: 0.85em;
}

.taxo-badge {
  display: inline-block;
  width: 28px;
  height: 28px;
  line-height: 28px;
  text-align: center;
  border-radius: 6px;
  font-size: 0.9em;
}

.taxo-badge.sichuan { background: #fef0f0; }
.taxo-badge.cantonese { background: #fdf6e3; }
.taxo-badge.jiangsu { background: #e8f4f8; }
.taxo-badge.zhejiang { background: #f5f0e8; }
.taxo-badge.fujian { background: #fff5e6; }
.taxo-badge.hunan { background: #ffe8e8; }
.taxo-badge.anhui { background: #f0f0e8; }
.taxo-badge.shandong { background: #fef9e8; }
.taxo-badge.street { background: #ffe8d0; }
.taxo-badge.noodles { background: #fff8e0; }
.taxo-badge.bbq { background: #fce4e4; }
.taxo-badge.regional { background: #f8e8f0; }

.taxo-sub {
  display: inline-block;
  margin-left: 4px;
  font-size: 0.78em;
  color: #aaa;
  vertical-align: middle;
}

.taxo-card.extra {
  border-style: dashed;
}

.taxonomy-note {
  margin: 14px 0 0 0;
  font-size: 0.82em;
  color: #aaa;
}

@media (max-width: 768px) {
  .cuisine-grid-taxonomy,
  .cuisine-grid-taxonomy.extra {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .cuisine-grid-taxonomy,
  .cuisine-grid-taxonomy.extra {
    grid-template-columns: 1fr;
  }
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
