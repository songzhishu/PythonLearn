from ultralytics import YOLO
import cv2
import numpy as np
import dxcam
import win32gui, win32con
import time

# --- 初始化 YOLO ---
model = YOLO("yolov8n-pose.pt")

# --- 初始化 屏幕采集 (dxcam 最新版 API) ---
camera = dxcam.create()
camera.start(target_fps=30)   # 可改高，如 60，取决于显卡和 CPU

# 骨骼连接
POSE_CONNECTIONS = [
    (0,1),(0,2),(1,3),(2,4),
    (5,6),(5,7),(7,9),(6,8),(8,10),
    (11,12),(11,13),(13,15),(12,14),(14,16),
    (5,11),(6,12)
]

# --- 创建显示窗口，并设为置顶 + 透明 + 鼠标穿透 ---
window_name = "Overlay Pose"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)

hwnd = win32gui.FindWindow(None, window_name)
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
                       | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                      win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

# --- 主循环 ---
while True:
    frame = camera.get_latest_frame()
    if frame is None:
        continue

    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    result = model(frame, conf=0.4, verbose=False)[0]

    annotated = frame.copy()

    if result.keypoints is not None:
        for kpts in result.keypoints.data.cpu().numpy():
            pts = [(int(x), int(y)) if conf > 0.4 else None for x, y, conf in kpts]

            for a, b in POSE_CONNECTIONS:
                if pts[a] and pts[b]:
                    cv2.line(annotated, pts[a], pts[b], (255, 0, 0), 2)

            for p in pts:
                if p:
                    cv2.circle(annotated, p, 3, (0, 0, 255), -1)

    cv2.imshow(window_name, annotated)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.stop()
cv2.destroyAllWindows()
