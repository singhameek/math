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