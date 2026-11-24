from src.io_utils import read_graph
from src.verify import verify_coloring, used_colors

# 读取数据
n, edges = read_graph("data/toy6.txt")
print("课程数量 n =", n)
print("冲突边 edges =", edges)

# 题目里的图，用 3 个时间段可以合法排考：
# 比如 0->段1, 1->段2, 2->段3, 3->段1, 4->段2, 5->段3
# 在代码里 0-indexed 就是：0, 1, 2, 0, 1, 2
ans = [0, 1, 2, 0, 1, 2]
print("这个方案合法吗？", verify_coloring(n, edges, ans))
print("一共用了几个时间段？", used_colors(ans))

# 故意写个错的：第 0 门和第 1 门课安排在同一个时间段（都是 0）
bad = [0, 0, 2, 1, 2, 1]
print("错误方案合法吗？", verify_coloring(n, edges, bad))