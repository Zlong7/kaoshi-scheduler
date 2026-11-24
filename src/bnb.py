import heapq
from src.greedy import color_greedy


def color_bnb(G):
    n = len(G)
    # 贪心求初始上界 (原顺序)
    bestK, greedy_sol = color_greedy(G)
    bnb_sol = None

    order = sorted(range(n), key=lambda i: -sum(G[i]))
    G_ordered = [[G[order[i]][order[j]] for j in range(n)] for i in range(n)]

    push_count = 1
    pop_count = 0
    prune_count = 0

    # 初始状态，一个颜色都没用，used = 0
    heap = [(0, 0, [])]

    while heap:
        used, idx, coloring = heapq.heappop(heap)
        pop_count += 1

        if used >= bestK:
            prune_count += 1
            continue

        if idx == n:
            bestK = used
            bnb_sol = coloring  # 记录的是 order 顺序的解
            continue

        for c in range(min(used + 1, bestK)):
            conflict = False
            for u in range(idx):
                if G_ordered[idx][u] and coloring[u] == c:
                    conflict = True
                    break

            if not conflict:
                new_used = max(used, c + 1)
                if new_used < bestK:
                    heapq.heappush(heap, (new_used, idx + 1, coloring + [c]))
                    push_count += 1
                else:
                    prune_count += 1

    # 【修复点】根据是否有 BnB 解来决定映射
    if bnb_sol is not None:
        # 如果 BnB 找到了更优解（或同优解），需要把 order 映射回原数组
        final_sol = [-1] * n
        for i, c in enumerate(bnb_sol):
            final_sol[order[i]] = c
    else:
        # 如果 BnB 没找到，直接用贪心解
        final_sol = greedy_sol

    return bestK, final_sol, pop_count, push_count, prune_count