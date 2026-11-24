"""Welsh-Powell 贪心着色算法，用于求上界"""


def color_greedy(G):
    n = len(G)
    # 按度数降序排列
    order = sorted(range(n), key=lambda i: -sum(G[i]))
    color = [-1] * n
    max_color = -1

    for v in order:
        # 找到邻居中已经用过的最小未占用颜色
        used_colors = {color[u] for u in range(n) if G[v][u] and color[u] != -1}
        c = 0
        while c in used_colors:
            c += 1
        color[v] = c
        max_color = max(max_color, c)

    return max_color + 1, color