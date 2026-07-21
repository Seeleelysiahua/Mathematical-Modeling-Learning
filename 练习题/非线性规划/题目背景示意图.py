import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# ==================== macOS 中文字体配置 ====================
zh_font = None
mac_fonts = ['PingFang SC', 'Heiti SC', 'STHeiti', 'Apple LiGothic', 'Songti SC']
for f in mac_fonts:
    if f in [font.name for font in fm.fontManager.ttflist]:
        zh_font = f
        break

if zh_font is None:
    for f in fm.fontManager.ttflist:
        if 'SC' in f.name or 'CN' in f.name or 'CJK' in f.name:
            zh_font = f.name
            break

if zh_font:
    plt.rcParams['font.sans-serif'] = [zh_font, 'DejaVu Sans']
else:
    print("警告：未检测到中文字体，中文可能显示为方框。")

plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150

# ==================== 绘图 ====================
fig = plt.figure(figsize=(12, 8), facecolor='#080c1a')
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor('#080c1a')
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.axis('off')

# 星空
np.random.seed(123)
stars_x = np.random.uniform(0, 12, 80)
stars_y = np.random.uniform(0, 8, 80)
ax.scatter(stars_x, stars_y, s=np.random.uniform(2, 8, 80),
           c='white', alpha=0.25, edgecolors='none')

def draw_info_box(ax, x, y, title, lines, title_color='#4a6fa5'):
    ax.text(x, y, title, fontsize=9, ha='center', va='center',
            color=title_color, weight='bold')
    for i, line in enumerate(lines):
        ax.text(x, y - 0.4 - i*0.35, line, fontsize=7.5, ha='center', va='center',
                color='#333333',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                          edgecolor='#aaaaaa', linewidth=0.5, alpha=0.95))

def map_coord(x, y):
    new_x = 2.5 + (x - 1.37) / (15.92 - 1.37) * 7.0
    new_y = 2.5 + (y - 5.0) / (18.0 - 5.0) * 4.0
    return new_x, new_y

# 左侧：手撕侠
left_cx, left_cy = 1.2, 4.0
ax.plot(left_cx, left_cy, 'o', color='white', markersize=18, markeredgewidth=1.5,
        markeredgecolor='#4a6fa5', zorder=5)
ax.text(left_cx, left_cy, '手', fontsize=10, ha='center', va='center',
        color='#4a6fa5', weight='bold', zorder=6)
ax.text(left_cx, left_cy-0.8, '手撕侠', fontsize=10, ha='center', va='center',
        color='white', weight='bold')
ax.text(left_cx, left_cy-1.3, '起点 A (4, 1)', fontsize=7.5, ha='center', va='center',
        color='#cccccc')
draw_info_box(ax, left_cx, left_cy-2.2, '约束与消耗',
              ['单日上限：20 只怪兽',
               '击杀消耗：3 馍 / 只',
               '赶路消耗：1 馍 / 100 km'])

# 右侧：燕双鹰
right_cx, right_cy = 10.8, 4.0
ax.plot(right_cx, right_cy, 'o', color='white', markersize=18, markeredgewidth=1.5,
        markeredgecolor='#c0845c', zorder=5)
ax.text(right_cx, right_cy, '燕', fontsize=9, ha='center', va='center',
        color='#c0845c', weight='bold', zorder=6)
ax.text(right_cx, right_cy-0.8, '燕双鹰', fontsize=10, ha='center', va='center',
        color='white', weight='bold')
ax.text(right_cx, right_cy-1.3, '起点 B (8, 9)', fontsize=7.5, ha='center', va='center',
        color='#cccccc')
draw_info_box(ax, right_cx, right_cy-2.2, '约束与消耗',
              ['单日上限：30 只怪兽',
               '击杀消耗：1 馍 / 只',
               '赶路消耗：3 馍 / 100 km'])

# 中心星球
planets = [
    ('A', 1.37, 10.21, 5),
    ('B', 9.45, 9.45, 9),
    ('C', 4.43, 8.88, 4),
    ('D', 6.66, 5.0, 8),
    ('E', 3.14, 16.44, 14),
    ('F', 15.92, 18.0, 11)
]
for name, x_raw, y_raw, num in planets:
    px, py = map_coord(x_raw, y_raw)
    # 星球圆点
    ax.plot(px, py, 'o', color='#e0e0e0', markersize=20, markeredgewidth=1.2,
            markeredgecolor='#555555', zorder=7)
    # 字母严格居中（不再加 0.05 偏移）
    ax.text(px, py, name, fontsize=8.5, ha='center', va='center',
            color='black', weight='bold', zorder=8)
    # 下方信息标注
    label = f"({x_raw:.2f}, {y_raw:.2f})\n怪兽 {num} 只"
    ax.text(px, py-0.75, label, fontsize=6.5, ha='center', va='top', color='#cccccc',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='#0f1530',
                      edgecolor='#555555', linewidth=0.5, alpha=0.9))

# 标题
ax.text(6, 7.5, '双人单日上限分配问题 — 星球信息总览', fontsize=14, ha='center', va='center',
        color='white', weight='bold',
        bbox=dict(facecolor='#080c1a', edgecolor='#4a6fa5', pad=0.6, boxstyle='round,pad=0.3'))

# 图例
ax.text(6, 0.6, '○ 手撕侠起点     □ 燕双鹰起点     ● 待维稳星球', fontsize=7.5, ha='center',
        color='#aaaaaa', style='italic')

# 保存
plt.savefig('assignment_diagram.png', dpi=300, bbox_inches='tight', facecolor='#080c1a')
plt.savefig('assignment_diagram.pdf', bbox_inches='tight', facecolor='#080c1a')
plt.show()