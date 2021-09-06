class Sub:
    a=0
    b=0
    def __init__(self, a,b):
        self.a = a
        self.b=b
    def __repr__(self):
        return f"SUB1 :: a:{self.a}, b:{self.b} fxxk "


class Sub2:
    aa=0
    bb=0
    def __init__(self, a,b):
        self.a = a
        self.b=b
    def __repr__(self):
        return f"SUB2 :: a:{self.a}, b:{self.b} "
    def submethod(self):
        print("서브에 있는 메서드입니다. ")




if __name__=='__main__':
    print("서브가 메인으로 실행되었어!")
# else:
#     print("서브는 서브야")