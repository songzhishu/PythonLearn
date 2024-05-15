employee_info = {
    "001":
        {
            "姓名": "张三",
            "部门": "技术部",
            "职位": "工程师",
            "基本工资": 5000,
            "级别": 1,
        },
    "002":
        {
            "姓名": "李四",
            "部门": "市场部",
            "职位": "销售员",
            "基本工资": 3000,
            "级别": 1,
        },
    "003":
        {
            "姓名": "王五",
            "部门": "财务部",
            "职位": "会计",
            "基本工资": 4000,
            "级别": 1,
        },
    "004":
        {
            "姓名": "赵六",
            "部门": "技术部",
            "职位": "工程师",
            "基本工资": 5000,
            "级别": 2,
        },
    "005":
        {
            "姓名": "钱七",
            "部门": "市场部",
            "职位": "销售员",
            "基本工资": 3000,
            "级别": 2,
        }
}


# 员工信息字典

def calculate_salary():
    for employee_id in employee_info:
        if employee_info[employee_id]["级别"] == 1:
            employee_info[employee_id]["基本工资"] += 1000
            employee_info[employee_id]["级别"] += 1
    return employee_info


salary = calculate_salary()
print(salary)
