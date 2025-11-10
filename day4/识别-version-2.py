from ultralytics import YOLO
import cv2
import time
import mss
import numpy as np
from screeninfo import get_monitors

# --- 自动获取屏幕分辨率 ---
def get_screen_resolution():
    monitors = get_monitors()
    primary_monitor = monitors[0]
    return primary_monitor.width, primary_monitor.height

# --- 初始化 ---
# 1. 加载 YOLOv8 姿态模型（轻量版兼顾速度）
model = YOLO("yolov8n-pose.pt")

# 2. 自动获取屏幕参数
screen_width, screen_height = get_screen_resolution()
print(f"屏幕分辨率：{screen_width}x{screen_height}")

# 3. 屏幕捕获配置（居中捕获 1000x800 区域，扩大视野）
sct = mss.mss()
capture_width = 1000
capture_height = 800
monitor = {
    "top": (screen_height - capture_height) // 2,
    "left": (screen_width - capture_width) // 2,
    "width": capture_width,
    "height": capture_height
}

# 帧率计算变量
pTime = 0

# 骨骼连接定义（YOLOv8 17个关键点的标准连接）
POSE_CONNECTIONS = [
    (0, 1), (0, 2), (1, 3), (2, 4),  # 面部
    (5, 6), (5, 7), (7, 9), (6, 8), (8, 10),  # 上肢
    (11, 12), (11, 13), (13, 15), (12, 14), (14, 16),  # 下肢
    (5, 11), (6, 12)  # 躯干
]

# --- 主循环：捕获+检测+实时标注 ---
while True:
    # 1. 捕获屏幕帧
    sct_img = sct.grab(monitor)
    frame = np.array(sct_img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    if frame is None:
        continue

    # 2. YOLOv8 姿态检测
    results = model(frame, verbose=False, conf=0.5)
    annotated_frame = frame.copy()

    # 3. 实时绘制骨骼框架
    if results and len(results) > 0:
        result = results[0]
        if result.keypoints is not None and len(result.keypoints.data) > 0:
            # 遍历每个人
            for person_idx, keypoints in enumerate(result.keypoints.data):
                keypoints = keypoints.cpu().numpy()
                h, w, _ = frame.shape

                # 存储可见的关节点（置信度>0.5）
                visible_kpts = []
                for kpt_id, (x, y, conf) in enumerate(keypoints):
                    if conf > 0.5:
                        cx, cy = int(x), int(y)
                        visible_kpts.append((kpt_id, cx, cy))
                        # 绘制关节点（红色实心圆，半径4）
                        cv2.circle(annotated_frame, (cx, cy), 4, (0, 0, 255), cv2.FILLED)
                        # 标注关节点ID（白色文字）
                        cv2.putText(annotated_frame, str(kpt_id), (cx+5, cy-5),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

                # 绘制骨骼连接（蓝色粗线，线宽3）
                for (kpt1_id, kpt2_id) in POSE_CONNECTIONS:
                    # 查找两个关节点是否可见
                    kpt1 = next((k for k in visible_kpts if k[0] == kpt1_id), None)
                    kpt2 = next((k for k in visible_kpts if k[0] == kpt2_id), None)
                    if kpt1 and kpt2:
                        cv2.line(annotated_frame, (kpt1[1], kpt1[2]), (kpt2[1], kpt2[2]),
                               (255, 0, 0), 3)

                # 打印关键坐标（可选，不影响标注）
                print(f"\n=== 第 {person_idx + 1} 个人 ===")
                nose = next((k for k in visible_kpts if k[0] == 0), None)
                if nose:
                    screen_x = nose[1] + monitor["left"]
                    screen_y = nose[2] + monitor["top"]
                    print(f"鼻子坐标：区域({nose[1]},{nose[2]}) | 屏幕({screen_x},{screen_y})")

    # 4. 显示帧率和捕获区域信息
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    info_text = f"FPS: {int(fps)} | 捕获区域: {capture_width}x{capture_height}"
    cv2.putText(annotated_frame, info_text, (10, 50),
               cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)

    # 5. 显示标注结果（窗口可拖动）
    cv2.imshow("YOLOv8 实时骨骼标注", annotated_frame)

    # 按 'q' 退出
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# --- 释放资源 ---
cv2.destroyAllWindows()
sct.close()
print("程序退出，资源已释放")