# 捕获指定异常
try:
    # 可能会引发异常的代码
    # 例如，尝试打开一个不存在的文件
    f = open("file.txt")
    # 假设我们想要捕获FileNotFoundError异常
except FileNotFoundError:
    # 处理FileNotFoundError异常的代码
    print("文件不存在，请检查路径。")
# 如果没有异常发生，except子句在try子句执行完毕后不会被执行
# 如果没有异常发生，下面的代码会继续执行
print("文件操作完成。")

# 捕获多个异常
try:
    # 可能会引发异常的代码
    # 例如，尝试打开一个不存在的文件
    f = open("file.txt")
    # 假设我们想要捕获FileNotFoundError和IOError异常
except (FileNotFoundError,IOError):
    # 处理FileNotFoundError和IOError异常的代码
    print("文件不存在，请检查路径。")
# 如果没有异常发生，except子句在try子句执行完毕后不会被执行
# 如果没有异常发生，下面的代码会继续执行
print("文件操作完成。")

