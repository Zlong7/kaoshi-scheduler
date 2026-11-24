import csv
import statistics
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

data = {}

with open("report/results_raw.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        n, method = int(row["Size"]), row["Method"]
        if n not in data:
            data[n] = {'backtrack': {'times': [], 'nodes': []}, 'bnb': {'times': [], 'nodes': []}}

        t = float(row["Time(s)"])
        nodes = int(row["Nodes"])

        # 耗时：把正常和超时（=30）分开记录
        if t < 30.0:
            data[n][method]['times'].append(t)
        else:
            data[n][method]['times'].append(30.0)

        # 节点：只记录真正跑出来的节点数
        if nodes != -1:
            data[n][method]['nodes'].append(nodes)

sizes = sorted(data.keys())

# ---------- 图1：耗时对比 ----------
bt_t = [statistics.mean(data[n]['backtrack']['times']) for n in sizes]
bnb_t = [statistics.mean(data[n]['bnb']['times']) for n in sizes]

plt.figure(figsize=(10, 5))
plt.plot(sizes, bt_t, marker='o', label='回溯法平均耗时')
plt.plot(sizes, bnb_t, marker='s', label='分支限界平均耗时')
plt.yscale('log')
plt.xticks(sizes)
plt.title("算法平均耗时对比 (对数坐标, p=0.3, 上限30s)")
plt.xlabel("课程数量 (n)")
plt.ylabel("平均耗时 (秒) - 对数轴")
plt.grid(True, linestyle='--', alpha=0.6, which='both')
plt.legend()
plt.savefig("report/time_compare.png", dpi=300)
plt.show()

# ---------- 图2：节点数对比（仅看成功样本） ----------
bt_n, bnb_n = [], []
for n in sizes:
    bt_valid = data[n]['backtrack']['nodes']
    bnb_valid = data[n]['bnb']['nodes']
    bt_n.append(statistics.mean(bt_valid) if bt_valid else None)
    bnb_n.append(statistics.mean(bnb_valid) if bnb_valid else None)

plt.figure(figsize=(10, 5))
# 只画有成功样本的点
valid_bt_x = [sizes[i] for i in range(len(sizes)) if bt_n[i] is not None]
valid_bt_y = [v for v in bt_n if v is not None]
valid_bnb_x = [sizes[i] for i in range(len(sizes)) if bnb_n[i] is not None]
valid_bnb_y = [v for v in bnb_n if v is not None]

plt.plot(valid_bt_x, valid_bt_y, marker='o', label='回溯法平均节点数')
plt.plot(valid_bnb_x, valid_bnb_y, marker='s', label='分支限界平均节点数')

plt.yscale('log')
plt.xticks(sizes)
plt.title("成功求解样本的搜索节点数对比 (对数坐标, p=0.3)")
plt.xlabel("课程数量 (n)")
plt.ylabel("平均搜索节点数 - 对数轴")
plt.grid(True, linestyle='--', alpha=0.6, which='both')
plt.legend()
plt.savefig("report/nodes_compare.png", dpi=300)
plt.show()