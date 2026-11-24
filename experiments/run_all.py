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

    print(f"{'规模':<5} | {'算法':<10} | {'平均耗时(s)':<12} | {'耗时标准差':<10} | {'平均节点数':<10}")
    print("-" * 65)

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
                        K, sol, _, _, _ = color_bnb(G, time_limit=30)
                    real_times.append(time.time() - start)
                    nodes_list.append(nodes)
                    assert verify_coloring(n, edges, sol)
                except TimeoutError:
                    timeouts += 1
                    real_times.append(30.0)
                    nodes_list.append(999999)

            avg_t = statistics.mean(real_times)
            std_t = statistics.stdev(real_times) if len(real_times) > 1 else 0.0
            avg_n = statistics.mean(nodes_list)

            note = f"(超时{timeouts}次)" if timeouts > 0 else ""
            print(f"{n:<5} | {method:<10} | {avg_t:<12.4f} | {std_t:<10.4f} | {avg_n:<10.0f} {note}")

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