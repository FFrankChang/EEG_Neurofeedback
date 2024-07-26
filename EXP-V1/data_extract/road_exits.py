import pandas as pd

def calculate_road_exits(data):
    """
    计算车辆离开道路的次数。

    参数:
        data (pd.DataFrame): 包含车辆轨迹数据的DataFrame，必须包含'Location_y'列。

    返回:
        int: 车辆离开道路的次数。
    """
    # 标记是否在道路内
    data['On_Road'] = (data['Location_y'] >= 2992.5) & (data['Location_y'] <= 3000)

    # 找到状态改变的地方（从道路内到道路外，或从道路外到道路内）
    transitions = data['On_Road'].astype(int).diff().ne(0)

    # 离开道路的次数，即从道路外到道路内的转变
    road_exits = ((transitions) & (data['On_Road'].shift(-1) == True)).sum()

    return road_exits

# 读取数据
file_path = '/path/to/your/file.csv'  # 请替换为您的文件路径
data = pd.read_csv(file_path)

# 使用函数计算离开道路的次数
exits_count = calculate_road_exits(data)

# 输出结果
print(f"车辆离开道路的次数: {exits_count}")
