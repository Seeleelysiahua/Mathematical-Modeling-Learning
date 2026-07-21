import matplotlib.pyplot as plt
import numpy as np

# ======================
# 0. 全局字体设置（Mac 适用）
# ======================
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Heiti SC', 'PingFang SC']
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

# ======================
# 1. 数据定义
# ======================
INF = 10 ** 12
n = 6
C = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 50, INF, 40, 25, 10],
    [0, 50, 0, 15, 20, INF, 25],
    [0, INF, 15, 0, 10, 20, INF],
    [0, 40, 20, 10, 0, 100, 25],
    [0, 25, INF, 20, 100, 0, 55],
    [0, 10, 25, INF, 25, 55, 0]
]

# ======================
# 2. Dijkstra 并记录历史
# ======================
dist = [INF] * (n + 1)
dist[1] = 0
S = {1}
T = set(range(2, n + 1))

for v in range(2, n + 1):
    if C[1][v] < INF:
        dist[v] = C[1][v]

history = [(S.copy(), dist.copy())]  # 第0轮

while T:
    u = min(T, key=lambda x: dist[x])
    S.add(u)
    T.remove(u)
    for v in T:
        if C[u][v] < INF:
            nd = dist[u] + C[u][v]
            if nd < dist[v]:
                dist[v] = nd
    history.append((S.copy(), dist.copy()))

# ======================
# 3. 绘图数据准备
# ======================
rounds = list(range(len(history)))  # 0~5
cities = [1, 2, 3, 4, 5, 6]
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

# 计算所有有限票价的最大值，用于设定 Y 轴上限
all_finite = [d for _, d_arr in history for d in d_arr[1:] if d < INF]
max_finite = max(all_finite) if all_finite else 100

plt.figure(figsize=(9, 6))

for idx, node in enumerate(cities):
    # 提取每轮距离，并用 None 替代 INF
    dist_values = [h[1][node] if h[1][node] < INF else None for h in history]

    # 永久节点标记
    perm_mask = [node in h[0] for h in history]

    # 折线
    plt.plot(rounds, dist_values, color=colors[idx], linewidth=2,
             label=f'$c_{node}$')

    # 在永久节点轮次处加实心标记
    perm_rounds = [r for r, is_perm in enumerate(perm_mask) if is_perm]
    perm_dists = [history[r][1][node] for r in perm_rounds]
    valid = [(r, d) for r, d in zip(perm_rounds, perm_dists) if d is not None]
    if valid:
        r_vals, d_vals = zip(*valid)
        plt.scatter(r_vals, d_vals, color=colors[idx], s=80, zorder=5,
                    edgecolors='black', linewidths=0.8)

# ======================
# 4. 坐标轴与外观
# ======================
plt.xlabel('迭代轮次', fontsize=12)
plt.ylabel('临时距离 (票价)', fontsize=12)
plt.title('Dijkstra 算法距离收敛曲线', fontsize=14, fontweight='bold')

# 手动设定 Y 轴范围，防止空白
plt.ylim(bottom=0, top=max_finite + 20)
plt.xticks(rounds)
plt.legend(loc='upper right', fontsize=10)
plt.grid(True, linestyle='--', alpha=0.6)

# 注释：实心标记含义
plt.text(0.5, -0.12, '● 实心标记表示该节点已被纳入永久集合 S',
         transform=plt.gca().transAxes, ha='center', fontsize=10, style='italic')

plt.tight_layout()

# 保存时自动裁剪空白边框
plt.savefig('convergence_curve.pdf', format='pdf', bbox_inches='tight')
plt.show()