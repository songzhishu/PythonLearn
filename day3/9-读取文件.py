fileurl = "D:/PythonProject/PythonLearn\day3/file/测试.txt"
type_ = "r"
encoding = "utf-8"
f = open(fileurl, type_, encoding=encoding)

# print(f.read(10))

# readline = f.readlines()
# print(readline)
# f.close()


# 读取文件 读取完关闭资源
with open(fileurl, type_, encoding=encoding) as f:
    for line in f.readlines():
        print(line)
