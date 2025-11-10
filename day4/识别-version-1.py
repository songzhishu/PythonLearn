from ultralytics import YOLO
import cv2
import time
import mss
import numpy as np
from screeninfo import get_monitors

# --- 核心改动：自动获取屏幕分辨率 ---
def get_screen_resolution():
    """自动获取主屏幕的宽度和高度"""
    monitors = get_monitors()
    primary_monitor = monitors[0]  # 取第一个屏幕（主屏幕）
    return primary_monitor.width, primary_monitor.height

# --- 初始化 ---
# 1. 加载 YOLOv8 模型
model = YOLO("yolov8n-pose.pt")

# 2. 自动获取屏幕分辨率
screen_width, screen_height = get_screen_resolution()
print(f"自动检测屏幕分辨率：{screen_width}x{screen_height}")

# 3. 初始化屏幕捕获（居中捕获 800x600 区域，适配自动获取的分辨率）
sct = mss.mss()
monitor = {
    "top": (screen_height - 600) // 2,    # 垂直居中
    "left": (screen_width - 800) // 2,    # 水平居中
    "width": 800,
    "height": 600
}

# 帧率计算变量
pTime = 0

# --- 主循环 ---
while True:
    # 屏幕捕获
    sct_img = sct.grab(monitor)
    frame = np.array(sct_img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    if frame is None:
        continue

    # YOLOv8 姿态检测
    results = model(frame, verbose=False, conf=0.5)
    annotated_frame = frame.copy()

    if results and len(results) > 0:
        result = results[0]
        # 绘制骨骼
        annotated_frame = result.plot(conf=False, line_width=2, kpt_radius=3)
        # 提取坐标
        if result.keypoints is not None and len(result.keypoints.data) > 0:
            for person_idx, keypoints in enumerate(result.keypoints.data):
                keypoints = keypoints.cpu().numpy()
                print(f"\n=== 第 {person_idx + 1} 个人 ===")
                for kpt_id, (x, y, conf) in enumerate(keypoints):
                    if conf > 0.5:
                        cx, cy = int(x), int(y)
                        # 屏幕绝对坐标（自动适配分辨率）
                        screen_x = cx + monitor["left"]
                        screen_y = cy + monitor["top"]
                        kpt_name = model.names.get(kpt_id, f"关键点{kpt_id}")
                        print(f"{kpt_name}: 区域坐标({cx},{cy}) | 屏幕坐标({screen_x},{screen_y})")
                        # 标记鼻子
                        if kpt_id == 0:
                            cv2.circle(annotated_frame, (cx, cy), 5, (0, 255, 0), cv2.FILLED)

    # 显示帧率
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(annotated_frame, f"FPS: {int(fps)} | 分辨率: {screen_width}x{screen_height}",
                (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)

    # 显示窗口
    cv2.imshow("YOLOv8 屏幕姿态估计（自动适配分辨率）", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 释放资源
cv2.destroyAllWindows()
sct.close()
print("程序退出")