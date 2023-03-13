import math
import sys

FILE_IN = "files/input.txt"

def getmat_file():
    # Получить матрицу из файла
    with open(FILE_IN, 'rt') as fin:
        try:
            n = int(fin.readline())
            if (n<=0):
                raise ValueError
            matrix = []
            counter = 0
            precision = -1
            for line in fin:
                if (counter < n):
                    new_row = list(map(float, line.strip().split()))
                    if len(new_row) != (n + 1):
                        raise ValueError
                    matrix.append(new_row) 
                else:
                    precision = float(line)
                counter+=1
            if (precision < 0 or counter > n+1):
                raise TypeError
            if (len(matrix) != n):
                raise ValueError
        except ValueError:
            return None, None
        except TypeError:
            return matrix, None
    print("Порядок матрицы: " + str(n))
    print("Коэффициенты матрицы:")
    for row in matrix:
        for col in row:
            print('{:10}'.format(round(col, 3)), end='')
        print()
    print("Желаемая точность:" + str(precision))
    return matrix, precision


def precision_input(): 
    # Получить желаемую точность c клавиатуры
    try:
        precision = float(input("Введите желаемую точность: "))
    except ValueError:
        return None
    return precision

def getmat_input():
    # Получить матрицу с клавиатуры
    while True:
        try:
            n = int(input("Введите порядок матрицы: "))
            if n <= 0:
                print("Порядок матрицы должен быть положительным.")
            else:
                break
        except ValueError:
            print("Порядок матрицы должен быть целым числом.")
    matrix = []
    print("Вводите коэффициенты матрицы через пробел строка за строкой:")
    try:
        for i in range(n):
            matrix.append(list(map(float, input().strip().split())))
            if len(matrix[i]) != (n+1):
                raise ValueError
    except ValueError:
        return None
    return matrix

def diagonal(matrix):
    # Диагональное преобладание
    sorted = dict()
    column = 0
    for i in range (len(matrix)):
        maxValue = sys.float_info.min
        sum = 0

        for j in range (len(matrix)):
            previous = maxValue
            maxValue = max(maxValue, matrix[i][j])

            if (previous != maxValue):
                column = j
            
            sum += abs(matrix[i][j])
        
        sum -= maxValue
        if (maxValue>=sum):
            if (column in sorted):
                print("Приведение к диагональному представлению невозможно")
                return matrix
            else:
                sorted[column] = matrix[i]
        else:
            print("Приведение к диагональному представлению невозможно")
            return matrix

    result = []
    #Переставим уравнения местами так, чтобы выполнялось условие преобладания диагональных элементов
    for i in range(len(matrix)):
        if (i in sorted):
            result.append(sorted.get(i))
        else:
            print("Приведение к диагональному преобладанию невозможно")
            return matrix              

    print("Переставили строки так, чтобы выполнялось условие преобладания диагональных элементов:")
    for row in result:
        for col in row:
            print('{:10}'.format(round(col, 3)), end='')
        print()
    return result

def transform(matrix):
    #Выражаем из первого уравнения x_1, из второго x_2, из третьего x_3
    result = [[0] * len(matrix[0]) for i in range(len(matrix))]
    for i in range(len(matrix)):
        element = matrix[i][i]
        for j in range(len(matrix[0])):
            if (i != j):
                result[i][j] = matrix[i][j] / element
                if (j != (len(matrix[0])-1)):
                    result[i][j] *= -1
    print("Матрица C:")
    for i in range(len(result)):
        for j in range(len(result[0])-1):
            # print(result[i][j])
            print('{:10}'.format(round(result[i][j], 3)), end='')
        print()

    print("Матрица d:")
    for i in range(len(result)):
        print('{:10}'.format(round(result[i][len(result[0])-1], 3)))

    return result
            
def check(matrix):
    #Проверяем условие сходимости
    maxValue = sys.float_info.min
    for i in range(len(matrix)):
        sum = 0
        for j in range(len(matrix[0])-1):
            sum += matrix[i][j]
        maxValue = max(sum, maxValue)
    return maxValue < 1 


def iterate(matrix, precision, limit):
    # матрица d
    current = []
    for i in range(len(matrix)):
        current.append(matrix[i][len(matrix[0])-1])

    maxValue = sys.float_info.min
    criteria = sys.float_info.min
    counter = 0
    tmp = 0

    while True:
        previous = current.copy()
        for i in range(len(matrix)):
            for j in range(len(matrix[0])-1):
                    tmp += matrix[i][j] * previous[j]
            tmp += matrix[i][len(matrix[0])-1]
            current[i] = tmp

            maxValue = max(maxValue, abs(current[i] - previous[i]))

            tmp = 0
        criteria = maxValue
        maxValue = sys.float_info.min
        counter+=1
        if (counter == limit or criteria < precision):
            break

    if (counter == limit):
        print("Результат не получен за " + str(limit) + " итераций")
        return None
    
    #Вектор погрешностей
    for i in range(len(current)):
        previous[i] = abs(current[i]-previous[i])
    
    print("Вектор погрешностей: ")
    for col in previous:
        print(col)

    print("Результат получен за " + str(counter) + " итераций")

    return current


def solve(matrix, precision):
    matrix = diagonal(matrix)

    matrix = transform(matrix)

    if (check(matrix)):
        print("Достаточное условие сходимости выполняется")
    else:
        print("Достаточное условие сходимости не выполняется")

    return iterate(matrix, precision, 100000)


def main():
    print("\t\tЛабораторная работа #1 (7 вариант)")
    print("Метод простых итераций")
    print("Взять коэффициенты из файла (file) или ввести с клавиатуры (console) ?")

    method = input("")
    while (method != 'file') and (method != 'console'):
        print("Введите 'file' или 'console' для выбора способа ввода.")
        method = input("")

    if method == 'console':
        matrix = getmat_input()
        precision = precision_input()
    else:
        matrix, precision = getmat_file()

    if matrix is None:
        print("При считывании коэффициентов матрицы произошла ошибка!")
        return
    
    if precision is None:
        print("При считывании коэффициента точности произошла ошибка!")
        return

    answer = solve(matrix[:], precision)
    if (answer != None):
        print("Вектор неизвестных: ")
        for col in answer:
            print(col)
            # print('{}'.format(round(col, 3)))
    else:
        print("Ответ не получилось найти c данной точностью...")
        return

main()