from pulp import LpProblem, LpVariable, LpMaximize, value

# 1. 定义基础数据
n = 10  # 货物数量
max_weight = 30  # 货车最大载重
weight = [6, 3, 4, 5, 1, 2, 3, 5, 4, 2]  # 每件货物重量，对应物品1~10
profit = [540, 200, 180, 350, 60, 150, 280, 450, 320, 120]  # 每件货物利润

# 2. 创建问题实例，目标为最大化利润
prob = LpProblem("货物运输最大利润", sense=LpMaximize)

# 3. 定义0-1决策变量：x[i]=1表示运送第i+1件货物，x[i]=0表示不运送
x = [LpVariable(f"x{i+1}", cat="Binary") for i in range(n)]

# 4. 添加目标函数：总利润最大化
prob += sum(profit[i] * x[i] for i in range(n)), "总利润"

# 5. 添加约束条件：总重量不超过货车载重
prob += sum(weight[i] * x[i] for i in range(n)) <= max_weight, "载重约束"

# 6. 求解问题
prob.solve()

# 7. 输出结果
print("求解状态:", prob.status)  # 1表示找到最优解
print("最大总利润:", value(prob.objective), "元")
print("选中运送的货物编号：")
selected = []
total_w = 0
for i in range(n):
    if value(x[i]) == 1:
        selected.append(i+1)
        total_w += weight[i]
print(selected)
print("总装载重量:", total_w, "吨")

import matplotlib.pyplot as plt

# ========== Mac 稳定可用的中文字体配置 ==========
# 按优先级 fallback，前面的找不到就自动用后面的
plt.rcParams['font.sans-serif'] = ['STHeiti', 'Hiragino Sans GB', 'Arial Unicode MS', 'PingFang SC']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示异常
plt.rcParams['figure.dpi'] = 120


# ========== 2. 题目原始数据 ==========
goods_id = list(range(1, 11))  # 货物编号1~10
weight = [6, 3, 4, 5, 1, 2, 3, 5, 4, 2]  # 重量（吨）
profit = [540, 200, 180, 350, 60, 150, 280, 450, 320, 120]  # 利润（元）

# 最优解：选中的货物编号
selected = [1, 2, 4, 6, 7, 8, 9, 10]
total_weight = sum(weight[i-1] for i in selected)
total_profit = sum(profit[i-1] for i in selected)

# ========== 3. 创建画布：2行1列子图 ==========
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# -------------------- 子图1：货物属性双轴对比图 --------------------
bar_width = 0.35
x = range(len(goods_id))

# 左轴：重量
ax1_bar = ax1.bar([i - bar_width/2 for i in x], weight, width=bar_width,
                  color='#4C72B0', label='重量(t)', alpha=0.8)
ax1.set_ylabel('重量 (t)', fontsize=11)
ax1.set_xticks(x)
ax1.set_xticklabels(goods_id)
ax1.set_xlabel('货物编号', fontsize=11)
ax1.set_title('10件货物重量与利润对比', fontsize=13, fontweight='bold', pad=10)

# 右轴：利润
ax1_twin = ax1.twinx()
ax1_bar2 = ax1_twin.bar([i + bar_width/2 for i in x], profit, width=bar_width,
                        color='#DD8452', label='利润(元)', alpha=0.8)
ax1_twin.set_ylabel('利润 (元)', fontsize=11)

# 合并图例
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax1_twin.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

# -------------------- 子图2：最优方案选择结果图 --------------------
# 按选中/未选中分配颜色
colors = ['#2ECC71' if i+1 in selected else '#E74C3C' for i in range(len(goods_id))]
bars = ax2.bar(goods_id, profit, color=colors, alpha=0.8)

# 标注选中状态
for i, bar in enumerate(bars):
    height = bar.get_height()
    status = '选中' if (i+1) in selected else '未选'
    ax2.text(bar.get_x() + bar.get_width()/2, height + 10, status,
             ha='center', va='bottom', fontsize=9)

ax2.set_xlabel('货物编号', fontsize=11)
ax2.set_ylabel('单件利润 (元)', fontsize=11)
ax2.set_title(f'最优运送方案结果（总载重：{total_weight}t，总利润：{total_profit}元）',
              fontsize=13, fontweight='bold', pad=10)
ax2.set_xticks(goods_id)

# 添加图例
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor='#2ECC71', label='选中运送'),
                   Patch(facecolor='#E74C3C', label='不运送')]
ax2.legend(handles=legend_elements, loc='upper right')

# ========== 4. 调整布局并保存 ==========
plt.tight_layout()
# 导出PDF矢量图，可直接插入LaTeX，无限放大不模糊
plt.savefig('货物运输最优方案图.pdf', format='pdf', bbox_inches='tight')
plt.show()
