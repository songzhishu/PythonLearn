# while循环

# 计算1到100的和
sum = 0
num = 1
while num <= 100:
    sum += num
    num += 1

print("1到100的和为:", sum)

# 计算1到100的乘积
product = 1
num = 1
while num <= 100:
    product *= num
    num += 1

print("1到100的乘积为:", product)

# 用python计算1到100的阶乘的和
factorial = 1
k = 0
num = 1
while num <= 100:
    factorial *= num
    k += factorial
    num += 1

print("1到100的阶乘的和为:", k)


