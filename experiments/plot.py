import csv
import matplotlib.pyplot as plt

# 设置中文字体，防止图表乱码 (Windows 下一般用黑体)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

sizes = []
bt_time, bnb_time = [], []
bt_nodes, bnb_nodes = [], []

with open("report/results.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        n = int(row["Size(n)"])
        method = row["Method"]

        if method == "backtrack":
            sizes.append(n)
            bt_time.append(float(row["Time(s)"]))
            bt_nodes.append(int(row["Nodes"]))
        else:
            bnb_time.append(float(row["Time(s)"]))
            bnb_nodes.append(int(row["Nodes"]))

# 画第一张图：耗时对比
plt.figure(figsize=(10, 5))
plt.plot(sizes, bt_time, marker='o', label='回溯法 (Backtrack)')
plt.plot(sizes, bnb_time, marker='s', label='分支限界 (BnB)')
plt.title("算法耗时对比 (随课程规模增加)")
plt.xlabel("课程数量 (n)")
plt.ylabel("平均耗时 (秒)")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig("report/time_compare.png")
plt.show()

# 画第二张图：搜索节点数对比
plt.figure(figsize=(10, 5))
plt.plot(sizes, bt_nodes, marker='o', label='回溯法 (Backtrack)')
plt.plot(sizes, bnb_nodes, marker='s', label='分支限界 (BnB)')
plt.title("搜索节点数对比 (随课程规模增加)")
plt.xlabel("课程数量 (n)")
plt.ylabel("平均搜索节点数")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig("report/nodes_compare.png")
plt.show()