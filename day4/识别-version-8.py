from ultralytics import YOLO
import cv2
import mss
import numpy as np
import win32gui
import win32con
import win32api

# --- 1. 模型选择：用yolov8s-pose（平衡速度/精度）+ 固定输入尺寸 ---
model = YOLO("yolov8s-pose.pt")
model.conf = 0.6  # 初始置信度（过滤低精度识别）
model.iou = 0.7  # 抑制重复识别
model.imgsz = 640  # 固定输入尺寸，提升速度

sct = mss.mss()
monitor = sct.monitors[1]  # 全屏
FULL_WIDTH, FULL_HEIGHT = monitor["width"], monitor["height"]
SCALE = 0.5  # 检测画面缩小比例（50%）
DETECT_WIDTH = int(FULL_WIDTH * SCALE)
DETECT_HEIGHT = int(FULL_HEIGHT * SCALE)

POSE_CONNECTIONS = [
    (0, 1), (0, 2), (1, 3), (2, 4),
    (5, 6), (5, 7), (7, 9), (6, 8), (8, 10),
    (11, 12), (11, 13), (13, 15), (12, 14), (14, 16),
    (5, 11), (6, 12)
]

# --- 初始化画笔/画刷 ---
desktop_dc = win32gui.GetDC(0)
pen = win32gui.CreatePen(win32con.PS_SOLID, 2, win32api.RGB(80, 200, 255))  # 淡青色骨骼
brush = win32gui.CreateSolidBrush(win32api.RGB(255, 80, 80))  # 淡红色关节点
frame_count = 0  # 检测频率计数器

try:
    print("全屏骨骼标注已启动（按 Q 退出）")
    while True:
        # 2. 降低检测频率：每2帧检测1次
        frame_count += 1
        if frame_count % 2 != 0:
            continue

        # 3. 捕获全屏并缩小画面（减少计算量）
        sct_img = sct.grab(monitor)
        # 转换为OpenCV格式并缩小到50%
        frame = np.frombuffer(sct_img.rgb, dtype=np.uint8).reshape(FULL_HEIGHT, FULL_WIDTH, 3)
        frame_small = cv2.resize(frame, (DETECT_WIDTH, DETECT_HEIGHT))

        # 4. 姿态检测（小尺寸画面，速度更快）
        results = model(frame_small, verbose=False)

        # 5. 绘制骨骼（坐标放大回全屏尺寸）
        win32gui.SelectObject(desktop_dc, pen)
        win32gui.SelectObject(desktop_dc, brush)

        if results and len(results) > 0:
            result = results[0]
            if result.keypoints is not None and len(result.keypoints.data) > 0:
                for keypoints in result.keypoints.data:
                    keypoints = keypoints.cpu().numpy()
                    visible_kpts = []
                    # 关节点：坐标放大回全屏
                    for kpt_id, (x, y, conf) in enumerate(keypoints):
                        if conf > 0.6:
                            # 缩小的画面→全屏，坐标×(1/SCALE)
                            cx = int(x / SCALE)
                            cy = int(y / SCALE)
                            visible_kpts.append((cx, cy))
                            # 画稍大的关节点（更清晰）
                            win32gui.Ellipse(desktop_dc, cx - 3, cy - 3, cx + 3, cy + 3)
                    # 骨骼线：同样放大坐标
                    for (kpt1_id, kpt2_id) in POSE_CONNECTIONS:
                        if kpt1_id < len(visible_kpts) and kpt2_id < len(visible_kpts):
                            x1, y1 = visible_kpts[kpt1_id]
                            x2, y2 = visible_kpts[kpt2_id]
                            win32gui.MoveToEx(desktop_dc, x1, y1)
                            win32gui.LineTo(desktop_dc, x2, y2)

        # 6. 退出提示
        win32gui.SetBkColor(desktop_dc, win32api.RGB(0, 0, 0))
        win32gui.SetTextColor(desktop_dc, win32api.RGB(255, 255, 255))
        win32gui.DrawText(desktop_dc, "按 Q 退出", -1, (FULL_WIDTH - 120, 10, FULL_WIDTH, 35), win32con.DT_CENTER)

        # 7. 按Q退出
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