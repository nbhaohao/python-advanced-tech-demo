from collections.abc import Iterator


class Company(object):
    def __init__(self, employee_list):
        self.employee_list = employee_list

    def __getitem__(self, index):
        return self.employee_list[index]




if __name__ == '__main__':
    company = Company(["tom", "bob", "jane"])
    # 虽然我们这里没有实现 __iter__, 但这里会默认给它一个迭代器, 并且调用 __getitem__ 方法.
    my_iter = iter(company)
    # while True:
    #     try:
    #         result = next(my_iter)
    #         print(result)
    #     except StopIteration:
    #         break

    # for-in 帮我们处理了上面的捕获异常的逻辑.
    for employee in company:
        print(employee)
