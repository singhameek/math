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
    elif b and e == 0:
        answer = a/c
        check = f/d
        if answer/check == 1:
            print("x =", answer)
        else:
            print("Could not determine, please ensure that the equations are real")
    else:
       determinant = (a*e) - (b*d) ##Cramer's Rule

       if determinant == 0:
           print("Could not solve, ensure equations are real")

       else:
           x = ((c*e)-(b*f))/determinant
           y=((a*f)-(c*d))/determinant
           print("x equals", x, "and y equals", y)

elif mode == 3:
    print("Solving for ax**2 + bx + c = 0")
    a = int(input("Value of a \n"))
    b = int(input("Value of b \n"))
    c = int(input("Value of c \n"))

    x1 = (-b + ((b**2)-(4*a*c))**0.5)/(2*a)
    x2 = (-b - ((b**2)-(4*a*c))**0.5)/(2*a)

    print("The roots are",x1,"and",x2)


elif mode == 4:
    func = int(input("Select trig function: 1 for sine, 2 for cosine, 3 for tangent, 4 for arcsine, 5 for arccosine, 6 for arctangent \n"))
    x = float(input("Value to calculate: use a degree value for regular functions and decimal for arc functions. Don't include units. \n"))

    if func == 1:
        print(math.sin(x))
    elif func == 2:
        print(math.cos(x))
    elif func == 3:
        print(math.tan(x))
    elif func == 4:
        print(math.asin(x))
    elif func == 5:
        print(math.acos(x))
    elif func == 6:
        print(math.atan(x))