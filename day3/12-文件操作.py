# 读取
t = open('D:\PythonProject\PythonLearn\day3/file\测试.txt', 'r', encoding='utf-8')

# 写入
f = open('D:\PythonProject\PythonLearn\day3/file\测试_bat.txt', 'w', encoding='utf-8')

# 读取
for line in t:
    line = line.strip()
    split = line.split(",")
    if split[4] == '正式':
        # 复制数据
        f.write(line + "\n")

f.close()
t.close()