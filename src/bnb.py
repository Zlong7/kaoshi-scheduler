"""分支限界法（广度优先 + 界限剪枝）求解图着色问题"""
import heapq


def color_bnb(G):
    """寻找图 G 的最少着色数。
    返回: (最少时间段数 bestK, 具体排考方案 bestSol, 搜索节点数 nodes_visited)
    """
    n = len(G)
    bestK = n + 1
    bestSol = None
    nodes_visited = 0

    # 启发式：按度降序排序，保证先处理冲突大的
    order = sorted(range(n), key=lambda i: -sum(G[i]))

    # 重新映射一下图，让原本的 order 变成 0,1,2...
    G_ordered = [[G[order[i]][order[j]] for j in range(n)] for i in range(n)]

    # 优先队列 (used, idx, coloring)
    # used: 已使用的时间段数； idx: 已经排好的课程数； coloring: 当前方案
    heap = [(0, 0, [])]

    while heap:
        used, idx, coloring = heapq.heappop(heap)
        nodes_visited += 1

        # 界限剪枝：如果已用的时间段数已经大于等于当前最优解，不可能更优了
        if used >= bestK:
            continue

        if idx == n:
            bestK = used
            bestSol = coloring
            continue

        # 对称性打破：只尝试已用时间段 + 1个新时间段
        # 即如果当前用了 2 个段(0,1)，下一个课最多只能选 0, 1, 2
        for c in range(min(used + 1, bestK)):
            # 冲突检测
            conflict = False
            for u in range(idx):
                if G_ordered[idx][u] and coloring[u] == c:
                    conflict = True
                    break

            if not conflict:
                new_used = max(used, c + 1)
                heapq.heappush(heap, (new_used, idx + 1, coloring + [c]))

    # 由于排序过，返回前要把颜色映射回原本的课程编号
    final_sol = [-1] * n
    if bestSol:
        for i, c in enumerate(bestSol):
            final_sol[order[i]] = c

    return bestK, final_sol, nodes_visited