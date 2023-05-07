import math
import matplotlib.pyplot as plt
import numpy as np

FILE_IN = "files/input.txt"
x_i, n_i, p_i = [], [], []

def getdata_file():
    # Получить данные из файла
    with open(FILE_IN, 'rt', encoding="utf-8") as fin:
        try:
            with open(FILE_IN, 'rt', encoding='UTF-8') as fin:
                data = [list(map(float, row.split())) for row in fin.readlines()]
                return data[0]
        except (ValueError):
            print("Ошибка! С файлом проблемы!")

def numerical_characteristics_of_distribution_stat(data):
    #Получить числовые характеристики статистического распределения
    n = len(data)
    m, dispersion, q = 0, 0, 0

    data_un = np.unique(data)

    for x in data_un:
        counter = 0 
        x_i.append(x)
        for i in data:
            if (i == x):
                counter+=1
        n_i.append(counter)
        p_i.append(counter / n)

    for i in range(len(x_i)):
        m += x_i[i] * p_i[i] 
    
    for i in range(len(x_i)):
        dispersion += (x_i[i] - m)**2 * p_i[i]

    q = dispersion**(1/2)

    s = n/(n-1)*dispersion

    s_sqrt = s**(1/2)

    return m, dispersion, q, data_un, s, s_sqrt


def variation_series_info(data):
    info = {}

    data.sort()
    n = len(data)
    info["varser"] = data
    info["min"] = data[0]
    info["max"] = data[n-1]
    info["scope"] = info["max"] - info["min"]
    info["interval"] = round(1 + math.log(n,2), 0)
    info["h"] = info["scope"] / info["interval"]
    info["xStart"] = info["min"] - info["h"]/2
    info["num_characteristics"] = numerical_characteristics_of_distribution_stat(data)

    return info

def calculateEmpiricFunction(data):
    #Посчитать Эмпирическую функцию
    draw = []
    counter = 0
    f = 0 
    print("Эмпирическая функция:")
    for i in p_i:
        if (f == 0):
            print(round(f,4), f", при x <= {data[counter]}")
        else:
            print(str(round(f, 4)), f", при {prev} < x <= {data[counter]}")
        draw.append((data[counter], round(f,4)))
        f += i
        prev = data[counter]
        counter += 1
    draw.append((data[-1], round(f,4)))
    print(str(round(f, 4)), f", при x > {data[-1]}")

    return draw

def drawEmpiricFunction(fun_data):
    #Нарисовать Эмпирическую функцию
    ax = plt.gca()
    plt.grid()

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    x, y = zip(*fun_data)
    x_new = list(x)
    y_new = list(y)

    plt.title("График Эмпирической функции распределения")
    plt.plot([x_new[0] - 0.5, x_new[0]], [y_new[0], y_new[0]], color='r')
    plt.plot([x_new[-1], x_new[-1] + 0.5], [y_new[-1], y_new[-1]], color='r')
    for i in range(len(x_new) - 1):
        plt.plot([x_new[i], x_new[i + 1]], [y_new[i + 1], y_new[i + 1]], color='r')

    plt.savefig(f"empiric_function.png")
    plt.show(block=True)

def drawHistogram(max, h, xStart, data):
    #Нарисовать гистограмму относительной частоты
    histogram_data = []
    while xStart < max:
        counter = 0
        for val in data:
            if (val >= xStart and val < (xStart+h)):
                counter+=1 
        p_w = counter / (len(data) * h)
        histogram_data.append((f"[{round(xStart, 2)}; {round(xStart+h, 2)})", p_w))
        xStart += h
    
    x, y = zip(*histogram_data)

    fig, ax = plt.subplots()
    ax.bar(x, y)


    fig.set_figwidth(12)
    fig.set_figheight(6)

    plt.title("Гистограмма относительных частот")
    plt.savefig("histogram.png")
    plt.show(block=True)


def drawFrequencyPolygon(max, h, xStart, data):
    #Нарисовать полигон частот
    polygon_data = []
    n = len(data)
    while xStart < max:
        counter = 0
        for val in data:
            if (val >= xStart and val < (xStart + h)):
                counter += 1
        polygon_data.append(((xStart+h)/2, counter))
        if(xStart + h > max):
            print(f"[ {xStart} : {xStart+h} ] - {counter} - {counter/n}")
        else:
            print(f"[ {xStart} : {xStart+h} ) - {counter} - {counter/n}")
        xStart += h

    ax = plt.gca()
    plt.grid()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    x, y = zip(*polygon_data)
    x_new = list(x)
    y_new = list(y)

    plt.title("Полигон частот")
    plt.plot(x_new, y_new, '-o')

    plt.savefig(f"poligon.png")
    plt.show(block=True)



def main():
    data = variation_series_info(getdata_file())

    print("Вариационный ряд: ", data["varser"])
    print("Экстремальные значения: ")
    print("Max: ", data["max"])
    print("Min: ", data["min"])
    print("Размах выборки: ", data["scope"])
    
    print("Математическое ожидание0", data["num_characteristics"][0])
    print("Дисперсия", data["num_characteristics"][1])
    print("Среднеквадратическое отклонение", data["num_characteristics"][2])
    print("Исправленная выборочная дисперсия", data["num_characteristics"][4])
    print("Исправленное выборочное среднее квадратическое отклонение", data["num_characteristics"][5])

    data_for_draw = calculateEmpiricFunction(data["num_characteristics"][3])
    drawEmpiricFunction(data_for_draw)

    drawFrequencyPolygon(data["max"], data["h"], data["xStart"], data["varser"])

    drawHistogram(data["max"], data["h"], data["xStart"], data["varser"])
    
main()