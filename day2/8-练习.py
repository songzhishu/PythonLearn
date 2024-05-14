import random

money = 10000

for i in range(1, 21):
    score = random.randint(1, 10)
    if money < 1000:
        print(f"剩余工资{money}元，工资扣光，无法发工资")
        break
    elif score <= 5:
        print(f"第{i}个员工，得分：{score},评分低不发工资")
        continue
    elif score >= 6:
        money -= 1000
        print(f"第{i}个员工，得分：{score},扣工资{score}元，剩余工资{money}元")
        continue

