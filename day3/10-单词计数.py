# 打开文件
t = open('D:/PythonProject/PythonLearn/day3/file/word.txt', 'r', encoding='utf-8')


def word_count(file):
    # 读取文件内容
    global count
    readlines = file.readlines()
    # 得到每一行的数据
    sum = 0
    for i in readlines:
        count = i.count("for")
        sum += count
    return sum


count = 0
for line in t:
    # 去除换行符
    line = line.strip()
    line_split = line.split(" ")
    print(line_split)
    for word in line_split:
        if word == "for":
            count += 1
print(count)
