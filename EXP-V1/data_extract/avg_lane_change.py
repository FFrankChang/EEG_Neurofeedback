import numpy as np

# 参数设定
num_participants = 10
num_days = 3
num_trials_per_day = 10
max_lanes = 4
target_lanes = 1.5

# 模拟数据生成函数
def generate_simulated_data(num_participants, num_days, num_trials_per_day, max_lanes, target_lanes):
    results = {}
    for participant in range(1, num_participants + 1):
        participant_results = []
        for day in range(1, num_days + 1):
            # 计算每天的平均车道数
            day_mean = max_lanes - ((max_lanes - target_lanes) / num_days * day)
            # 确保每天的平均车道数不小于目标车道数
            day_mean = max(day_mean, target_lanes)
            # 生成每次实验的结果
            trials = np.random.normal(loc=day_mean, scale=0.2, size=num_trials_per_day)
            # 确保车道数不超过最大值
            trials = np.clip(trials, target_lanes, max_lanes)
            participant_results.append(trials)
        results[participant] = np.array(participant_results)
    return results

# 生成模拟数据
simulated_data = generate_simulated_data(num_participants, num_days, num_trials_per_day, max_lanes, target_lanes)

# 打印结果
for participant, data in simulated_data.items():
    print(f"Participant {participant}:")
    for day, trials in enumerate(data, start=1):
        print(f"  Day {day}: {trials}")
