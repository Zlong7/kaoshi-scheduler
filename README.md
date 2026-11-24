# 高校期末考试排考优化 (Exam Scheduling Optimization)

## 项目简介
本项目将高校期末考试排考问题抽象为**图着色问题 (Graph Coloring)**，使用**贪心算法**求上界，并使用**回溯法 (Backtracking)** 和 **分支限界法 (Branch and Bound)** 求解最少考试时间段与合法的排考方案。项目包含完整的数据集、正确的算法实现、严谨的实验对比与可视化功能。

## 环境依赖
- Python 3.8+
- 安装依赖包：
  ```bash
  pip install -r requirements.txt