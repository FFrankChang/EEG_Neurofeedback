from pydub import AudioSegment
from pydub.generators import Sine

def generate_beeps(duration=60, beep_duration=100, frequency=1000):
    # 创建一个静音的音频段
    silent_segment = AudioSegment.silent(duration=1000 - beep_duration)
    # 创建一个频率为1000Hz的正弦波beep音，持续时间为100毫秒
    beep = Sine(frequency).to_audio_segment(duration=beep_duration).apply_gain(-3)  # 调整一点增益

    # 创建一个包含60个beep的音频段，每个beep后接一个静音段
    one_minute_beep = beep + silent_segment
    one_minute_audio = one_minute_beep * duration  # 持续60秒

    return one_minute_audio

# 生成音频
beep_audio = generate_beeps()

# 导出到文件
beep_audio.export("one_minute_beeps.wav", format="wav")

print("音频已生成并保存为 one_minute_beeps.wav")
