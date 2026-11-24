import time
import random
import csv
import os
import statistics
from src.backtrack import color_backtrack
from src.bnb import color_bnb
from src.verify import verify_coloring


def generate_random_graph(n, edge_prob=0.3, seed=None):
    if seed is not None: random.seed(seed)
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
    sizes = [6, 10, 20, 40, 80, 120]
    runs_per_size = 5
    results = []

    print(f"{'规模':<5} | {'算法':<10} | {'平均耗时(s)':<12} | {'成功次数':<8} | {'成功样本平均节点数':<15}")
    print("-" * 70)

    for n in sizes:
        graphs = [generate_random_graph(n, 0.3, seed=i * 100 + n) for i in range(runs_per_size)]

        for method in ['backtrack', 'bnb']:
            real_times, nodes_list = [], []
            timeouts = 0

            for (edges, G) in graphs:
                start = time.time()
                try:
                    if method == 'backtrack':
                        K, sol, nodes = color_backtrack(G, time_limit=30)
                    else:
                        # 【修复】正确接收 BnB 返回的出堆次数
                        K, sol, nodes, _, _ = color_bnb(G, time_limit=30)

                    real_times.append(time.time() - start)
                    nodes_list.append(nodes)
                    assert verify_coloring(n, edges, sol)
                except TimeoutError:
                    timeouts += 1
                    real_times.append(30.0)
                    nodes_list.append(-1)  # 【修复】超时用 -1 占位，不参与平均

            avg_t = statistics.mean(real_times)

            # 【修复】只计算成功跑完的样本的节点数平均
            valid_nodes = [x for x in nodes_list if x != -1]
            avg_n = statistics.mean(valid_nodes) if valid_nodes else -1

            success_count = runs_per_size - timeouts
            note = f"(超时{timeouts}次)" if timeouts > 0 else ""

            avg_n_str = f"{avg_n:.0f}" if avg_n != -1 else "N/A"
            print(
                f"{n:<5} | {method:<10} | {avg_t:<12.4f} | {success_count}/{runs_per_size:<5} | {avg_n_str:<15} {note}")

            # 记录原始数据，超时的节点记为 -1
            for i, t in enumerate(real_times):
                results.append([n, method, i, round(t, 6), nodes_list[i]])

    os.makedirs("report", exist_ok=True)
    with open("report/results_raw.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Size", "Method", "Run_ID", "Time(s)", "Nodes"])
        writer.writerows(results)
    print("\n原始实验数据已保存到 report/results_raw.csv")


if __name__ == "__main__":
    main()