import sys
from sympy import *
import numpy as np
import math

x = Symbol('x')

def check_infinite_break_at_point_a_and_b(f, a, b):
    try:
        limit_left = limit(f, x, b, '-')
        limit_right = limit(f, x, a, '+')
        if math.isinf(limit_left) or math.isinf(limit_right):
            return True
        else:
            return False
    except ValueError:
        return True
    
def check_infinite_break_at_point_interval(f, a, b):
    try:
        n = 10000
        points = np.linspace(a, b, n)
        for i in range(n):
            limit_left = limit(f, x, round(points[i], 2), '-')
            limit_right = limit(f, x, round(points[i], 2), '+')
            if math.isinf(limit_left) or math.isinf(limit_right):
                return True
        return False
                
    except ValueError:
        return True


def rectangle_method(function, a, b, error, modification):
    # Метод прямоугольников
    n = 4
    counter = 0

    while(True):
        x_h = a
        x1 = a
        # для вычисления I_h
        h = (b - a) / n 
        # для вычисления I_h/2
        h1 = h / 2 
    
        #I_h
        result_h = 0
        #I_h/2
        result_h1 = 0

        if (modification == "middle"):
            k = 2
            for i in range(n):
                result_h += function(x_h + h/2)
                x_h += h
            result_h *= h

            for i in range(2*n):
                result_h1 += function(x1 + h1/2)
                x1 += h1
            result_h1 *= h1
        elif (modification == "left"):
            k = 1
            for i in range(n):
                result_h += function(x_h)
                x_h += h
            result_h *= h

            for i in range(2*n):
                result_h1 += function(x1)
                x1 += h1
            result_h1 *= h1
        else: 
            k = 1
            x_h += h
            x1 += h1
            for i in range(n):
                result_h += function(x_h)
                x_h += h
            result_h *= h

            for i in range(2*n):
                result_h1 += function(x1)
                x1 += h1
            result_h1 *= h1

        if (counter > 1000):
            return None
        elif (((result_h1 - result_h) / (2**k - 1)) < error):
            break
        else: 
            n *= 2
            counter += 1
   
    return result_h, n  


def trapezoid_method(function, a, b, error):
    # Метод трапеций
    n = 4
    counter = 0
    k = 2

    while(True):
        # для вычисления I_h
        h = (b - a) / n 
        # для вычисления I_h/2
        h1 = h / 2 

        x_h = a + h
        x1 = a + h1
    
        #I_h
        result_h = (function(a) + function(b)) / 2
        #I_h/2
        result_h1 = result_h

        for i in range(n-1):
            result_h += function(x_h)
            x_h += h
        result_h *= h

        for i in range(2*n - 1):
            result_h1 += function(x1)
            x1 += h1
        result_h1 *= h1

        if (counter > 1000):
            return None
        elif (((result_h1 - result_h) / (2**k - 1)) < error):
            break
        else: 
            n *= 2
            counter += 1

    return result_h, n  


def simpson_method(function, a, b, error):
    # Метод Симпсона
    n = 4
    counter = 0
    k = 4

    while(True):
        # для вычисления I_h
        h = (b - a) / n 
        # для вычисления I_h/2
        h1 = h / 2 
    
        #I_h
        result_h = function(a) + function(b)
        #I_h/2
        result_h1 = result_h

        x_h = a + h
        x1 = a + h1

        for i in range(n-1):
            if i % 2 == 0:
                result_h += 4 * function(x_h)
            else:
                result_h += 2 * function(x_h)
            x_h += h
        result_h *= h / 3

        for i in range(2*n-1):
            if i % 2 == 0:
                result_h1 += 4 * function(x1)
            else:
                result_h1 += 2 * function(x1)
            x1 += h1
        result_h1 *= h1 / 3
    
        if (counter > 1000):
            return None
        elif (((result_h1 - result_h) / (2**k - 1)) < error):
            break
        else: 
            n *= 2
            counter += 1

    return result_h, n  



def getfunc(func_id):
    # Получить выбранную функцию
    if func_id == '1':
        return lambda x: x ** 2
    elif func_id == '2':
        return lambda x: 1 / x
    elif func_id == '3':
        return lambda x: 4 * x**3 - 5 * x**2 + 6 * x - 7
    elif func_id == '4':
        return lambda x: 1 / (1-x)
    else:
        return None
    
def getstrfunc(func_id):
    # Получить выбранную функцию в строковом формате
    if func_id == '1':
        return x**2
    elif func_id == '2':
        return  1 / x
    elif func_id == '3':
        return 4 * x**3 - 5 * x**2 + 6 * x - 7
    elif func_id == '4':
        return 1 / (1-x)
    else:
        return None


def getmethod(method_id):
    # Получить выбранный метод
    if method_id == '1':
        return 'rectangle_method'
    elif method_id == '2':
        return 'trapezoid_method'
    elif method_id == '3':
        return 'simpson_method'
    else:
        return None
    
def getmodification(modification_id):
    # Получить выбранную модификацию метода прямоугольников
    if modification_id == '1':
        return 'left'
    elif modification_id == '2':
        return 'right'
    elif modification_id == '3':
        return 'middle'
    else:
        return None


def getdata_input():
    # Получить данные с клавиатуры
    data = {}

    print("\nВыберите функцию.")
    print("1: x^2")
    print("2: 1 / x")
    print("3: 4x^3 - 5x^2 + 6x - 7")
    print("4: 1 / (1-x)")
    while True:
        try:
            func_id = input("")
            func = getfunc(func_id)
            strfunction = getstrfunc(func_id)
            if func is None:
                raise AttributeError
            break
        except AttributeError:
            print("Функции нет в списке.")
    data['function'] = func
    data['strfunction'] = strfunction

    print("\nВыберите метод решения.")
    print("1: Метод прямоугольников")
    print("2: Метод трапеций")
    print("3: Метод Симпсона")
    while True:
        try:
            method_id = input("")
            method = getmethod(method_id)
            if method == 'rectangle_method':
                print("\nВыберите модификацию метода")
                print("1: левые прямоугольники")
                print("2: правые прямоугольники")
                print("3: средние прямоугольники")
                while True:
                    try:
                        modification_id = input("")
                        modification = getmodification(modification_id)
                        if modification is None:
                            raise AttributeError
                        data['modification'] = modification
                        break
                    except AttributeError:
                        print("Модификации метода нет в списке.")
            if method is None:
                raise AttributeError
            break
        except AttributeError:
            print("Метода нет в списке.")
    data['method'] = method

    print("\nВведите пределы интегрирования.")
    while True:
        try:
            a, b = map(float, input("").split())
            if a > b:
                a, b = b, a
            break
        except ValueError:
            print("Пределы интегрирования должны быть числами, введенными через пробел.")
    data['a'] = a
    data['b'] = b

    print("\nВведите погрешность вычисления.")
    while True:
        try:
            error = float(input("Погрешность вычисления: "))
            if error <= 0:
                raise ArithmeticError
            break
        except (ValueError, ArithmeticError):
            print("Погрешность вычисления должна быть положительным числом.")
    data['error'] = error

    return data


def main():
    print("Лабораторная работа #3 (7)")
    print("Численное интегрирование")

    data = getdata_input()
    if ((check_infinite_break_at_point_a_and_b(data['strfunction'], data['a'], data['b'])) or check_infinite_break_at_point_interval(data['strfunction'], data['a'], data['b'])):
        print("Интеграл не существует")
    else:   
        if data['method'] == 'rectangle_method':
            answer = rectangle_method(data['function'], data['a'], data['b'], data['error'], data['modification'])
        elif data['method'] == 'trapezoid_method':
            answer = trapezoid_method(data['function'], data['a'], data['b'], data['error'])
        else:
            answer = simpson_method(data['function'], data['a'], data['b'], data['error'])


        if answer == None:
            print("Не получилось получить ответ с требуемой точностью за 10000 итераций")
            sys.exit()
            
        print("Значение интеграла: " + str(answer[0]))
        print("Количество разбиений: " + str(answer[1]))

main()