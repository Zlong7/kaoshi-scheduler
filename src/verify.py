"""排考方案合法性校验。所有算法输出都必须过这里。"""


def verify_coloring(n, edges, coloring):
    """检查 coloring 是否为合法 K 着色。

    coloring: list[int]，长度 n，每个元素是该课的时间段编号（0-indexed），-1 表示未分配。
    返回 True 当且仅当：长度正确、无未分配、每条边两端颜色不同。
    """
    if coloring is None or len(coloring) != n:
        return False
    if any(c is None or c < 0 for c in coloring):
        return False
    for u, v in edges:
        if coloring[u] == coloring[v]:
            return False
    return True


def used_colors(coloring):
    """实际使用的时间段数（= 最大编号 + 1）。空方案返回 0。"""
    return max(coloring) + 1 if coloring else 0