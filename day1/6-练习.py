# 练习

name = "小李"

current_price = 19.99

code_name = "10001"

number_of_growths = 1.2

day = 7

print(f"公司名{name},代码{code_name},当前价格{current_price}")
print("增长系数%f,增长天数:%d,骨架%.2f" % (number_of_growths, day, (current_price * number_of_growths ** day)))
