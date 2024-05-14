for i in range(3, 100):
    if i % 2 == 0:
        print(i, end=' ')
        break
print("---------------")
for i in range(3, 100):
    if i % 2 == 0:
        print(f"偶数{i}", end=' ')
        continue
    if i % 2 != 0:
        print(f"奇数{i}", end=' ')
        continue
