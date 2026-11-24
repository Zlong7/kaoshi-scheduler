import csv
import statistics
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 汇总数据
data = {} # data[n][method] = {'times': [], 'nodes': []}

with open("report/results_raw.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        n, method = int(row["Size"]), row["Method"]
        if n not in data: data[n] = {'backtrack': {'times': [], 'nodes': []}, 'bnb': {'times': [], 'nodes': []}}
        data[n][method]['times'].append(float(row["Time(s)"]))
        data[n][method]['nodes'].append(int(row["Nodes"]))

sizes = sorted(data.keys())
bt_t = [statistics.mean(data[n]['backtrack']['times']) for n in sizes]
bt_t_err = [statistics.stdev(data[n]['backtrack']['times']) if len(data[n]['backtrack']['times'])>1 else 0 for n in sizes]
bnb_t = [statistics.mean(data[n]['bnb']['times']) for n in sizes]
bnb_t_err = [statistics.stdev(data[n]['bnb']['times']) if len(data[n]['bnb']['times'])>1 else 0 for n in sizes]

# 1. 耗时对比图
plt.figure(figsize=(10, 5))
plt.errorbar(sizes, bt_t, yerr=bt_t_err, marker='o', label='回溯法', capsize=5)
plt.errorbar(sizes, bnb_t, yerr=bnb_t_err, marker='s', label='分支限界', capsize=5)
plt.yscale('log') # 【精修】对数坐标
plt.xticks(sizes) # 强制刻度为实际规模
plt.title("算法耗时对比 (对数坐标, 每规模5个随机图, p=0.3, 30s超时)")
plt.xlabel("课程数量 (n)")
plt.ylabel("平均耗时 (秒) - 对数轴")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6, which='both')
plt.savefig("report/time_compare.png", dpi=300)
plt.show()

# 2. 节点数对比图
bt_n = [statistics.mean(data[n]['backtrack']['nodes']) for n in sizes]
bnb_n = [statistics.mean(data[n]['bnb']['nodes']) for n in sizes]
plt.figure(figsize=(10, 5))
plt.plot(sizes, bt_n, marker='o', label='回溯法')
plt.plot(sizes, bnb_n, marker='s', label='分支限界')
plt.yscale('log') # 【精修】对数坐标
plt.xticks(sizes)
plt.title("搜索节点数对比 (对数坐标, 每规模5个随机图, p=0.3)")
plt.xlabel("课程数量 (n)")
plt.ylabel("平均搜索节点数 - 对数轴")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6, which='both')
plt.savefig("report/nodes_compare.png", dpi=300)
plt.show()