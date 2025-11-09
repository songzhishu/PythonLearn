import pyautogui

# 1. 鼠标移动到指定位置
print("移动鼠标到 (100, 200)...")
pyautogui.moveTo(100, 200)
print("已移动鼠标到 (100, 200)")

# 2. 鼠标点击
print("在当前位置点击鼠标左键...")
pyautogui.click()

print("在 (500, 500) 位置点击鼠标左键...")
pyautogui.click(500, 500)

print("双击鼠标左键，在 (200, 200) 位置...")
pyautogui.doubleClick(200, 200)

# 3. 鼠标拖动
print("从当前位置拖动到 (500, 500)...")
pyautogui.dragTo(500, 500, duration=2)

print("从 (100, 100) 拖动到 (300, 300)...")
pyautogui.moveTo(100, 100)
pyautogui.mouseDown()
pyautogui.move(200, 200)
pyautogui.mouseUp()

# 4. 鼠标滚动
print("向上滚动 500 单位...")
pyautogui.scroll(500)

print("向下滚动 500 单位...")
pyautogui.scroll(-500)

# 5. 移动并点击一段时间后再点击
print("移动到 (300, 300)，然后点击...")
pyautogui.moveTo(300, 300, duration=1)
pyautogui.click()

# 6. 相对移动鼠标
print("相对当前位置移动鼠标 (200, 100)...")
pyautogui.move(200, 100)

# 7. 获取屏幕分辨率和当前鼠标位置
screen_width, screen_height = pyautogui.size()
print(f"屏幕分辨率：{screen_width}x{screen_height}")

current_x, current_y = pyautogui.position()
print(f"当前鼠标位置：{current_x}, {current_y}")

# 8. 快速定位和拖动鼠标
print("快速移动到屏幕中心...")
pyautogui.moveTo(screen_width // 2, screen_height // 2)

print("拖动鼠标到屏幕右下角...")
pyautogui.dragTo(screen_width - 100, screen_height - 100, duration=2)

print("所有操作完成！")
