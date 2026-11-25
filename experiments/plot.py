import csv
import statistics
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

data = {}
# 记录成功次数，用于在图表上标注
success_counts = {'backtrack': {}, 'bnb': {}}

with open("report/results_raw.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        n, method = int(row["Size"]), row["Method"]
        if n not in data:
            data[n] = {'backtrack': {'times': [], 'nodes': []}, 'bnb': {'times': [], 'nodes': []}}
            success_counts['backtrack'][n] = 0
            success_counts['bnb'][n] = 0

        t = float(row["Time(s)"])
        nodes = int(row["Nodes"])

        if t < 30.0:
            data[n][method]['times'].append(t)
        else:
            data[n][method]['times'].append(30.0)

        if nodes != -1:
            data[n][method]['nodes'].append(nodes)
            success_counts[method][n] += 1

sizes = sorted(data.keys())

# ---------- 图1：耗时对比 ----------
bt_t = [statistics.mean(data[n]['backtrack']['times']) for n in sizes]
bnb_t = [statistics.mean(data[n]['bnb']['times']) for n in sizes]

plt.figure(figsize=(10, 5))
plt.plot(sizes, bt_t, marker='o', label='回溯法')
plt.plot(sizes, bnb_t, marker='s', label='分支限界')
plt.yscale('log')
plt.xticks(sizes)
# 【修复】修改标题
plt.title("算法耗时对比 (30秒截尾平均耗时, 超时按30s计入)")
plt.xlabel("课程数量 (n)")
plt.ylabel("平均耗时 (秒) - 对数轴")
plt.grid(True, linestyle='--', alpha=0.6, which='both')
plt.legend()
plt.savefig("report/time_compare.png", dpi=300)
plt.show()

# ---------- 图2：节点数对比 ----------
bt_n, bnb_n = [], []
for n in sizes:
    bt_valid = data[n]['backtrack']['nodes']
    bnb_valid = data[n]['bnb']['nodes']
    bt_n.append(statistics.mean(bt_valid) if bt_valid else None)
    bnb_n.append(statistics.mean(bnb_valid) if bnb_valid else None)

plt.figure(figsize=(10, 5))
valid_bt_x = [sizes[i] for i in range(len(sizes)) if bt_n[i] is not None]
valid_bt_y = [v for v in bt_n if v is not None]
valid_bnb_x = [sizes[i] for i in range(len(sizes)) if bnb_n[i] is not None]
valid_bnb_y = [v for v in bnb_n if v is not None]

plt.plot(valid_bt_x, valid_bt_y, marker='o', label='回溯法')
plt.plot(valid_bnb_x, valid_bnb_y, marker='s', label='分支限界')

plt.yscale('log')
plt.xticks(sizes)
plt.title("成功求解样本的搜索节点数对比 (对数坐标)")
plt.xlabel("课程数量 (n)")
plt.ylabel("平均搜索节点数 (仅限成功样本)")

# 【修复】在图上添加文本标注成功率
if 40 in success_counts['backtrack']:
    bt_40 = success_counts['backtrack'][40]
    bnb_40 = success_counts['bnb'][40]
    plt.annotate(f'n=40 回溯成功 {bt_40}/5\nn=40 分支限界成功 {bnb_40}/5',
                 xy=(40, valid_bnb_y[-1]), xytext=(25, valid_bnb_y[-1] * 10),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6))

plt.annotate('n=80, 120 均无成功样本', xy=(80, 10), xytext=(60, 100))

plt.grid(True, linestyle='--', alpha=0.6, which='both')
plt.legend()
plt.savefig("report/nodes_compare.png", dpi=300)
plt.show()