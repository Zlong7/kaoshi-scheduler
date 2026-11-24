import time
import random
import csv
import os
import concurrent.futures
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


# 使用多线程/进程包一层超时机制（30秒）
def run_with_timeout(func, *args, timeout=30):
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(func, *args)
        try:
            return future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            return "TIMEOUT"


def main():
    sizes = [6, 10, 20, 40, 80, 120]
    runs_per_size = 5  # 每个规模 5 张图
    results = []

    print(f"{'规模':<5} | {'算法':<10} | {'平均耗时(s)':<12} | {'耗时标准差':<10} | {'平均节点数':<10}")
    print("-" * 65)

    for n in sizes:
        # 生成 5 张固定随机种子的图
        graphs = [generate_random_graph(n, 0.3, seed=i * 100 + n) for i in range(runs_per_size)]

        for method in ['backtrack', 'bnb']:
            times, nodes_list = [], []
            timeouts = 0

            for (edges, G) in graphs:
                if method == 'backtrack':
                    res = run_with_timeout(color_backtrack, G, timeout=30)
                else:
                    res = run_with_timeout(color_bnb, G, timeout=30)

                if res == "TIMEOUT":
                    timeouts += 1
                    times.append(30.0)
                    nodes_list.append(999999)
                else:
                    # res 结构：backtrack->(K, sol, nodes) / bnb->(K, sol, pop, push, prune)
                    K, sol = res[0], res[1]
                    nodes = res[2] if method == 'backtrack' else res[2]
                    assert verify_coloring(n, edges, sol)
                    times.append(res[0] if False else 0)  # 占位，实际耗时在下面测
                    nodes_list.append(nodes)

            # 重新跑一遍正式记录耗时（避免超时机制影响计时）
            real_times = []
            for (edges, G) in graphs:
                start = time.time()
                if method == 'backtrack':
                    res = run_with_timeout(color_backtrack, G, timeout=30)
                else:
                    res = run_with_timeout(color_bnb, G, timeout=30)
                if res != "TIMEOUT":
                    real_times.append(time.time() - start)
                else:
                    real_times.append(30.0)

            import statistics
            avg_t = statistics.mean(real_times) if real_times else 30.0
            std_t = statistics.stdev(real_times) if len(real_times) > 1 else 0.0
            avg_n = statistics.mean(nodes_list)

            note = f"(超时{timeouts}次)" if timeouts > 0 else ""
            print(f"{n:<5} | {method:<10} | {avg_t:<12.4f} | {std_t:<10.4f} | {avg_n:<10.0f} {note}")

            # 保存原始数据
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