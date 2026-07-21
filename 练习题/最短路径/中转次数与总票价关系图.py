import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Heiti SC', 'PingFang SC']
plt.rcParams['axes.unicode_minus'] = False

# 数据： (目标, 中转次数, 总票价)
data = [
    ('c₂', 1, 35),
    ('c₃', 2, 45),
    ('c₄', 1, 35),
    ('c₅', 0, 25),
    ('c₆', 0, 10)
]

transfers = [d[1] for d in data]
costs = [d[2] for d in data]
labels = [d[0] for d in data]

plt.figure(figsize=(6, 5))
# 气泡大小代表票价
sizes = [c*15 for c in costs]
scatter = plt.scatter(transfers, costs, s=sizes, c=costs, cmap='YlOrRd',
                      edgecolors='black', alpha=0.8)

# 标注城市名
for i, label in enumerate(labels):
    plt.text(transfers[i]+0.1, costs[i]+1, label, fontsize=11, fontweight='bold')

plt.xlabel('中转次数', fontsize=12)
plt.ylabel('总票价（元）', fontsize=12)
plt.title('中转次数与最低票价的关系', fontsize=14, fontweight='bold')
plt.xticks([0,1,2])
plt.grid(True, linestyle='--', alpha=0.4)
plt.tight_layout()
plt.savefig('scatter_transfer_cost.pdf', format='pdf', bbox_inches='tight')
plt.show()