from ultralytics import YOLO
import cv2
import time
import mss
import numpy as np
from screeninfo import get_monitors
from PIL import Image, ImageDraw, ImageFont
import os


# 自动获取屏幕分辨率
def get_screen_resolution():
    monitors = get_monitors()
    primary_monitor = monitors[0]
    return primary_monitor.width, primary_monitor.height


# 使用 Pillow 渲染中文到 OpenCV 画面
def draw_chinese_text(img, text, position, font_size=28, color=(0, 255, 255)):
    pil_img = Image.fromarray(img)
    draw = ImageDraw.Draw(pil_img)

    font_paths = [
        r"C:\Windows\Fonts\simsun.ttc",  # 宋体
        r"C:\Windows\Fonts\simhei.ttf",  # 黑体
        r"C:\Windows\Fonts\simkai.ttf"   # 楷体
    ]

    font = None
    for font_path in font_paths:
        if os.path.exists(font_path):
            font = ImageFont.truetype(font_path, font_size)
            break

    if font is None:  # 找不到中文字体就用默认字体
        font = ImageFont.load_default()

    draw.text(position, text, fill=color, font=font)
    return np.array(pil_img)


# --- 初始化 YOLO ---
model = YOLO("yolov8n-pose.pt")

screen_width, screen_height = get_screen_resolution()
print(f"屏幕分辨率：{screen_width}x{screen_height}")

sct = mss.mss()
monitor = sct.monitors[1]

pTime = 0
max_fps = 30
frame_interval = 1.0 / max_fps

POSE_CONNECTIONS = [
    (0, 1), (0, 2), (1, 3), (2, 4),
    (5, 6), (5, 7), (7, 9), (6, 8), (8, 10),
    (11, 12), (11, 13), (13, 15), (12, 14), (14, 16),
    (5, 11), (6, 12)
]


# --- 主循环 ---
while True:
    current_time = time.time()

    if current_time - pTime < frame_interval:
        time.sleep(0.001)
        continue

    time_diff = max(current_time - pTime, 0.001)
    pTime = current_time
    fps = 1 / time_diff

    try:
        sct_img = sct.grab(monitor)
    except Exception as e:
        print(f"捕获异常：{e}")
        continue

    frame = np.frombuffer(sct_img.rgb, dtype=np.uint8).reshape(sct_img.height, sct_img.width, 3)
    results = model(frame, verbose=False, conf=0.4, iou=0.5)
    annotated_frame = frame.copy()

    if results and len(results) > 0:
        result = results[0]
        if result.keypoints is not None and len(result.keypoints.data) > 0:
            for keypoints in result.keypoints.data:
                keypoints = keypoints.cpu().numpy()
                visible_kpts = []
                for x, y, conf in keypoints:
                    if conf > 0.4:
                        cx, cy = int(x), int(y)
                        visible_kpts.append((cx, cy))
                        cv2.circle(annotated_frame, (cx, cy), 3, (0, 0, 255), cv2.FILLED)

                for a, b in POSE_CONNECTIONS:
                    if a < len(visible_kpts) and b < len(visible_kpts):
                        cv2.line(annotated_frame, visible_kpts[a], visible_kpts[b], (255, 0, 0), 2)

    # 用 Pillow 添加中文
    info_text = f"FPS: {int(fps)} | 全屏骨骼检测 | 按 'q' 退出"
    annotated_frame = draw_chinese_text(annotated_frame, info_text, (10, 40), font_size=30)

    cv2.imshow("YOLOv8 全屏骨骼检测（中文正常显示）", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
sct.close()
print("程序退出 ✅")
