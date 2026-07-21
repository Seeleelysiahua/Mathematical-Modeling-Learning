import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# ======================
# 1. 构建图结构
# ======================
G = nx.Graph()
cities = ['c₁', 'c₂', 'c₃', 'c₄', 'c₅', 'c₆']
G.add_nodes_from(cities)

# 仅添加存在直达航线的边（票价）
edges = [
    ('c₁', 'c₂', 50),
    ('c₁', 'c₄', 40),
    ('c₁', 'c₅', 25),
    ('c₁', 'c₆', 10),
    ('c₂', 'c₃', 15),
    ('c₂', 'c₄', 20),
    ('c₂', 'c₆', 25),
    ('c₃', 'c₄', 10),
    ('c₃', 'c₅', 20),
    ('c₄', 'c₆', 25),
    ('c₄', 'c₅', 100),
    ('c₅', 'c₆', 55)
]
G.add_weighted_edges_from(edges)

# ======================
# 2. 自定义坐标布局（c₆ 位于几何中心）
# ======================
pos = {
    'c₁': (0, 0),
    'c₂': (2, 1),
    'c₃': (4, 1),
    'c₄': (3, -1),
    'c₅': (5, 0),
    'c₆': (2, -2)      # 中心位置
}

# ======================
# 3. 边宽映射：票价越低，线越粗
# ======================
prices = [d['weight'] for _, _, d in G.edges(data=True)]
min_price, max_price = min(prices), max(prices)
# 映射到线宽 1.0 ~ 5.0（票价 10 → 线宽 5，票价 100 → 线宽 1）
def price_to_width(price):
    return 1.0 + 4.0 * (max_price - price) / (max_price - min_price)

edge_widths = [price_to_width(d['weight']) for _, _, d in G.edges(data=True)]
edge_labels = nx.get_edge_attributes(G, 'weight')

# ======================
# 4. 绘图
# ======================
plt.figure(figsize=(8, 6))

# 4.1 绘制边（根据宽度）
nx.draw_networkx_edges(G, pos, width=edge_widths, edge_color='gray', alpha=0.8)

# 4.2 绘制节点：源点 c₁ 用星形，其余用圆形
# 先绘制普通节点（c₂~c₆）
other_nodes = [c for c in cities if c != 'c₁']
nx.draw_networkx_nodes(G, pos, nodelist=other_nodes,
                       node_shape='o', node_size=700,
                       node_color='lightblue', edgecolors='black', linewidths=1.2)

# 再绘制源点 c₁（星形 + 纯色填充）
nx.draw_networkx_nodes(G, pos, nodelist=['c₁'],
                       node_shape='*', node_size=900,
                       node_color='orange', edgecolors='darkred', linewidths=1.5)

# 4.3 绘制节点标签
nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')

# 4.4 绘制边标签（票价）
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                             font_size=10, font_color='darkblue',
                             label_pos=0.5)

# 4.5 添加图例（用于说明线宽含义）
legend_elements = [
    Line2D([0], [0], marker='*', color='w', markerfacecolor='orange',
           markersize=15, label='源点 c₁ (星形)'),
    Line2D([0], [0], linewidth=5, color='gray', label='低票价 (10 元)'),
    Line2D([0], [0], linewidth=2.5, color='gray', label='中等票价 (~50 元)'),
    Line2D([0], [0], linewidth=1, color='gray', label='高票价 (100 元)')
]
plt.legend(handles=legend_elements, loc='upper right', framealpha=0.9)

plt.title('城市航运网络拓扑与直达票价', fontsize=14, fontweight='bold')
plt.axis('off')
plt.tight_layout()

# 输出矢量图（PDF 或 SVG）
plt.savefig('network_topology.pdf', format='pdf', bbox_inches='tight')
# plt.savefig('network_topology.svg', format='svg', bbox_inches='tight')
plt.show()