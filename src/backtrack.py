def color_backtrack(G):
    n = len(G)
    order = sorted(range(n), key=lambda i: -sum(G[i]))
    nodes_visited = 0  # 【修改点】移到最外层，累计所有 K 的尝试
    
    def can_assign(v, c, color):
        for u in range(n):
            if G[v][u] and color[u] == c:
                return False
        return True

    for K in range(1, n + 1):
        color = [-1] * n
        def dfs(pos):
            nonlocal nodes_visited
            nodes_visited += 1
            if pos == n: return True
            v = order[pos]
            for c in range(K):
                if can_assign(v, c, color):
                    color[v] = c
                    if dfs(pos + 1): return True
                    color[v] = -1
            return False

        if dfs(0):
            return K, color, nodes_visited
    return n, list(range(n)), nodes_visited