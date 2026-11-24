import matplotlib.pyplot as plt
from src.io_utils import read_graph, build_adj_matrix
from src.backtrack import color_backtrack

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def draw_calendar(n, sol):
    """把排考方案画成甘特图（日历）的形式"""
    # 记录每个时间段里有哪些课
    slots = {}
    for i, slot in enumerate(sol):
        if slot not in slots:
            slots[slot] = []
        slots[slot].append(chr(65 + i))  # 转成 A, B, C...

    # 找出哪个时间段课最多，用来决定图有多高
    max_courses = max(len(c) for c in slots.values())

    # 根据课的数量动态调整画布高度
    fig, ax = plt.subplots(figsize=(10, max(3, max_courses * 0.8)))

    colors = ['#ef4444', '#f59e0b', '#10b981', '#8b5cf6', '#06b6d4', '#ec4899']

    for slot, c_list in slots.items():
        # 颜色根据时间段固定
        color = colors[slot % len(colors)]

        for j, c in enumerate(c_list):
            # 【修复点】：让 y 坐标随 j 变化（上下错开），而不是固定在 0
            y_pos = j

            # 画方块
            ax.barh(y=y_pos, width=0.8, left=slot, color=color,
                    edgecolor='white', height=0.8)
            # 写字
            ax.text(slot + 0.4, y_pos, c, ha='center', va='center',
                    color='white', fontweight='bold', fontsize=14)

    # 设置图表范围
    ax.set_xlim(-0.5, max(slots.keys()) + 1.5)
    ax.set_ylim(-0.5, max_courses - 0.5)

    # 设置X轴刻度
    ax.set_xticks(range(max(slots.keys()) + 1))
    ax.set_xticklabels([f"时间段 {k + 1}" for k in range(max(slots.keys()) + 1)], fontsize=12)

    # 隐藏 Y 轴
    ax.set_yticks([])

    # 把 Y 轴翻转一下，让第一门课在上面
    ax.invert_yaxis()

    # 加上竖线网格，看起来更像表格
    for k in range(max(slots.keys()) + 2):
        ax.axvline(x=k - 0.5, color='#cbd5e1', linestyle='--', linewidth=1)

    ax.set_title("可视化排考日历 (每块代表一门课程)", fontsize=16, pad=15)

    plt.tight_layout()
    plt.savefig("report/schedule_calendar.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    n, edges = read_graph("data/toy6.txt")
    G = build_adj_matrix(n, edges)
    K, sol, _ = color_backtrack(G)
    print(f"排考方案: {sol}")
    draw_calendar(n, sol)