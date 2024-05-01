import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, welch 

# 带通滤波函数
def bandpass_filter(data, lowcut=1.0, highcut=40.0, fs=1000, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    sos = butter(order, [low, high], btype='band', output='sos')
    y = filtfilt(sos, data, axis=0)
    return y


# 读取CSV文件
def load_data(filename):
    data = pd.read_csv(filename, usecols=['timestamp', 'F7'])
    return data

def plot_results(original_data, filtered_data, timestamps, fs=1000):
    fig, axs = plt.subplots(2, 1, figsize=(10, 12))  # 创建两个子图

    # 时间序列子图
    color = 'tab:blue'
    axs[0].set_xlabel('Timestamp')
    axs[0].set_ylabel('Original F7 Data', color=color)
    axs[0].plot(timestamps, original_data, label='Original F7 Data', color=color, alpha=0.7)
    axs[0].tick_params(axis='y', labelcolor=color)

    ax2 = axs[0].twinx()
    color = 'tab:red'
    ax2.set_ylabel('Filtered F7 Data', color=color)
    ax2.plot(timestamps, filtered_data, label='Filtered F7 Data', color=color, linewidth=2)
    ax2.tick_params(axis='y', labelcolor=color)
    
    # PSD子图
    f_orig, Pxx_orig = welch(original_data, fs, nperseg=1024)
    f_filt, Pxx_filt = welch(filtered_data, fs, nperseg=1024)
    
    axs[1].plot(f_orig, Pxx_orig, label='Original PSD')
    axs[1].plot(f_filt, Pxx_filt, label='Filtered PSD', linestyle='--')
    axs[1].set_title('Power Spectral Densities of Original and Filtered Data')
    axs[1].set_xlabel('Frequency (Hz)')
    axs[1].set_ylabel('PSD (V²/Hz)')
    axs[1].set_xlim([0,50])
    axs[1].legend()

    plt.tight_layout()  # 自动调整子图参数，以给定的填充
    plt.show()

# 主函数
def main():
    filename = 'D:\\Frank_Project\\EEG_Neurofeedback\\data\\20240430_01_final_02\\eegraw_20240430_152635_final.csv'
    data = load_data(filename)
    filtered_signal = bandpass_filter(data['F7'], fs=1000)
    plot_results(data['F7'], filtered_signal, data['timestamp'], fs=1000)

if __name__ == '__main__':
    main()
