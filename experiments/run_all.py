import time
import random
import csv
import os

from src.backtrack import color_backtrack
from src.bnb import color_bnb
from src.verify import verify_coloring


def generate_random_graph(n, edge_prob=0.3):
    """随机生成一个有 n 个节点的图"""
    edges = []
    G = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < edge_prob:
                edges.append((i, j))
                G[i][j] = 1
                G[j][i] = 1
    return edges, G


def main():
    # 把规模改小一点，防止 Python 跑太久卡死
    sizes = [10, 15, 20, 25, 30]
    results = []

    print(f"{'规模(n)':<8} | {'算法':<10} | {'K值':<5} | {'耗时(秒)':<10} | {'搜索节点数':<10}")
    print("-" * 60)

    # 固定随机种子，保证每次运行结果一致
    random.seed(42)

    for n in sizes:
        # 【修复点】：先生成图，再让两个算法都跑这同一张图
        edges, G = generate_random_graph(n, edge_prob=0.3)

        for method in ['backtrack', 'bnb']:
            total_time = 0
            total_nodes = 0
            K_val = 0

            # 每个算法在同一张图上跑 1 次即可（跑3次耗时太长）
            start = time.time()

            if method == 'backtrack':
                K_val, sol, nodes = color_backtrack(G)
            else:
                K_val, sol, nodes = color_bnb(G)

            total_time = time.time() - start
            total_nodes = nodes

            # 断言保证结果合法
            assert verify_coloring(n, edges, sol), "出错了！算法生成了不合法方案"

            print(f"{n:<8} | {method:<10} | {K_val:<5} | {total_time:<10.4f} | {total_nodes:<10}")
            results.append([n, method, K_val, round(total_time, 4), total_nodes])

    # 保存为 CSV 文件
    os.makedirs("report", exist_ok=True)
    with open("report/results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Size(n)", "Method", "K", "Time(s)", "Nodes"])
        writer.writerows(results)

    print("\n实验数据已保存到 report/results.csv")


if __name__ == "__main__":
    main()