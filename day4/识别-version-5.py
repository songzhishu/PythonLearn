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

# 用 Pillow 渲染中文到 OpenCV 图像
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
            try:
                font = ImageFont.truetype(font_path, font_size)
                break
            except Exception:
                font = None

    if font is None:  # 找不到中文字体就用默认
        font = ImageFont.load_default()

    draw.text(position, text, fill=color, font=font)
    return np.array(pil_img)

# --- 初始化 ---
model = YOLO("yolov8n-pose.pt")  # 确保模型文件存在
screen_width, screen_height = get_screen_resolution()
print(f"屏幕分辨率：{screen_width}x{screen_height}")

sct = mss.mss()
monitor = sct.monitors[1]  # 主屏幕

# 帧率控制
pTime = time.time()
max_fps = 30
frame_interval = 1.0 / max_fps

# POSE 连接（确保与模型 keypoint 数量/索引对应）
POSE_CONNECTIONS = [
    (0, 1), (0, 2), (1, 3), (2, 4),
    (5, 6), (5, 7), (7, 9), (6, 8), (8, 10),
    (11, 12), (11, 13), (13, 15), (12, 14), (14, 16),
    (5, 11), (6, 12)
]

# 主循环
try:
    while True:
        now = time.time()
        # 简单帧率控制：如果间隔太小，短暂睡眠
        elapsed = now - pTime
        if elapsed < frame_interval:
            time.sleep(max(0.001, frame_interval - elapsed))
            continue
        pTime = time.time()

        # 捕获屏幕
        try:
            sct_img = sct.grab(monitor)
        except Exception as e:
            print("屏幕捕获异常：", e)
            time.sleep(0.01)
            continue

        # 将 mss 返回的对象转换为 numpy 数组（注意 mss 返回 BGRA）
        frame_bgra = np.array(sct_img)  # shape: (h, w, 4)
        # 转成 BGR（OpenCV 使用 BGR）
        if frame_bgra.shape[2] == 4:
            frame = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)
        else:
            frame = cv2.cvtColor(frame_bgra, cv2.COLOR_RGB2BGR)

        # 运行 YOLOv8-pose（inference）
        results = model(frame, verbose=False, conf=0.4, iou=0.5)

        annotated_frame = frame.copy()

        # 绘制骨骼：按 keypoint ID 索引位置绘制，避免索引错位
        if results and len(results) > 0:
            result = results[0]
            # result.keypoints.data: (n_instances, n_keypoints, 3)
            if result.keypoints is not None and len(result.keypoints.data) > 0:
                for kpts_tensor in result.keypoints.data:
                    # 将 tensor 转 numpy （如果在 CPU 上的话，直接 .numpy()）
                    try:
                        kpts = kpts_tensor.cpu().numpy()
                    except Exception:
                        kpts = np.array(kpts_tensor)

                    # 建立一个固定长度的点列表（以 keypoint ID 为索引）
                    points = [None] * len(kpts)  # len(kpts) 通常是关键点数量，如17或33
                    for idx, (x, y, conf) in enumerate(kpts):
                        if conf > 0.4:
                            cx, cy = int(round(x)), int(round(y))
                            points[idx] = (cx, cy)
                            cv2.circle(annotated_frame, (cx, cy), 3, (0, 0, 255), cv2.FILLED)

                    # 按 POSE_CONNECTIONS 用原始 ID 去连线（只在两端都可见时画线）
                    for a, b in POSE_CONNECTIONS:
                        if a < len(points) and b < len(points):
                            if points[a] is not None and points[b] is not None:
                                cv2.line(annotated_frame, points[a], points[b], (255, 0, 0), 2)

        # 计算并显示 FPS（更稳定）
        curr_time = time.time()
        fps = 1.0 / max(1e-6, (curr_time - now))
        info_text = f"FPS: {int(fps)} | 全屏骨骼检测 | 按 'q' 退出"

        # 用 Pillow 渲染中文文本
        annotated_frame = draw_chinese_text(annotated_frame, info_text, (10, 40), font_size=28)

        # 显示
        cv2.imshow("YOLOv8 全屏骨骼检测", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    # 释放资源
    try:
        cv2.destroyAllWindows()
    except Exception:
        pass
    try:
        sct.close()
    except Exception:
        pass
    print("程序已退出并释放资源。")
