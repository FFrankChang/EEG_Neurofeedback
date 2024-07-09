import cv2
import datetime

def add_timestamp(frame, timestamp):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, timestamp, (10, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    return frame

# 设置视频捕捉
cap = cv2.VideoCapture(0)  # 0 表示默认摄像头

# 设置视频编解码器和输出文件
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 对于MP4格式，使用MP4V编码
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (1280, 720))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        # 获取当前时间戳
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        # 将时间戳添加到帧上
        frame = add_timestamp(frame, timestamp)
        # 写入帧
        out.write(frame)
        
        # 显示带时间戳的视频帧
        cv2.imshow('Video with Timestamp', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# 释放资源
cap.release()
out.release()
cv2.destroyAllWindows()
