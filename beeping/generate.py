from pydub import AudioSegment
import os

# 音频文件路径
input_file = r'D:\gitee\EEG_Neurofeedback\beeping\heartbeat.MP3'

# 加载音频
audio = AudioSegment.from_mp3(input_file)

# 目标长度：5000ms（5秒）
target_length = 5 * 1000

# 循环音频直到达到目标长度
long_audio = audio
while len(long_audio) < target_length:
    long_audio += audio

# 如果超过5秒，就截断到5秒
if len(long_audio) > target_length:
    long_audio = long_audio[:target_length]

# 输出文件路径
output_file = 'new.mp3'

# 导出音频
long_audio.export(output_file, format="mp3")

print(f"Generated audio file saved as {output_file}")
