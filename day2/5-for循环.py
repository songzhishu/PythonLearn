for i in range(1, 10):
    j = 1
    for j in range(1, i + 1):
        print(i, '*', j, '=', i * j, end='\t')
        j += 1
    print()

# 统计文本中单词出现的次数
txt = "I love python I love python"
count = 0
for x in txt:
    if x == 'o':
        count += 1
print(count)
