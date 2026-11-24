import time
from src.io_utils import read_graph, build_adj_matrix
from src.verify import verify_coloring, used_colors
from src.backtrack import color_backtrack
from src.bnb import color_bnb

# 1. 准备数据
n, edges = read_graph("data/toy6.txt")
G = build_adj_matrix(n, edges)

# 2. 运行回溯法
start = time.time()
bt_K, bt_sol, bt_nodes = color_backtrack(G)
bt_time = time.time() - start

# 3. 运行分支限界法
start = time.time()
bnb_K, bnb_sol, bnb_nodes = color_bnb(G)
bnb_time = time.time() - start

# 4. 打印对比结果
print("====== 算法运行结果对比 ======")
print(f"【回溯法】 K = {bt_K}, 耗时 = {bt_time:.4f}s, 搜索节点 = {bt_nodes}")
print(f"   排考方案: {bt_sol}")
print(f"   合法性校验: {verify_coloring(n, edges, bt_sol)}")
print("-" * 30)
print(f"【分支限界】K = {bnb_K}, 耗时 = {bnb_time:.4f}s, 搜索节点 = {bnb_nodes}")
print(f"   排考方案: {bnb_sol}")
print(f"   合法性校验: {verify_coloring(n, edges, bnb_sol)}")