import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.dates import DateFormatter

class MyFormatter(DateFormatter):
    def __call__(self, x, pos=0):
        result = super().__call__(x, pos)
        if '.' in result:
            pre, post = result.split('.')
            result = f"{pre}.{post[:3]}"
        return result

# 加载数据
def load_data(filename):
    file = pd.read_csv(filename)
    file['StorageTime'] = pd.to_datetime(file['timestamp'], unit='s')
    print(file.head())
    return file

# 绘图函数，包括滑块逻辑
def interactive_plot(data):
    # 初始显示范围
    start = 0
    end = start + 60

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 8))
    plt.subplots_adjust(bottom=0.35, hspace=0.4)  # 调整子图间距以便放置控件

    # 第一个子图：瞳孔直径
    scat_left = ax1.scatter(data['StorageTime'][start:end], data['FilteredLeftPupilDiameter'][start:end], color='b', label='Left Pupil Diameter', alpha=0.5)
    scat_right = ax1.scatter(data['StorageTime'][start:end], data['FilteredRightPupilDiameter'][start:end], color='g', label='Right Pupil Diameter', alpha=0.5)
    ax1.set_xlim(data['StorageTime'][start], data['StorageTime'][end - 1])  # 设置x轴的初始范围
    ax1.set_ylim(min(data['FilteredLeftPupilDiameter'].min(), data['FilteredRightPupilDiameter'].min()) * 0.95,
                 max(data['FilteredLeftPupilDiameter'].max(), data['FilteredRightPupilDiameter'].max()) * 1.05)
    ax1.set_ylabel('Pupil Diameter')
    ax1.legend()
    ax1.grid(True)
    ax1.xaxis.set_major_formatter(MyFormatter('%H:%M:%S.%f'))
    ax2.xaxis.set_major_formatter(MyFormatter('%H:%M:%S.%f'))

    # 第二个子图：眼睑开合
    line_left = ax2.plot(data['StorageTime'][start:end], data['LeftEyelidOpening'][start:end], color='lightblue', label='Left Eyelid Opening')[0]
    line_right = ax2.plot(data['StorageTime'][start:end], data['RightEyelidOpening'][start:end], color='lightgreen', label='Right Eyelid Opening')[0]
    ax2.set_ylim(-0.001,
                 max(data['LeftEyelidOpening'].max(), data['RightEyelidOpening'].max()) * 1.05)
    ax2.set_ylabel('Eyelid Opening')
    ax2.legend()
    ax2.grid(True)

    # 添加滑块
    ax_slider = plt.axes([0.1, 0.15, 0.8, 0.03])
    slider = Slider(ax_slider, 'Start Index', 0, len(data) - 100, valinit=start, valstep=1)

    # 添加按钮
    ax_button_left = plt.axes([0.1, 0.1, 0.1, 0.03])
    button_left = Button(ax_button_left, 'Left')
    ax_button_right = plt.axes([0.21, 0.1, 0.1, 0.03])
    button_right = Button(ax_button_right, 'Right')

    # 按钮事件处理函数
    def move_left(event):
        new_start = max(0, slider.val - 10)
        slider.set_val(new_start)

    def move_right(event):
        new_start = min(len(data) - 100, slider.val + 10)
        slider.set_val(new_start)

    button_left.on_clicked(move_left)
    button_right.on_clicked(move_right)

    # 更新函数，用于响应滑块操作
    def update(val):
        start = int(slider.val)
        end = start + 60
        scat_left.set_offsets(list(zip(data['StorageTime'][start:end], data['FilteredLeftPupilDiameter'][start:end])))
        scat_right.set_offsets(list(zip(data['StorageTime'][start:end], data['FilteredRightPupilDiameter'][start:end])))
        ax1.set_xlim(data['StorageTime'][start], data['StorageTime'][end - 1])  # 更新x轴范围

        line_left.set_data(data['StorageTime'][start:end], data['LeftEyelidOpening'][start:end])
        line_right.set_data(data['StorageTime'][start:end], data['RightEyelidOpening'][start:end])

        fig.canvas.draw_idle()

    slider.on_changed(update)  # 滑块变化时调用更新函数

    plt.show()

# 主函数
def main():
    filename = r'E:\NFB_data_backup\20240730\S12_D01\EYE_20240730150926.csv'  # 修改为你的文件名
    data = load_data(filename)
    interactive_plot(data)

if __name__ == "__main__":
    main()
