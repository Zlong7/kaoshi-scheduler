import time


def color_backtrack(G, time_limit=30):
    """增加了 time_limit 参数，内置超时检查"""
    n = len(G)
    order = sorted(range(n), key=lambda i: -sum(G[i]))
    nodes_visited = 0

    def can_assign(v, c, color):
        for u in range(n):
            if G[v][u] and color[u] == c:
                return False
        return True

    start_time = time.time()

    for K in range(1, n + 1):
        color = [-1] * n

        def dfs(pos):
            nonlocal nodes_visited
            # 【内置超时检查】每次递归检查一下时间
            if time.time() - start_time > time_limit:
                raise TimeoutError("回溯搜索超时")

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