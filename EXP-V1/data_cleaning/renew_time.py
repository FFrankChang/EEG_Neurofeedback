import pandas as pd
from scipy.spatial import KDTree

def load_data(file_a_path, file_b_path):
    # 加载文件A和文件B
    file_a = pd.read_csv(file_a_path)
    file_b = pd.read_csv(file_b_path)
    return file_a, file_b

def find_nearest_time_ms(timestamp, timestamp_tree, file_b):
    # 在文件B中找到与给定时间戳最接近的time_ms，并转换为秒
    distance, index = timestamp_tree.query([timestamp])
    return file_b.loc[index, 'time_ms'] / 1000  # 转换毫秒到秒

def update_timestamps(file_a, file_b):
    # 创建KDTree以进行高效的最近时间戳搜索
    timestamp_tree = KDTree(file_b[['timestamp']].values)
    
    # 更新文件A中的segmentStart和segmentEnd，转换结果为秒
    file_a['segmentStart'] = file_a['segmentStart'].apply(lambda x: find_nearest_time_ms(x, timestamp_tree, file_b))
    file_a['segmentEnd'] = file_a['segmentEnd'].apply(lambda x: find_nearest_time_ms(x, timestamp_tree, file_b))
    return file_a

def save_updated_file(file_a, output_path):
    # 保存处理后的文件A
    file_a.to_csv(output_path, index=False)

# 主执行代码
def main():
    file_a_path = r'E:\Frank_Projects\EEG_Neurofeedback_Frank\S03_segment.csv'  # 这里替换为您的文件A路径
    file_b_path = r'E:\Frank_Projects\EEG_Neurofeedback_Frank\S03_eye_data.csv'  # 这里替换为您的文件B路径

    # 加载数据
    file_a, file_b = load_data(file_a_path, file_b_path)
    
    # 更新时间戳
    updated_file_a = update_timestamps(file_a, file_b)
    
    # 定义输出文件路径
    output_path = 'updated_file.csv'
    
    # 保存更新后的文件
    save_updated_file(updated_file_a, output_path)
    
    print("File has been updated and saved in seconds.")

# 运行主函数
if __name__ == '__main__':
    main()
