import matplotlib.pyplot as plt

# ========== 1. Mac 中文字体配置（稳定兼容） ==========
plt.rcParams['font.sans-serif'] = ['STHeiti', 'Hiragino Sans GB', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 120

# ========== 2. 原始数据 ==========
goods_id = list(range(1, 11))
weight = [6, 3, 4, 5, 1, 2, 3, 5, 4, 2]
profit = [540, 200, 180, 350, 60, 150, 280, 450, 320, 120]
max_weight = 30

# ========== 3. 计算性价比，按单位重量利润降序排序 ==========
# 打包为 (编号, 重量, 利润, 单位利润)
goods = list(zip(goods_id, weight, profit, [p/w for p, w in zip(profit, weight)]))
goods_sorted = sorted(goods, key=lambda x: x[3], reverse=True)  # 按性价比从高到低排

# ========== 4. 模拟贪心算法选取过程 ==========
cum_weight = [0]    # 累计重量序列
cum_profit = [0]    # 累计利润序列
selected_idx = []   # 选中的货物在排序后列表中的索引

current_w = 0
current_p = 0
for i, item in enumerate(goods_sorted):
    if current_w + item[1] <= max_weight:
        current_w += item[1]
        current_p += item[2]
        selected_idx.append(i)
    cum_weight.append(current_w)
    cum_profit.append(current_p)

# ========== 5. 绘制可视化图表 ==========
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8), gridspec_kw={'height_ratios': [2, 1.5]})

# -------------------- 子图1：按性价比排序的货物对比（贪心选取结果） --------------------
sorted_ids = [item[0] for item in goods_sorted]
sorted_ratio = [item[3] for item in goods_sorted]
colors = ['#27AE60' if i in selected_idx else '#E74C3C' for i in range(len(goods_sorted))]

bars = ax1.bar(range(len(sorted_ids)), sorted_ratio, color=colors, alpha=0.85)
ax1.set_xticks(range(len(sorted_ids)))
ax1.set_xticklabels([f'货物{item[0]}' for item in goods_sorted])
ax1.set_ylabel('单位重量利润 (元/吨)', fontsize=11)
ax1.set_title('贪心算法核心：按「单位重量利润」从高到低依次选取', fontsize=13, fontweight='bold', pad=10)

# 标注每个柱子的性价比数值
for bar, ratio in zip(bars, sorted_ratio):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
             f'{ratio:.1f}', ha='center', va='bottom', fontsize=9)

# 添加图例
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor='#27AE60', label='贪心选中'),
                   Patch(facecolor='#E74C3C', label='载重不足，舍弃')]
ax1.legend(handles=legend_elements, loc='upper right')

# -------------------- 子图2：贪心选取过程累计重量变化 --------------------
steps = range(len(cum_weight))
ax2.plot(steps, cum_weight, marker='o', color='#2D68C4', linewidth=2, markersize=6, label='累计装载重量')
ax2.axhline(y=max_weight, color='#E74C3C', linestyle='--', linewidth=1.5, label=f'载重上限 {max_weight}t')

ax2.set_xlabel('选取步骤（按性价比顺序依次尝试）', fontsize=11)
ax2.set_ylabel('累计重量 (吨)', fontsize=11)
ax2.set_title('贪心选取过程：载重耗尽即停止，不回溯', fontsize=13, fontweight='bold', pad=10)
ax2.set_xticks(steps)
ax2.grid(axis='y', alpha=0.3)
ax2.legend(loc='lower right')

# 标注最终结果
ax2.text(len(steps)-1, cum_weight[-1],
         f'最终载重: {cum_weight[-1]}t\n总利润: {cum_profit[-1]}元',
         ha='right', va='bottom', fontsize=10,
         bbox=dict(facecolor='white', alpha=0.8, edgecolor='#27AE60'))

# ========== 6. 整体调整与导出 ==========
plt.suptitle('0-1背包问题 · 贪心算法原理可视化', fontsize=15, fontweight='bold', y=0.99)
plt.tight_layout()
plt.savefig('贪心算法核心原理图解.pdf', format='pdf', bbox_inches='tight')
plt.show()
