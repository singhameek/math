import math

mode = int(input("Please choose mode: 1 for linear, 2 for simultaneous, 3 for quadratics, 4 for trigonometry, 5 for statistics \n"))


if mode == 1:
    print("Solving for ax + b = c")
    a = int(input("Value for a \n"))
    b = int(input("Value for b \n"))
    c = int(input("Value for c \n"))

    if a == 0:
        print("The coefficient = 0,",b,"=",c)
    else:
        answer = (c - b) / a
        print("x is equal to", answer)

elif mode == 2:
    print("Solving for ax + by = c and dx + ey = f")
    a = int(input("Value for a \n"))
    b = int(input("Value for b \n"))
    c = int(input("Value for c \n"))
    d = int(input("Value for d \n"))
    e = int(input("Value for e \n"))
    f = int(input("Value for f \n"))

    if a and d == 0:
        answer = c/b
        check = f/e
        if answer/check == 1:
            print("y =", answer)
        else:
            print("Could not determine, please ensure that the equations are real")
    elif b and e ==0:
        answer = a/c
        check = f/d
        if answer/check == 1:
            print("x =", answer)
        else:
            print("Could not determine, please ensure that the equations are real")