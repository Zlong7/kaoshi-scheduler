"""回溯法（深度优先 + 剪枝）求解图着色问题"""


def color_backtrack(G):
    """寻找图 G 的最少着色数。
    G 为邻接矩阵。
    返回: (最少时间段数 K, 具体排考方案 coloring, 搜索节点数 stats)
    """
    n = len(G)

    # 优化：按顶点度降序排序（Welsh-Powell 思想，优先安排冲突最多的课）
    order = sorted(range(n), key=lambda i: -sum(G[i]))

    def can_assign(v, c, color):
        """检查给课程 v 分配时间段 c 是否合法"""
        for u in range(n):
            if G[v][u] and color[u] == c:
                return False
        return True

    # 尝试用 K 个时间段去排
    for K in range(1, n + 1):
        color = [-1] * n
        nodes_visited = 0  # 统计搜索节点数，用于后续实验对比

        def dfs(pos):
            nonlocal nodes_visited
            nodes_visited += 1

            if pos == n:
                return True  # 所有课程都安排完毕

            v = order[pos]
            # 对称性打破：第 pos 个节点最多只能用到前面用过的颜色 + 1 种
            # 但不影响最坏情况，简单起见这里就尝试 0 到 K-1
            for c in range(K):
                if can_assign(v, c, color):
                    color[v] = c
                    if dfs(pos + 1):
                        return True
                    color[v] = -1  # 回溯：撤销当前安排

            return False

        if dfs(0):
            return K, color, nodes_visited

    return n, list(range(n)), 0