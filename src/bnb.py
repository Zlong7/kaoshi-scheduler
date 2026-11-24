import heapq
import time
from src.greedy import color_greedy


def color_bnb(G, time_limit=30):
    n = len(G)
    bestK, greedy_sol = color_greedy(G)
    bnb_sol = None

    order = sorted(range(n), key=lambda i: -sum(G[i]))
    G_ordered = [[G[order[i]][order[j]] for j in range(n)] for i in range(n)]

    push_count = 1
    pop_count = 0
    prune_count = 0

    heap = [(0, 0, [])]
    start_time = time.time()

    while heap:
        # 【内置超时检查】每次出堆检查一下时间
        if time.time() - start_time > time_limit:
            raise TimeoutError("分支限界搜索超时")

        used, idx, coloring = heapq.heappop(heap)
        pop_count += 1

        if used >= bestK:
            prune_count += 1
            continue

        if idx == n:
            bestK = used
            bnb_sol = coloring
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

    if bnb_sol is not None:
        final_sol = [-1] * n
        for i, c in enumerate(bnb_sol):
            final_sol[order[i]] = c
    else:
        final_sol = greedy_sol

    return bestK, final_sol, pop_count, push_count, prune_count