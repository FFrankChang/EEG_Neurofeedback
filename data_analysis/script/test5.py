from scipy.signal import buttord

# 设定通带和阻带频率边界（Hz）
lowcut = 1.0
highcut = 40.0
fs = 1000  # 采样频率

# 通带和阻带频率，转化为归一化频率
nyq = 0.5 * fs
low = lowcut / nyq
high = highcut / nyq

# 通带和阻带容忍度（以dB为单位）
gpass = 3  # 通带最大损失
gstop = 40  # 阻带最小衰减

# 计算滤波器阶数
order, wn = buttord([low, high], [low * 0.9, high * 1.1], gpass, gstop)
print(f"Recommended filter order: {order}")
