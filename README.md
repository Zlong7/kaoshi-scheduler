# 高校期末考试排考优化 (Exam Scheduling Optimization)

## 项目简介
本项目将高校期末考试排考问题抽象为**图着色问题 (Graph Coloring)**，使用**回溯法 (Backtracking)** 和 **分支限界法 (Branch and Bound)** 求解最少考试时间段与合法的排考方案。

## 环境依赖
- Python 3.8+
- matplotlib (仅用于可视化)

## 目录结构
- `data/`：测试数据集（toy6、空图、完全图、二部图等）
- `src/`：核心源码
  - `io_utils.py`：图数据读取
  - `verify.py`：合法性校验
  - `backtrack.py`：回溯法实现
  - `bnb.py`：分支限界法实现
  - `visualize.py`：排考日历可视化
- `experiments/`：批量测试与绘图脚本

## 运行方式
请在项目根目录下运行以下命令：

1. **运行基础算法对比测试**：
   ```bash
   python -m src.test_algo