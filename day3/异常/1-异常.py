# 异常处理
try:
    open("a.txt", "r", encoding="utf-8")
except:
    print("文件打开失败")

