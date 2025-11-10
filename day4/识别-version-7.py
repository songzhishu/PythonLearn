from ultralytics import YOLO
import cv2
import mss
import numpy as np
import win32gui
import win32con
import win32api

# --- 初始化配置 ---
model = YOLO("yolov8n-pose.pt")  # 轻量模型保证流畅
sct = mss.mss()
monitor = sct.monitors[1]  # 主屏幕全屏
width, height = monitor["width"], monitor["height"]
POSE_CONNECTIONS = [  # 骨骼连接
    (0, 1), (0, 2), (1, 3), (2, 4),
    (5, 6), (5, 7), (7, 9), (6, 8), (8, 10),
    (11, 12), (11, 13), (13, 15), (12, 14), (14, 16),
    (5, 11), (6, 12)
]

# --- 核心：获取桌面DC，创建画笔/画刷 ---
desktop_dc = win32gui.GetDC(0)
pen = win32gui.CreatePen(win32con.PS_SOLID, 2, win32api.RGB(100, 150, 255))  # 淡蓝色2px线条
brush = win32gui.CreateSolidBrush(win32api.RGB(255, 100, 100))  # 淡红色画刷

try:
    print(f"已启动全屏骨骼标注（按 Q 退出）")
    while True:
        # 1. 捕获全屏画面
        sct_img = sct.grab(monitor)
        frame = np.frombuffer(sct_img.rgb, dtype=np.uint8).reshape(height, width, 3)

        # 2. 姿态检测
        results = model(frame, verbose=False, conf=0.5, iou=0.6)

        # 3. 绑定画笔/画刷
        win32gui.SelectObject(desktop_dc, pen)
        win32gui.SelectObject(desktop_dc, brush)

        # 4. 绘制骨骼
        if results and len(results) > 0:
            result = results[0]
            if result.keypoints is not None and len(result.keypoints.data) > 0:
                for keypoints in result.keypoints.data:
                    keypoints = keypoints.cpu().numpy()
                    visible_kpts = []
                    # 画关节点（淡红色小圆圈）
                    for kpt_id, (x, y, conf) in enumerate(keypoints):
                        if conf > 0.5:
                            cx, cy = int(x), int(y)
                            visible_kpts.append((cx, cy))
                            win32gui.Ellipse(desktop_dc, cx-2, cy-2, cx+2, cy+2)
                    # 画骨骼线（修正MoveToEx参数）
                    for (kpt1_id, kpt2_id) in POSE_CONNECTIONS:
                        if kpt1_id < len(visible_kpts) and kpt2_id < len(visible_kpts):
                            x1, y1 = visible_kpts[kpt1_id]
                            x2, y2 = visible_kpts[kpt2_id]
                            win32gui.MoveToEx(desktop_dc, x1, y1)  # 去掉第四个None参数
                            win32gui.LineTo(desktop_dc, x2, y2)

        # 5. 画退出提示
        info_text = "按 Q 退出"
        win32gui.SetBkColor(desktop_dc, win32api.RGB(0, 0, 0))
        win32gui.SetTextColor(desktop_dc, win32api.RGB(255, 255, 255))
        win32gui.DrawText(desktop_dc, info_text, -1, (width-120, 10, width, 35), win32con.DT_CENTER)

        # 6. 按Q退出
        if win32api.GetAsyncKeyState(ord('Q')) & 0x8000:
            break

except Exception as e:
    print(f"异常：{e}")

finally:
    # 释放资源+刷新桌面
    win32gui.DeleteObject(pen)
    win32gui.DeleteObject(brush)
    win32gui.ReleaseDC(0, desktop_dc)
    sct.close()
    win32gui.RedrawWindow(0, None, None, win32con.RDW_INVALIDATE | win32con.RDW_ALLCHILDREN | win32con.RDW_ERASE)
    print("已退出，桌面已刷新")