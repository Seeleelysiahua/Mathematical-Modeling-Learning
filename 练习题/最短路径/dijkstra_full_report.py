"""
Dijkstra单源最短路径算法 - 完整执行报告生成器
基于《城市航运路线最低票价规划方案》规范文档
"""

import sys

# ∞ 使用一个足够大的整数表示（取足够大避免溢出）
INF = 10**12


def dijkstra_full_report():
    """执行Dijkstra算法并生成完整的迭代过程报告"""

    # ========================================
    # 第一节：初始化
    # ========================================

    # 节点标签（1-based，与文档一致）
    nodes = [1, 2, 3, 4, 5, 6]
    n = len(nodes)

    # 邻接矩阵 (1-indexed，方便理解)
    # 对应文档中的直达票价邻接矩阵
    C = [
        [0, 0, 0, 0, 0, 0, 0],  # 占位，不用0行
        [0, 0, 50, INF, 40, 25, 10],    # c₁
        [0, 50, 0, 15, 20, INF, 25],    # c₂
        [0, INF, 15, 0, 10, 20, INF],   # c₃
        [0, 40, 20, 10, 0, 100, 25],    # c₄
        [0, 25, INF, 20, 100, 0, 55],   # c₅
        [0, 10, 25, INF, 25, 55, 0]     # c₆
    ]

    # 初始化距离数组和前驱节点数组
    dist = [INF] * (n + 1)
    prev = [0] * (n + 1)

    # 永久集合 S 和临时集合 T
    S = set()
    T = set(nodes)

    # ========================================
    # 初始化：从源点 c₁ 的直接邻居初始化距离
    # ========================================
    dist[1] = 0  # 源点到自身距离为0
    prev[1] = 0  # 源点无前驱

    # 遍历所有节点，初始化从 c₁ 出发的直接距离
    for v in range(2, n + 1):
        if C[1][v] < INF:
            dist[v] = C[1][v]
            prev[v] = 1  # 前驱为源点 c₁

    # 源点 c₁ 加入永久集合，从临时集合移除
    S.add(1)
    T.remove(1)

    # Unicode下标映射
    subscripts = {0: '₀', 1: '₁', 2: '₂', 3: '₃', 4: '₄', 5: '₅', 6: '₆', 7: '₇', 8: '₈', 9: '₉'}

    def cn(n: int) -> str:
        """将数字转换为带下标的c格式，如 1 -> c₁"""
        return f"c{subscripts.get(n, str(n))}"

    def safe_add(a: int, b: int) -> int:
        """安全加法，处理∞相加的情况"""
        if a >= INF or b >= INF:
            return INF
        return a + b

    def format_dist(d: int, is_permanent: bool) -> str:
        """格式化距离值"""
        if d >= INF:
            return "  ∞   "
        elif is_permanent:
            # 已确定的最短距离，添加 ✓ 标记
            if d < 10:
                return f"  ✓0{d}  "
            elif d < 100:
                return f"  ✓{d}  "
            else:
                return f" ✓{d}  "
        else:
            # 临时距离
            if d < 10:
                return f"   0{d}  "
            elif d < 100:
                return f"   {d}  "
            else:
                return f"  {d}  "

    def state_str() -> str:
        """返回当前 dist/prev/状态 的表格字符串"""
        lines = []
        lines.append("  ┌─────────┬────────┬────────┬────────┬────────┬────────┬────────┐")
        lines.append("  │  节点   │  c₁    │  c₂    │  c₃    │  c₄    │  c₅    │  c₆    │")
        lines.append("  ├─────────┼────────┼────────┼────────┼────────┼────────┼────────┤")

        # dist 行
        dist_vals = [format_dist(dist[i], i in S) for i in range(1, 7)]
        lines.append("  │  dist   │" + "│".join(dist_vals) + "│")

        # prev 行
        prev_vals = []
        for i in range(1, 7):
            p = prev[i]
            if p == 0:
                prev_vals.append("  -   ")
            else:
                prev_vals.append(f" {cn(p)}   ")
        lines.append("  │  prev   │" + "│".join(prev_vals) + "│")

        # 状态行
        state_vals = ["  S   " if i in S else "  T   " for i in range(1, 7)]
        lines.append("  │  状态   │" + "│".join(state_vals) + "│")

        lines.append("  └─────────┴────────┴────────┴────────┴────────┴────────┴────────┘")
        return "\n".join(lines)

    def adjacency_str() -> str:
        """返回邻接矩阵的字符串表示"""
        lines = []
        lines.append("           c₁      c₂      c₃      c₄      c₅      c₆")
        lines.append("         ┌──────┬──────┬──────┬──────┬──────┬──────┐")
        for i in range(1, 7):
            row_vals = []
            for j in range(1, 7):
                if C[i][j] >= INF:
                    row_vals.append("    ∞")
                else:
                    row_vals.append(f"{C[i][j]:>5}")
            lines.append(f"     {cn(i)} │ {'│'.join(row_vals)} │")
        lines.append("         └──────┴──────┴──────┴──────┴──────┴──────┘")
        return "\n".join(lines)

    def get_path(target: int) -> list:
        """根据前驱节点数组回溯路径"""
        path = []
        cur = target
        while cur != 0:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        return path

    def draw_network(path: list = None) -> str:
        """生成简化的网络图ASCII art

        原始网络:
            c₁ ───(50)─── c₂
            │  ╲          │
           (10) (25)    (15)
            │     ╲      │
            ↓      ╲    (10)
            c₆ ───────── c₄ ───(100)─── c₅
            │       ╲              ╱
           (25)     ╲ (20)      (55)
            │        ╲  ╱       ╱
            └──────── c₃
        """
        if path is None:
            path = []

        path_set = set(path)
        lines = []

        # 绘制上部分
        lines.append("        c₁ ───(50)─── c₂")
        lines.append("        │  ╲          │")
        lines.append("       (10) (25)    (15)")
        lines.append("        │     ╲      │")

        # 根据路径标记中间行
        if {1, 6, 4}.issubset(path_set):
            lines.append("        ↓      ╲    (10)")
            lines.append("        c₆ ───────── c₄ ───(100)─── c₅")
        elif {1, 5}.issubset(path_set):
            lines.append("       (10) (25)    (10)")
            lines.append("        │     ╲      │")
            lines.append("        ↓      ╲    ↓")
            lines.append("        c₆ ───────── c₄ ───(100)─── c₅")
        else:
            lines.append("        ↓      ╲    ↓")
            lines.append("        c₆ ───────── c₄ ───(100)─── c₅")

        lines.append("        │       ╲              ╱")
        lines.append("       (25)     ╲ (20)      (55)")
        lines.append("        │        ╲  ╱       ╱")
        lines.append("        └──────── c₃        /")

        # 添加路径标记
        if path:
            path_str = " → ".join([f"c{x}" for x in path])
            lines.append("")
            lines.append(f"  ※ 标记路线：{path_str}")

        return "\n".join(lines)

    # ========================================
    # 第二节：输出初始化状态
    # ========================================

    print("═" * 70)
    print("算法初始化（第0轮 / 初始状态）")
    print("═" * 70)
    print()

    print("【永久集合 S】")
    print("  S = { c₁ }    ← 源点直接加入")
    print()
    print("【临时集合 T】")
    print("  T = { c₂, c₃, c₄, c₅, c₆ }")
    print()
    print("【初始距离数组】")
    for i in range(1, 7):
        if i == 1:
            val = "0"
        elif dist[i] >= INF:
            val = "∞"
        else:
            val = str(dist[i])
        print(f"  dist[{i}] = {val}")
    print()
    print("【前驱节点数组】")
    for i in range(1, 7):
        if i == 1:
            print(f"  prev[{i}] = NULL   ← 源点无前驱")
        elif prev[i] != 0:
            print(f"  prev[{i}] = c{prev[i]}   ← 直接前驱为源点")
        else:
            print(f"  prev[{i}] = NULL")
    print()
    print("【邻接矩阵】")
    print(adjacency_str())
    print()
    print(state_str())

    # ========================================
    # 第三节：迭代过程
    # ========================================

    round_num = 1
    while T:
        # 从 T 中选出 dist 最小的节点（若相等选编号小的）
        min_dist = INF
        u = -1
        for v in sorted(T):
            if dist[v] < min_dist:
                min_dist = dist[v]
                u = v

        print()
        print("═" * 70)
        print(f"第 {round_num} 轮迭代")
        print("═" * 70)
        print()

        print("【永久集合 S】")
        S_list = sorted(S)
        S_str = ", ".join([cn(x) for x in S_list])
        print(f"  S = {{ {S_str} }}")
        print()

        print("【当前临时集合 T】")
        T_list = sorted(T)
        T_str = ", ".join([cn(x) for x in T_list])
        print(f"  T = {{ {T_str} }}")
        print()

        print("【从 T 中选择 dist 最小的节点】")
        for x in T_list:
            d_str = "∞" if dist[x] >= INF else str(dist[x])
            print(f"  dist[{x}] = {d_str}")
        print(f"  最小值：dist[{u}] = {dist[u]}")
        print()

        print(f"【本轮选定节点】★ {cn(u)} ★")
        print(f"  选定距离：{dist[u]}")
        print()

        # 更新集合
        S_old = S.copy()
        S.add(u)
        T.remove(u)

        print("【更新永久集合】")
        S_old_list = sorted(S_old)
        S_new_list = sorted(S)
        old_str = ", ".join([cn(x) for x in S_old_list])
        new_str = ", ".join([cn(x) for x in S_new_list])
        print(f"  S_old = {{ {old_str} }}")
        print(f"  S_new = {{ {new_str} }}")
        print()

        # 松弛更新
        print("【距离更新判定】")
        print(f"  检查 {cn(u)} 的邻居节点（在 T 中的）：")
        print()

        # 构建更新表格
        print("  ┌────────┬─────────────┬──────────────┬─────────────┬─────────┐")
        print(f"  │ 节点   │ 原dist[c_j] │ C[{u}][j]+{dist[u]:<8} │ 新dist[c_j] │ 是否更新 │")
        print("  ├────────┼─────────────┼──────────────┼─────────────┼─────────┤")

        has_neighbor = False
        for v in T_list:  # T_list 是更新前的T
            if C[u][v] < INF:  # 是邻居
                has_neighbor = True
                old_val = "∞" if dist[v] >= INF else str(dist[v])
                edge_val = "∞" if C[u][v] >= INF else str(C[u][v])

                # 安全加法
                new_dist = safe_add(dist[u], C[u][v])
                new_val = "∞" if new_dist >= INF else str(new_dist)

                updated = (new_dist < dist[v])
                update_flag = "✓更新" if updated else "✗不更新"

                print(f"  │  {cn(v)}    │    {old_val:<8} │ {edge_val}+{dist[u]:<8} │    {new_val:<9} │  {update_flag}   │")

                if updated:
                    dist[v] = new_dist
                    prev[v] = u

        if not has_neighbor:
            print("  │ (无邻居节点在T中，无需更新)                                      │")

        print("  └────────┴─────────────┴──────────────┴─────────────┴─────────┘")
        print()

        print("【更新后的状态】")
        print()
        print(state_str())

        print()
        print("【永久集合 S】")
        S_str = ", ".join([cn(x) for x in sorted(S)])
        print(f"  S = {{ {S_str} }}")

        print()
        T_str = ", ".join([cn(x) for x in sorted(T)]) if T else "(空)"
        print("【临时集合 T】")
        print(f"  T = {{ {T_str} }}")

        round_num += 1

    # ========================================
    # 第四节：算法结束
    # ========================================

    print()
    print("═" * 70)
    print("                    算法执行完毕")
    print("═" * 70)
    print()

    # ========================================
    # 第五节：最终结果汇总
    # ========================================

    print("【最短距离结果】")
    print("┌─────────────┬────────────────┐")
    print("│  目标城市   │  从c₁出发的最低票价  │")
    print("├─────────────┼────────────────┤")
    for i in range(2, 7):
        if dist[i] >= INF:
            print(f"│    c{i}       │     不可达    │")
        else:
            print(f"│    c{i}       │      {dist[i]} 元     │")
    print("└─────────────┴────────────────┘")
    print()

    # ========================================
    # 第六节：路径回溯与详情
    # ========================================

    print("【路径回溯结果】")
    print("基于前驱节点数组 prev[] 进行路径回溯：")
    print()

    # 输出每个目标的路线详情
    for target in range(2, 7):
        path = get_path(target)

        print("╔" + "═" * 66 + "╗")
        print(f"║                    目标城市：{cn(target)}                               ║")
        print("╚" + "═" * 66 + "╝")
        print()

        print("【最低总票价】")
        if dist[target] >= INF:
            print(f"  从 c₁ 到 {cn(target)} 不可达")
        else:
            print(f"  从 c₁ 到 {cn(target)} 的最低票价为：{dist[target]} 元")
        print()

        path_str = " → ".join([cn(x) for x in path])
        print("【完整中转途经节点序列】")
        print(f"  路线：{path_str}")
        print(f"  共经过 {len(path) - 1} 个航段")
        print()

        print("【分段票价累加明细】")
        print("  ┌────────┬────────┬────────┬────────┐")
        print("  │  航段  │  起点  │  终点  │  票价  │")
        print("  ├────────┼────────┼────────┼────────┤")

        if dist[target] >= INF:
            print("  │ (无可用路径)                                    │")
        else:
            total = 0
            for k in range(len(path) - 1):
                start = path[k]
                end = path[k + 1]
                cost = C[start][end]
                total += cost
                print(f"  │  第{k + 1}段 │ {cn(start)}    │ {cn(end)}    │   {cost:<4} │")
            print("  ├────────┼────────┼────────┼────────┤")
            print(f"  │  合计  │        │        │   {total:<4} │")
        print("  └────────┴────────┴────────┴────────┘")
        print()

        # 路线可视化
        print("【路线可视化文字绘制】")
        if dist[target] >= INF:
            print("  (无可用路线)")
        else:
            print(draw_network(path))
        print()

        # 验证
        if dist[target] < INF and len(path) > 1:
            expr = " + ".join([f"C[{path[i]}][{path[i + 1]}]" for i in range(len(path) - 1)])
            vals = " + ".join([str(C[path[i]][path[i + 1]]) for i in range(len(path) - 1)])
            total_check = sum(C[path[i]][path[i + 1]] for i in range(len(path) - 1))
            print("【验证】")
            print(f"  {expr} = {vals} = {total_check} ✓")
        print()

    # ========================================
    # 第七节：完整路线图汇总
    # ========================================

    print("═" * 70)
    print("                          城市航运网络完整路线图")
    print("═" * 70)
    print()

    print("""                           c₁ ───(50)─── c₂
                           │  ╲          │
                          (10) (25)    (15)
                           │     ╲      │
                           │      ╲    (10)
                           ↓       ╲   /
                           c₆ ───(25)─── c₄ ───(100)─── c₅
                                   ╲              ╱
                                    ╲          (55)
                                     ╲        ╱
                                          c₃""")
    print()

    print("═" * 70)
    print("                              最短路线汇总")
    print("═" * 70)
    print()

    print("┌─────────────┬──────────────────┬───────────────────────────┬────────────┐")
    print("│  目标城市   │    最低票价      │      最优路线             │   核验值   │")
    print("├─────────────┼──────────────────┼───────────────────────────┼────────────┤")
    for target in range(2, 7):
        path = get_path(target)
        if dist[target] < INF:
            path_str = " → ".join([cn(x) for x in path])
            vals = " + ".join([str(C[path[i]][path[i + 1]]) for i in range(len(path) - 1)])
            total_check = sum(C[path[i]][path[i + 1]] for i in range(len(path) - 1))
            print(f"│   {cn(target)}       │      {dist[target]:>2} 元       │  {path_str:<25} │ {vals:<10} = {total_check} ✓ │")
        else:
            print(f"│   {cn(target)}       │      不可达      │                           │            │")
    print("└─────────────┴──────────────────┴───────────────────────────┴────────────┘")
    print()

    print("═" * 70)
    print("★ c₆ 是关键中转枢纽：4条最优路线中3条经过c₆")
    print("═" * 70)


# ========================================
# 入口点
# ========================================

if __name__ == "__main__":
    dijkstra_full_report()
