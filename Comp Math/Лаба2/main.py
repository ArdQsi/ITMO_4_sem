import numpy as np
import matplotlib.pyplot as plt
from sympy import *
import sys

FILE_IN = "files/input.txt"
FILE_OUT = "files/output.txt"
x = Symbol('x')
y = Symbol('y')

def checkQuantityOfRoots(function, a, b):
    # Проверка на количество корней в указаном промежутке
    roots = 0
    epsilon = 0.01
    for i in np.arange(a, b, epsilon):
        if (function.subs(x, i) * function.subs(x, i+epsilon) < 0):
            roots += 1
    return roots


def halfDivision_method(a, b, function, error):
    # Метод половинного деления
    counter = 0
    middle = (a + b) / 2
    counter += 1

    while (abs(a - b) > error or abs(function.subs(x, middle)) > error):
        a = a if function.subs(x, a) * function.subs(x, middle) < 0 else middle
        b = b if function.subs(x, b) * function.subs(x, middle) < 0 else middle
        middle = (a + b) / 2
        counter += 1
  
    return middle, function.subs(x, middle), counter

def secant_method(a, b, function, error):
    # Метод секущих 
    secondDerivative = secondDiff(function, x)
    if function.subs(x, a) * secondDerivative.subs(x, a) > 0:
        x0 = a
    else: 
        x0 = b

    x1 = x0 + (b-a)/2
    x2 = x1 - (((x1 - x0) / (function.subs(x, x1) - function.subs(x, x0))) * function.subs(x, x1))
    itr = 0
    while ((abs(x2 - x1) > error or abs(function.subs(x,x2)) > error) and itr < 1000):
        x0 = x1
        x1 = x2
        x2 =  x1 - (((x1 - x0) / (function.subs(x, x1) - function.subs(x, x0))) * function.subs(x, x1))
        itr += 1

    return x2, function.subs(x, x2), itr

def iteration_method(a, b, function, error):
    # Метод простой итерации 
    counter = 0

    firstDerivative = firstDiff(function, x)
    if (abs(firstDerivative.subs(x, a)) > abs(firstDerivative.subs(x, b))):
        x0 = a
    else:
        x0 = b

    k = -1 / firstDerivative.subs(x, x0)

    phi = x + k * function
    x1 = phi.subs(x, x0)
    x1Derivative = x1.diff(x)
    # проверка на достаточное условие сходимости метода
    check = abs(x1Derivative.subs(x, a)) < 1 and abs(x1Derivative.subs(x, b)) < 1

    
    while ((abs(x1 - x0) > error or abs(function.subs(x, x1)) > error) and counter < 1000):
        x0 = x1
        x1 = phi.subs(x, x0)
        counter += 1
    print(function.subs(x, x1))

    return x1, function.subs(x, x1), counter, check

def draw(function, coordx, a, b):
    # Отрисовать график для нелинейных уравнений
    plot_range = [ii/100 for ii in np.arange((a-1)*100, (b+1)*100)]
    y = [function.subs(x, ii) for ii in plot_range]
    plt.plot(plot_range, y)
    plt.xlabel(r'$x$')
    plt.ylabel(r'$f(x)$')
    plt.grid(True)
    plt.scatter(coordx, 0)
    plt.show()


def getfunc(function_num):
    # Получить выбранную функцию 
    if function_num == '1':
        return x**3 + 2.28 * x**2 - 1.934 * x - 3.907
    elif function_num == '2':
        return x**3 - x + 4
    elif function_num == '3':
        return sin(x) + 0.1
    elif function_num == '4':
        return exp(x) * sin(x)
    elif function_num == '5':
        return x**4 + 4 * x**3 - 22 * x**2 - 100 * x - 75
    else:
        return None 

def getsystem(function_num):
    # получить выбранную систему
    if function_num == '1':
        return [x**2 + y**2 - 4, y-3*x**2]
    elif function_num == '2':
        return [y + sin(x) - 1, 2*y + sin(x) - 2]
    elif function_num == '3':
        return [(x + 2*y)*(2*x - y + 1) - 6,  (2*x - y + 1)/(x + 2*y) - 2/3]
    else:
        return None
    
def firstDiff(equation, symbol):
    #Первая производная
    return diff(equation, symbol)

def secondDiff(equation, sybmol):
    #Вторая производная
    return diff(firstDiff(equation, sybmol))

def newtonMethod(f, g, x0, y0, epsilon):
    #метод Ньютона для системы нелинейных уравнений
    jacobi_matrix = [[firstDiff(f, x) , firstDiff(f, y)],
        [firstDiff(g, x) , firstDiff(g, y)]]
    dx = Symbol("dx")
    dy = Symbol("dy")

    first = jacobi_matrix[0][0] * dx + jacobi_matrix[0][1] * dy + f
    second = jacobi_matrix[1][0] * dx + jacobi_matrix[1][1] * dy + g

    iter = 0
    vector_errors_x = []
    vector_errors_y = []

    while (True):
        newSystem = [first.subs([(x, x0), (y, y0)]),
                     second.subs([(x, x0), (y, y0)])]
        
        try:
            solutions = linsolve(newSystem, (dx, dy)).args[0]
        except IndexError:
            return None

        x1 = x0 + solutions[0]
        y1 = y0 + solutions[1]
        iter+=1
        vector_errors_x.append(abs(x1 - x0))
        vector_errors_y.append(abs(y1 - y0))
        if (abs(x1 - x0) <= epsilon and abs(y1 - y0) <= epsilon):
            break
        x0 = x1
        y0 = y1
    
    return x0, y0, iter, vector_errors_x, vector_errors_y

def getPlotBefore(function1, function2):
    #нарисовать график для системы нелинейных уравнений для выбора точки
    plot1 = plot_implicit(function1, aspect_ratio=(1, 1), show=False, line_color="blue")
    plot2 = plot_implicit(function2, aspect_ratio=(1,1), show=False, line_color="red")
    plot1.append(plot2[0])
    plot1.show()

def getPlot(x, y, function1, function2):
    #нарисовать график для системы нелинейных уравнений
    plot1 = plot_implicit(function1, aspect_ratio=(1, 1), show=False, line_color="blue",
                          markers=[{'args': [x, y], 'color': "black", 'marker': "o", 'ms': 5}])
    plot2 = plot_implicit(function2, aspect_ratio=(1,1), show=False, line_color="red")
    plot1.append(plot2[0])
    plot1.show()

def printErrorAnswer(data, answer):
    if (data['out'] == "консоль"):
        print("\n" + answer)
    else:
        file = open(FILE_OUT, "w",encoding="utf8")
        file.write("\n" + answer)

def getdata_file():
    # Получить данные из файла
    with open(FILE_IN, 'rt', encoding="utf-8") as fin:
        try:
            data = {}

            task = fin.readline().strip()
            if not(task == "уравнение" or task == "система" or task == "систему"):
                print("Ошибка в 1 строке. Неправильно указано, что вы хотите решить.")
                raise AttributeError            
            data['task'] = task

            if(data['task'] == "уравнение"):
                function_data = getfunc(fin.readline().strip())
                if function_data is None:
                    print("Ошибка во 2 строке. Такой функции нет.")
                    raise ValueError
                data['function'] = function_data

                method = fin.readline().strip()
                if (method != '1') and (method != '2') and (method != '3'):
                    print("Ошибка в 3 строке. Неправильно указан метод.")
                    raise ValueError
                data["method"] = method

                a, b = map(float, fin.readline().strip().split())
                if a > b:
                    a, b = b, a
                elif a == b:
                    print("Ошибка в 4 строке. Границы интервала не могут быть равны.")
                    raise ArithmeticError
                if (checkQuantityOfRoots(function_data, a, b) > 1 or checkQuantityOfRoots(function_data, a, b) == 0):
                    print("Ошибка в 4 строке. Интервал содержит ноль или несколько корней.")
                    raise AttributeError
                data['a'] = a
                data['b'] = b

                error = float(fin.readline().strip())
                if error < 0:
                    print("Ошибка в 5 строке. Погрешность вычисления должна быть положительным числом.")
                    raise ArithmeticError
                data['error'] = error

                out = fin.readline().strip()
                if not(out == "файл" or out == "консоль"):
                    print("Ошибка в 6 строке. Неправильно указан способ вывода результата работы")
                    raise AttributeError
                data['out'] = out  

            else:
                function_data = getsystem(fin.readline().strip())
                if function_data is None:
                    print("Ошибка во 2 строке. Такой системы нет.")
                    raise ValueError
                data['system'] = function_data

                try: 
                    x0, y0 = map(float, fin.readline().strip().split())
                except ValueError:
                    print("Ошибка в 3 строке. Неправильно указано начальное приближени(x и y)")
                    raise ValueError
                data['x0'] = x0
                data['y0'] = y0

                error = float(fin.readline().strip())
                if error < 0:
                    print("Ошибка в 4 строке. Погрешность вычисления должна быть положительным числом.")
                    raise ArithmeticError
                data['error'] = error

                out = fin.readline().strip()
                if not(out == "файл" or out == "консоль"):
                    print("Ошибка в 5 строке. Неправильно указан способ вывода результата работы")
                    raise AttributeError
                data['out'] = out  

            return data
        except (ValueError, ArithmeticError, AttributeError):
            return None



def getdata_input():
    # Получить данные с клавиатуры
    data = {}

    print("Что вы хотите решить? (уравнение / систему)")
    choice = input("")
    while(choice != 'уравнение' and choice != 'систему'):
        print("Решить (уравнение / систему)")
        choice = input("")
    data['task'] = choice
    if (choice == "систему"):   
        print("\nВыберите систему уравнения")
        print("1: x^2 + y^2 - 4 = 0;  y = 3 * x^2")
        print("2: y + sin(x) - 1 = 0; 2y + sin(x) - 2= 0")
        print("3: (x + 2y)(2x - y + 1) - 6 = 0;  (2x - y + 1)/(x + 2y) - 2/3 = 0")
        system_data = getsystem(input("Система: "))
        while system_data is None:
            print("Выберите систему")
            system_data = getsystem(input("Система: "))
        data['system'] = system_data

        getPlotBefore(data['system'][0],data['system'][1])

        print("\nВыберите начальное приближение(x и y)")
        while True:
            try:
                x0, y0 = map(float, input("Начальное приближение: ").replace(",",".").split(" "))
                break
            except ValueError:
                print("Начальное приближение должно быть числом.")
        data['x0'] = x0
        data['y0'] = y0

        print("\nВыберите погрешность вычисления")
        while True:
            try:
                error = float(input("").replace(",", "."))
                if error <= 0:
                    raise ArithmeticError
                break
            except (ValueError, ArithmeticError):
                print("Погрешность вычисления должна быть положительным числом")
        data['error'] = error
    else: 
        print("\nВыберите функцию.")
        print("1: x^3 + 2.28x^2 - 1.934x - 3.907")
        print("2: x^3 - x + 4")
        print("3: sin(x) + 0.1")
        print("4: e^x * sin(x)")
        print("5: x^4 + 4x^3 - 22x^2 - 100x - 75")
        function_data = getfunc(input("Функция: "))
        while function_data is None:
            print("Выберите функцию")
            function_data = getfunc(input("Функция: "))
        data['function'] = function_data

        print("\nВыберите метод решения.")
        print("1: Метод половинного деления")
        print("2: Метод секущих")
        print("3: Метод простой итерации")
        method = input("")
        while (method != '1') and (method != '2') and (method != '3'):
            print("Выберите метод решения")
            method = input("")
        data['method'] = method

        print("\nВведите границы интервала через пробел(Например: 1 2)")
        while True:
            try:            
                a, b = map(float, input("").split())
                if a > b:
                    print('\nГраницы указываются в порядке возрастания. Ладно... Не утруждайся:)')
                    a, b = b, a
                elif a == b:
                    raise ArithmeticError
                if checkQuantityOfRoots(function_data, a, b) > 1 or checkQuantityOfRoots(function_data, a, b) == 0:
                    raise AttributeError
                break
            except ValueError:
                print("Границы интервала должны быть числами, введенными через пробел.")
            except ArithmeticError:
                print("Границы интервала не могут быть равны.")
            except AttributeError:
                print("Интервал содержит ноль или несколько корней.")
        data['a'] = a
        data['b'] = b

        print("\nВыберите погрешность вычисления")
        while True:
            try:
                error = float(input(""))
                if error <= 0:
                    raise ArithmeticError
                break
            except (ValueError, ArithmeticError):
                print("Погрешность вычисления должна быть положительным числом")
        data['error'] = error
        
    print("\nКуда вывести результат работы в файл(файл) или в консоль(консоль)?")
    inchoice = input("")
    while (inchoice != 'файл') and (inchoice != 'консоль'):
        print("Введите 'файл' или 'консоль' для выбора способа вывода результата работы")
        inchoice = input("")
    data['out'] = inchoice    

    return data

def main():
    print("Лабораторная работа #2 (7)")
    print("Численное решение нелинейных уравнений и систем")

    print("\nВзять исходные данные из файла (файл) или ввести с клавиатуры (консоль)?")
    inchoice = input("")
    while (inchoice != 'файл') and (inchoice != 'консоль'):
        print("Введите 'файл' или 'консоль' для выбора способа ввода")
        inchoice = input("")

    if inchoice == 'файл':
        data = getdata_file()
        if data is None:
            sys.exit()
    else:
        data = getdata_input()
    try:
        answer = None
        if data['task'] == 'уравнение':
            if data['method'] == '1':
                answer = halfDivision_method(data['a'], data['b'], data['function'], data['error'])
            elif data['method'] == '2':
                answer = secant_method(data['a'], data['b'], data['function'], data['error'])
            elif data['method'] == '3':
                answer = iteration_method(data['a'],  data['b'],  data['function'], data['error'])
            if (data['out'] == "консоль"):
                if data['method'] == '3': 
                    if answer[3]:
                        print("\nУсловие сходимости выполняется.")
                    else: 
                        print("\nУсловие сходимости не выполняется.")
                print("\nКорень уравнения: " + str(answer[0]))
                print("\nЗначение функции в корне: " + str(answer[1]))
                print("\nЧисло итераций: " + str(answer[2]))
                draw(data['function'], answer[0], data['a'], data['b'])
            else:
                file = open(FILE_OUT, "w", encoding="utf8")
                if data['method'] == '3': 
                    if answer[3]:
                        file.write("\nУсловие сходимости выполняется.")
                    else: 
                        file.write("\nУсловие сходимости не выполняется.")
                file.write("Корень уравнения: " + str(answer[0]))
                file.write("\nЗначение функции в корне: " + str(answer[1]))
                file.write("\nЧисло итераций: " + str(answer[2]))
                draw(data['function'], answer[0], data['a'], data['b'])
        else:
            answer = newtonMethod(data['system'][0], data['system'][1], data['x0'], data['y0'], data['error'])
            if answer is None:
                printErrorAnswer(data, "При выполнении метода произошла ошибка: невозможно точно вычислить один или два корня. Попробуйте выбрать другие начальные приближения")
                raise ValueError
            
            if (data['out'] == "консоль"):
                print("\nКорень уравнения: " + str(answer[0]))
                print("\nЗначение функции в корне: " + str(answer[1]))
                print("\nЧисло итераций: " + str(answer[2]))
                print("\nВектор погрешностей х:")
                for i in range(len(answer[3])):
                    print(answer[3][i])
                print("\nВектор погрешностей y:")
                for i in range(len(answer[4])):
                    print(answer[4][i])
            else:
                file = open(FILE_OUT, "w", encoding="utf8")
                file.write("Корень уравнения: " + str(answer[0]))
                file.write("\nЗначение функции в корне: " + str(answer[1]))
                file.write("\nЧисло итераций: " + str(answer[2]))
                file.write("\nВектор погрешностей х:\n")
                for i in range(len(answer[3])):
                    file.write(str(answer[3][i]) + "\n")
                file.write("\nВектор погрешностей y:\n")
                for i in range(len(answer[4])):
                    file.write(str(answer[4][i]) + "\n")
            getPlot(answer[0], answer[1], data['system'][0], data['system'][1])
            
    except ValueError:
        pass

main()