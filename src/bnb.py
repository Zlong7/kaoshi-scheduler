import heapq
from src.greedy import color_greedy # 【修改点】引入贪心

def color_bnb(G):
    n = len(G)
    # 【修改点】使用贪心算法初始化上界，大幅剪枝
    bestK, bestSol_init = color_greedy(G)
    bestSol = bestSol_init
    
    order = sorted(range(n), key=lambda i: -sum(G[i]))
    G_ordered = [[G[order[i]][order[j]] for j in range(n)] for i in range(n)]
    
    # 统计变量
    push_count = 1  # 初始状态入堆
    pop_count = 0   # 出堆扩展次数
    prune_count = 0 # 剪枝次数
    
    heap = [(bestK, 0, [])]  # 初始的 used 设为贪心求得的 bestK
    
    while heap:
        used, idx, coloring = heapq.heappop(heap)
        pop_count += 1
        
        if used >= bestK:
            prune_count += 1
            continue
            
        if idx == n:
            bestK = used
            bestSol = coloring
            continue

        for c in range(min(used + 1, bestK)):
            conflict = False
            for u in range(idx):
                if G_ordered[idx][u] and coloring[u] == c:
                    conflict = True
                    break
            
            if not conflict:
                new_used = max(used, c + 1)
                if new_used < bestK: # 只有可能更优才入堆
                    heapq.heappush(heap, (new_used, idx + 1, coloring + [c]))
                    push_count += 1
                else:
                    prune_count += 1

    final_sol = [-1] * n
    if bestSol:
        for i, c in enumerate(bestSol):
            final_sol[order[i]] = c
            
    # 返回：K, 方案, 出堆数(等价于搜索节点), 入堆数, 剪枝数
    return bestK, final_sol, pop_count, push_count, prune_count