import sympy


# 定义变量
a, pc, c, e, u, t, m = sympy.symbols('a, pc, c, e, u, t, m')

f = -(a*pc - c*pc - a*t + c*t + e*pc**2 - e*(pc**2)*u + c*pc*u - e*pc*t - c*t*u + e*pc*t*u)/(- e*pc**2 + 2*e*pc*t - e*t**2 + 2*e*m)

# 化简
f_s = sympy.simplify(f)
# 提取公因式
f_s = sympy.factor(f_s)

# 手写输出
sympy.pprint(f_s)