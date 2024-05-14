word = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

# 方法一
for i in range(len(word)):
    print(word[i], end=' ')

print()
# 方法二
i = 0
while i < len(word):
    print(word[i], end=' ')
    i += 1

print()
for e in word:
    print(e, end=' ')
