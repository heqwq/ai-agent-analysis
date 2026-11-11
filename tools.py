import pandas as pd
import matplotlib.pyplot as plt
from langchain.tools import tool
import uuid

# 解决图表中文显示乱码的问题
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


# 工具1：探查数据结构
@tool
def get_data_info(csv_path: str) -> str:
    """读取CSV文件，返回所有列名和数据类型。在分析前先调用此工具了解数据结构。"""
    try:
        df = pd.read_csv(csv_path, nrows=5)
        info = f"文件读取成功，共有 {len(df.columns)} 列。各列信息如下：\n"
        for col in df.columns:
            info += f"- 列名: '{col}', 数据类型: {df[col].dtype}\n"
        return info
    except Exception as e:
        return f"读取失败: {str(e)}"


# 工具2：检测异常（查重 + 3σ原则找偏大/偏小）
@tool
def detect_anomaly(csv_path: str, column_name: str) -> str:
    """分析数据，查找重复行，并用3σ原则找出异常大或异常小的数值。"""
    try:
        df = pd.read_csv(csv_path)

        if column_name not in df.columns:
            return f"错误：找不到列名 '{column_name}'。请先用 get_data_info 查看可用列名。"

        # 1. 查重复行
        duplicate_count = df.duplicated().sum()

        # 2. 算平均值和标准差 (3σ原则)
        col_data = df[column_name]
        mean = col_data.mean()
        std = col_data.std()

        # 防呆：如果标准差是0或空值（数据太少或全一样），没法算
        if pd.isna(std) or std == 0:
            return f"列 '{column_name}' 的数据没有波动或数据量太少，无法使用3σ原则检测。"

        upper_limit = mean + 3 * std  # 异常上限
        lower_limit = mean - 3 * std  # 异常下限

        # 筛选出超过上限 或 低于下限的异常点
        outliers = df[(col_data > upper_limit) | (col_data < lower_limit)]

        # 组合报告
        report = f"【数据扫描报告】\n"
        report += f"1. 查重：全表共发现 {duplicate_count} 条完全重复的垃圾数据。\n"
        report += f"2. 统计：列 '{column_name}' 的正常平均值是 {mean:.2f}。\n"
        report += f"3. 标准：正常数据应在 {lower_limit:.2f} 到 {upper_limit:.2f} 之间。\n"
        report += f"4. 结果：超出此范围的异常数据共有 {len(outliers)} 条。\n"

        if len(outliers) > 0:
            report += f"   异常数据部分行号：{outliers.index.tolist()[:10]}\n"

        return report
    except Exception as e:
        return f"检测失败，原因：{str(e)}"


# 工具3：画图并保存
@tool
def plot_anomalies(csv_path: str, column_name: str) -> str:
    """生成带有异常红点的折线图，基于3σ原则标注偏大或偏小的异常值。"""
    try:
        df = pd.read_csv(csv_path)
        if column_name not in df.columns:
            return f"画图失败：找不到列名 '{column_name}'。"
        col_data = df[column_name]

        mean = col_data.mean()
        std = col_data.std()

        if pd.isna(std) or std == 0:
            return f"画图失败：数据没有波动，无法标注异常。"

        upper_limit = mean + 3 * std
        lower_limit = mean - 3 * std

        # 找出异常点
        outliers = df[(col_data > upper_limit) | (col_data < lower_limit)]

        plt.figure(figsize=(10, 5))
        # 画正常的蓝线
        plt.plot(df.index, col_data, color='blue', label='正常数据')
        # 画异常的红点
        plt.scatter(outliers.index, outliers[column_name], color='red', label='异常点')

        plt.title(f"{column_name} 异常检测 (3σ原则)")
        plt.legend()

        # 生成防缓存图片名
        plot_filename = f"plot_{uuid.uuid4().hex[:8]}.png"
        plt.savefig(plot_filename)
        plt.close()

        return f"画图成功！图表已保存，文件名为：{plot_filename}"
    except Exception as e:
        return f"画图失败，原因：{str(e)}"