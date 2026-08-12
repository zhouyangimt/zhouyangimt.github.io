#!/usr/bin/env python3
"""Add Zhu Ye Qing card to tea/index.html Green Teas section."""
with open('tea/index.html', 'r') as f:
    html = f.read()

new_card = (
    '<article class=cuisine-card>'
    '<div class=cuisine-thumb><img src=/images/zhuyeqing-cover.jpg alt="Zhu Ye Qing" loading=lazy></div>'
    '<div class=cuisine-info>'
    '<h3><a href=/tea/zhuyeqing-bamboo-leaf-mountain/>Zhu Ye Qing: Bamboo Leaves from the Mountain Where Monkeys Pick Tea</a></h3>'
    '<div class=cuisine-tags>'
    '<span class=cuisine-tag>green-tea</span>'
    '<span class=cuisine-tag>zhu-ye-qing</span>'
    '<span class=cuisine-tag>sichuan</span>'
    '<span class=cuisine-tag>emei-shan</span>'
    '<span class=cuisine-tag>buddhist-tea</span>'
    '<span class=cuisine-tag>high-mountain</span>'
    '</div>'
    '<p class=cuisine-desc>Flat as bamboo leaves, grown on China\'s most sacred Buddhist mountain — the green tea that tastes like altitude and was perfected by monks a thousand years ago.</p>'
    '</div></article>'
)

# Find the Xinyang Maojian card end and insert after it
# The Xinyang Maojian card is the last in Green Teas section, before the Oolong section header
anchor = '<h2 class=tea-section-title>Oolong Teas</h2>'
if anchor not in html:
    print("ERROR: Oolong Teas anchor not found")
    exit(1)

html = html.replace(anchor, new_card + anchor, 1)

with open('tea/index.html', 'w') as f:
    f.write(html)

# Verify
card_count = html.count('<article class=cuisine-card>')
print(f"Tea index card count: {card_count}")
if 'zhuyeqing' in html.lower():
    print("OK: Zhu Ye Qing present in tea index")
else:
    print("ERROR: Zhu Ye Qing not found!")
