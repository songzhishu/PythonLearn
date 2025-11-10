from ultralytics import YOLO
import cv2
import time
import mss
import numpy as np
from screeninfo import get_monitors

# 自动获取屏幕分辨率（仅用于显示信息）
def get_screen_resolution():
    monitors = get_monitors()
    primary_monitor = monitors[0]
    return primary_monitor.width, primary_monitor.height

# --- 初始化 ---
# 1. 加载 YOLOv8 轻量姿态模型
model = YOLO("yolov8n-pose.pt")

# 2. 获取屏幕信息
screen_width, screen_height = get_screen_resolution()
print(f"当前屏幕分辨率：{screen_width}x{screen_height}（已设置全屏捕获）")

# 3. 屏幕捕获配置（关键：设置为全屏）
sct = mss.mss()
monitor = sct.monitors[1]  # 1 = 主屏幕全屏，0 = 虚拟桌面（多屏合并）

# 帧率计算变量
pTime = 0

# YOLOv8 标准骨骼连接
POSE_CONNECTIONS = [
    (0, 1), (0, 2), (1, 3), (2, 4),  # 面部
    (5, 6), (5, 7), (7, 9), (6, 8), (8, 10),  # 上肢
    (11, 12), (11, 13), (13, 15), (12, 14), (14, 16),  # 下肢
    (5, 11), (6, 12)  # 躯干
]

# --- 主循环：全屏捕获+实时骨骼标注 ---
while True:
    # 1. 捕获全屏画面
    sct_img = sct.grab(monitor)
    frame = np.array(sct_img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)  # BGRA转BGR（适配OpenCV）
    if frame is None:
        continue

    # 2. YOLOv8 姿态检测（降低置信度阈值，提升检测灵敏度）
    results = model(frame, verbose=False, conf=0.4)
    annotated_frame = frame.copy()

    # 3. 实时绘制骨骼框架（优化性能：线条变细、关节点缩小）
    if results and len(results) > 0:
        result = results[0]
        if result.keypoints is not None and len(result.keypoints.data) > 0:
            for person_idx, keypoints in enumerate(result.keypoints.data):
                keypoints = keypoints.cpu().numpy()
                visible_kpts = []

                # 绘制关节点（半径3，红色实心）
                for kpt_id, (x, y, conf) in enumerate(keypoints):
                    if conf > 0.4:
                        cx, cy = int(x), int(y)
                        visible_kpts.append((kpt_id, cx, cy))
                        cv2.circle(annotated_frame, (cx, cy), 3, (0, 0, 255), cv2.FILLED)
                        # 可选：隐藏关节点ID（全屏下文字过密）
                        # cv2.putText(annotated_frame, str(kpt_id), (cx+3, cy-3),
                        #            cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)

                # 绘制骨骼线（线宽2，蓝色）
                for (kpt1_id, kpt2_id) in POSE_CONNECTIONS:
                    kpt1 = next((k for k in visible_kpts if k[0] == kpt1_id), None)
                    kpt2 = next((k for k in visible_kpts if k[0] == kpt2_id), None)
                    if kpt1 and kpt2:
                        cv2.line(annotated_frame, (kpt1[1], kpt1[2]), (kpt2[1], kpt2[2]),
                               (255, 0, 0), 2)

                # 打印第一个人的鼻子坐标（全屏绝对坐标）
                nose = next((k for k in visible_kpts if k[0] == 0), None)
                if nose:
                    print(f"第 {person_idx + 1} 人 - 鼻子全屏坐标：({nose[1]},{nose[2]})")

    # 4. 显示帧率和退出提示（位置调整到屏幕左上角，不遮挡关键内容）
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    info_text = f"FPS: {int(fps)} | 全屏捕获 | 按 'q' 键退出"
    cv2.putText(annotated_frame, info_text, (10, 40),
               cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

    # 5. 显示标注结果（窗口可最大化，适配全屏）
    cv2.imshow("YOLOv8 全屏实时骨骼标注", annotated_frame)

    # 按 'q' 键退出（聚焦窗口后按下）
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# --- 释放资源 ---
cv2.destroyAllWindows()
sct.close()
print("程序已退出，全屏捕获资源已释放")
