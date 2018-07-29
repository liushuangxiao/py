a = 21
b = 10
c = 0
c = a + b
print("c = ", c)

c = a - b
print("c = ", c)

c = a*b
print("c = ", c)

c = a/b
print("c = ", c)

c = a % b
print("c = ", c)

# change a, b ,c
a = 2
b = 3
c = a**b
print("c = ", c)

a = 10
b = 5
c = a//b
print("c = ", c)

# 比较运算
print("a = ", a , " , b = ", b)
print("a == b :", a == b)
print("a != b :", a != b)
print("a > b :", a > b)
print("a >= b :", a >= b)
print("a < b :", a < b)
print("a <= b :", a <= b)

# 赋值
a = 2
b = 3
c = 0
print("a = ", a , " , b = ", b)
c = a + b
print("a + b :", c)
c += b
print("c += b :", c)

c -= a;
print("c -= a :", c)

c *= a;
print("c *= a :", c)

c /= a;
print("c /= a :", c)

c %= a;
print("c %= a :", c)

c **= a;
print("c **= a :", c)

c //= a;
print("c //= a :", c)

# 位运算
a = 60 # 60 =  0011 1100
       #       1100 0011
       #       1011 1101
b = 13 # 13 = 0000 1101
c = 0
c = a & b
print("a & b = ", c)
c = a | b
print("a | b = ", c)
c = a ^ b
print("a ^ b = ", c)
c = ~a
print("~a = ", c)
c = a << 2
print("a << 2 = ", c)
c = a >> 2
print("a >> 2 = ", c)

c = ~7
print("~a = ", c)