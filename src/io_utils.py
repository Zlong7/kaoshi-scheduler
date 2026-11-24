"""读写图数据。graph.txt 格式：第一行 n m，接下来 m 行 u v（0-indexed）。"""


def read_graph(path):
    """读取图文件，返回 (n, edges)。edges 为 [(u, v), ...]。"""
    with open(path, encoding="utf-8") as f:
        tokens = f.read().split()
    if not tokens:
        raise ValueError(f"空文件: {path}")
    it = iter(tokens)
    n = int(next(it))
    m = int(next(it))
    edges = []
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        edges.append((u, v))
    return n, edges


def build_adj_matrix(n, edges):
    """由边列表构建邻接矩阵 G，G[i][j]=1 表示 i 与 j 冲突。"""
    G = [[0] * n for _ in range(n)]
    for u, v in edges:
        G[u][v] = 1
        G[v][u] = 1
    return G