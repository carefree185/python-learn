# 创建一个整形变量
number_int = 10  # 等价于 number_int = int(10)
print(number_int)
# 创建一个浮点型变量
number_float = 3.14  # 等价于 number_float = float(3.14)
print(number_float)
# 创建一个复数变量
number_complex = 3 + 4j  # 等价于 number_complex = complex(3, 4)
number_complex_real = number_complex.real  # 获取实部
number_complex_imag = number_complex.imag  # 获取虚部
print(number_complex, number_complex_real, number_complex_imag)
# 算术运算
add = 3 + 5  # 加法
minus = 5 - 2  # 减法
multiply = 5 * 3  # 乘法
division = 5 / 2  # 除法
floor_division = 5 // 2 # 整数除法, 返回真实值的整数部分
power = 2 ** 3  # 幂运算
print(add, minus, multiply, division, floor_division, power)
