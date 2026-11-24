from src.io_utils import read_graph, build_adj_matrix
from src.backtrack import color_backtrack
from src.bnb import color_bnb
from src.verify import verify_coloring


def run_test(filename, expected_K, desc):
    n, edges = read_graph(filename)
    G = build_adj_matrix(n, edges)

    # 跑回溯
    K1, sol1, _ = color_backtrack(G)
    v1 = verify_coloring(n, edges, sol1)

    # 跑分支限界
    K2, sol2, _, _, _ = color_bnb(G)
    v2 = verify_coloring(n, edges, sol2)

    print(f"[{desc}]")
    print(f"  回溯法: K={K1} (预期{expected_K}), 合法={v1}")
    print(f"  分支限界: K={K2} (预期{expected_K}), 合法={v2}")
    print("-" * 40)


def test_invalid():
    n, edges = read_graph("data/toy6.txt")
    bad_sol = [0, 0, 0, 0, 0, 0]  # 全部安排在同一段，绝对非法
    is_valid = verify_coloring(n, edges, bad_sol)
    print(f"[非法方案校验] 预期 False, 实际 {is_valid} -> {'✅ 通过' if not is_valid else '❌ 失败'}")


if __name__ == "__main__":
    print("开始边界用例测试...\n")
    # 你需要自己在 data 下建一个 isolated.txt，内容为： 3 1 \n 0 1
    run_test("data/toy6.txt", 3, "题目Toy6")
    run_test("data/empty.txt", 1, "空图 (无冲突)")
    run_test("data/complete5.txt", 5, "完全图 K5")
    run_test("data/bipartite.txt", 2, "二部图")
    # 如果你没建 isolated.txt，就把下面这行注释掉
    # run_test("data/isolated.txt", 2, "含孤立顶点图")
    test_invalid()