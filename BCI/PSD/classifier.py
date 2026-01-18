import csv
import time
import random
import os
from datetime import datetime
import msvcrt  # Windows keyboard input

def simulate_data_collection():

    frame_count = 0
    while True:

        # 检测按键
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key.lower() == b'q':
                print(f"\n数据收集结束")
                break
    
    return frame_count

def run_mock_classifier():
    time.sleep(1) 
    label = random.randint(1, 4)
    print(f"人群类型标签: {label}")
    print("=" * 50)
    
    return label

def save_to_csv(start_time, end_time, label, frame_count):
    """保存运行记录到 CSV 文件"""
    # 确保 data 目录存在
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    csv_filename = f'{timestamp}.csv'
    csv_filepath = os.path.join(data_dir, csv_filename)
    
    # 写入 CSV
    with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['start_time', 'end_time', 'duration_seconds', 'label', 'frames_collected']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerow({
            'start_time': start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'duration_seconds': (end_time - start_time).total_seconds(),
            'label': label,
            'frames_collected': frame_count
        })
    
    print(f"\n记录已保存到: {csv_filepath}")

def main():
    """主函数"""

    
    start_time = datetime.now()
    
    frame_count = simulate_data_collection()

    label = run_mock_classifier()
    
    end_time = datetime.now()

    save_to_csv(start_time, end_time, label, frame_count)
    

if __name__ == "__main__":
    main()
