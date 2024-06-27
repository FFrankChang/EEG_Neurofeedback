import pandas as pd

def find_closest_timestamp(data_df, event_df):
    sample_rate = 1000
    results = []
    for index, event in event_df.iterrows():
        timestamp = event['timestamp']
        # 寻找最接近的时间戳
        closest_idx = (data_df['timestamp'] - timestamp).abs().idxmin()
        # 确保返回重复时间戳中的第一个索引
        closest_timestamp = data_df.loc[closest_idx, 'timestamp']
        first_occurrence_idx = data_df[data_df['timestamp'] == closest_timestamp].index[0]
        results.append({
            'Latency': first_occurrence_idx / sample_rate,
            'Type': event['Event_Type'],
            'Position': 1
        })
    return results

def main():
    # 加载数据
    subject = 's09'
    condition = 'silence'
    scenario = 'hard'
    data_df = pd.read_csv(f'{subject}_{scenario}_{condition}.csv')
    event_df = pd.read_csv(f'{subject}_{scenario}_{condition}_event.csv')

    # 查找最接近的时间戳
    results = find_closest_timestamp(data_df, event_df)

    # 保存结果
    results_df = pd.DataFrame(results)
    results_df.to_csv(f'{subject}_{scenario}_{condition}_event.txt', index=False, header=True, sep='\t')

if __name__ == "__main__":
    main()
