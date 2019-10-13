
# class A:
#     def __init__(self, b1):
#         self.a = 2
#         self._b = b1
#         print(self._b, '---')
#
#     @property
#     def b(self):
#         return self._b
#
# print(A(3).a, A(3)._b)
#
# class B(A):
#     def __init__(self, c):
#         super().__init__(c)
#         self.c = c
#     def name(self):
#         print(self.a)
#         print(self._b)
# B(4).name()
import numpy as np
data = [2,5,6,7]
data1 = [3,4,5,6]
n = np.array(data)
m = pow(n, 2)
print(m)