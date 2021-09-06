import sub

# def submethod():
#     print("서브에 있는 메서드입니다. ")
# print("this is sub")


def mainProgram():
    print("메인프로그램")
    class1=sub.Sub(10,20)
    print(class1)

    class2=sub.Sub2(100000,200000)
    print(class2)
    class2.submethod()##print("서브에 있는 메서드입니다. ")


if __name__=="__main__":##True
    print("This is main")
    mainProgram()
