
class A:
    def __init__(self):
        self.a = 2


print(A().a)


class B(A):
    def __init__(self):
        super().__init__()
        self.c = 2

    def name(self, b):
        print(self.a)
        print(self.c + self.a + b)
B().name(5)


class C(B):
    def __init__(self):
        super(B, self).__init__()
        self.a1 = 4
        print("c", self.a1, self.a)

C()
# import numpy as np
# data = [2,5,6,7]
# data1 = [3,4,5,6]
# n = np.array(data)
# m = pow(n, 2)
# print(m)