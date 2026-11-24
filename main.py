import argparse
import time
from src.io_utils import read_graph, build_adj_matrix
from src.verify import verify_coloring
from src.backtrack import color_backtrack
from src.bnb import color_bnb
from src.greedy import color_greedy

def main():
    parser = argparse.ArgumentParser(description="排考优化求解器")
    parser.add_argument("file", help="图数据文件路径，如 data/toy6.txt")
    parser.add_argument("--algo", choices=["backtrack", "bnb", "greedy", "all"], default="all", help="选择算法")
    args = parser.parse_args()

    n, edges = read_graph(args.file)
    G = build_adj_matrix(n, edges)
    print(f"读取成功: n={n}, 边数={len(edges)}\n")

    if args.algo in ["greedy", "all"]:
        start = time.time()
        K, sol = color_greedy(G)
        print(f"[贪心算法] K={K}, 耗时={time.time()-start:.6f}s, 合法={verify_coloring(n, edges, sol)}")

    if args.algo in ["backtrack", "all"]:
        start = time.time()
        K, sol, nodes = color_backtrack(G)
        print(f"[回溯法] K={K}, 耗时={time.time()-start:.6f}s, 节点={nodes}, 合法={verify_coloring(n, edges, sol)}")
        print(f"  方案: {sol}")

    if args.algo in ["bnb", "all"]:
        start = time.time()
        K, sol, pop, push, prune = color_bnb(G)
        print(f"[分支限界] K={K}, 耗时={time.time()-start:.6f}s, 出堆={pop}, 合法={verify_coloring(n, edges, sol)}")
        print(f"  方案: {sol}")

if __name__ == "__main__":
    main()