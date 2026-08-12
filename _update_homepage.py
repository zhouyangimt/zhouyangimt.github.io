#!/usr/bin/env python3
"""Update homepage tea section: add Zhu Ye Qing card, remove Biluochun."""
import re

with open('index.html', 'r') as f:
    html = f.read()

# New Zhu Ye Qing card
new_card = (
    '<article class=cuisine-card>'
    '<div class=cuisine-thumb><img src=/images/zhuyeqing-cover.jpg alt="Zhu Ye Qing" loading=lazy></div>'
    '<div class=cuisine-info>'
    '<h3><a href=/tea/zhuyeqing-bamboo-leaf-mountain/>Zhu Ye Qing: Bamboo Leaves from the Mountain Where Monkeys Pick Tea</a></h3>'
    '<div class=meta><time>2026-08-12</time></div>'
    '<p class=summary>Flat as bamboo leaves, grown on China\'s most sacred Buddhist mountain, and picked one bud at a time before spring arrives — the green tea that tastes like altitude.</p>'
    '</div></article>'
)

# Insert new card at the start of the tea grid (right after '<section class=cuisine-grid>' that follows tea-header)
# Find the tea section grid
tea_section_pattern = r'(<section class="section-header tea-header">.*?</section><section class=cuisine-grid>)'
match = re.search(tea_section_pattern, html)
if not match:
    print("ERROR: Could not find tea section grid")
    exit(1)

insert_pos = match.end()
html = html[:insert_pos] + new_card + html[insert_pos:]

# Remove the Biluochun card (last card in tea section)
biluochun_pattern = r'<article class=cuisine-card><div class=cuisine-thumb><img src=/images/biluochun-cover\.jpg alt="Biluochun" loading=lazy></div><div class=cuisine-info><h3><a href=/tea/biluochun-green-snail-spring/>Biluochun: The Green Snail That Frightens the Fragrance</a></h3><div class=meta><time>2026-07-18</time></div><p class=summary>Rolled into tight spirals, covered in silver down, and grown among fruit trees on a lake island in Su[^<]*</p></div></article>'
html = re.sub(biluochun_pattern, '', html)

with open('index.html', 'w') as f:
    f.write(html)

# Verify
card_count = html.count('<article class=cuisine-card>')
print(f"Total cuisine-card count: {card_count}")

# Count tea section cards specifically
tea_start = html.find('tea-header')
tea_end = html.find('baijiu-header')
tea_section = html[tea_start:tea_end]
tea_card_count = tea_section.count('<article class=cuisine-card>')
print(f"Tea section card count: {tea_card_count}")

# Verify Biluochun is gone
if 'biluochun' in tea_section.lower():
    print("WARNING: Biluochun still in tea section!")
else:
    print("OK: Biluochun removed from tea section")

# Verify Zhu Ye Qing present
if 'zhuyeqing' in html.lower():
    print("OK: Zhu Ye Qing present in homepage")
else:
    print("ERROR: Zhu Ye Qing not found in homepage!")
