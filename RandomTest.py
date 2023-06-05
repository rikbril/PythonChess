def test1():
    a = [3, 1]
    b = [3, 6]
    diff = None

    if a[0] != b[0]:
        diff = abs(a[0] - b[0])
    else:
        diff = abs(a[1] - b[1])

    if a[1] < b[1]:
        print("AAAA")

    for x in range(1, diff):
        print(x)        

def test2():
    a = -4
    b = a - (a * 2)
    print(b)





if __name__ == "__main__":
    test1()
    test2()
    pass