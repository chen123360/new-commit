import matplotlib.pyplot as plt
import pandas as pd
import os

# 设置中文字体，防止画图乱码
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ==========================================
# 1. 读取函数
# ==========================================
def load_dev_data(file_path, label):
    try:
        print(f"正在读取: {file_path} ...")
        # PyroSim的devc文件通常需要跳过第一行
        data = pd.read_csv(file_path, skiprows=1)

        # 提取三列数据
        time = data['Time']
        temp = data['TC_Center']
        co = data['CO_Center']

        print(f"✅ {file_path} 读取成功")
        return time, temp, co, label

    except FileNotFoundError:
        print(f"❌ 错误: 找不到文件 '{file_path}'")
        return None, None, None, None
    except Exception as e:
        print(f"❌ 读取出错: {e}")
        return None, None, None, None

# ==========================================
# 2. 主程序：循环读取三组数据
# ==========================================
def main():
    # ==============================
    # 修改文件名
    # ==============================
    files_config = [
        {'name': 'grid_0.1.csv', 'label': '0.1m 网格 (精细)'},
        {'name': 'grid_0.2.csv', 'label': '0.2m 网格 (中等)'},
        {'name': 'grid_0.5.csv', 'label': '0.5m 网格 (粗糙)'},
    ]

    # 创建两个画布，一个画温度，一个画CO
    plt.figure(figsize=(10, 6)) # 图1：温度
    plt.figure(figsize=(10, 6)) # 图2：一氧化碳

    for config in files_config:
        # ==========================================
        # 🛠️ 修改这里：告诉程序去上一级目录的 results 文件夹找文件
        # ==========================================
        # os.path.join("..", "results", config['name']) 的意思是：
        # 1. ..  代表“退回到上一级目录” (从 scripts 退回到 GridSensitivityAnalysis)
        # 2. results 代表进入 results 文件夹
        # 3. config['name'] 是具体的文件名
        file_path = os.path.join("..", "results", config['name'])

        # 读取数据
        t, temp, co, lbl = load_dev_data(file_path, config['label'])

        if t is not None:
            # --- 绘制温度图 ---
            plt.figure(1) # 切换到图1
            plt.plot(t, temp, linewidth=2, label=lbl)

            # --- 绘制CO图 ---
            plt.figure(2) # 切换到图2
            plt.plot(t, co, linewidth=2, label=lbl)

    # ==========================================
    # 3. 图表美化 (保持不变)
    # ==========================================

    # 美化温度图
    plt.figure(1)
    plt.title('不同网格尺寸下的中心点温度 (TC) 对比', fontsize=15)
    plt.xlabel('时间 (s)', fontsize=12)
    plt.ylabel('温度 (°C)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(title="网格精度")
    plt.tight_layout()

    # 美化CO图
    plt.figure(2)
    plt.title('不同网格尺寸下的中心点CO浓度对比', fontsize=15)
    plt.xlabel('时间 (s)', fontsize=12)
    plt.ylabel('CO 摩尔分数 (mol/mol)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(title="网格精度")
    plt.tight_layout()

    print("\n✅ 所有数据处理完毕，正在显示图表...")
    plt.show()

if __name__ == "__main__":
    main()