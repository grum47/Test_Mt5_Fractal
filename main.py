import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime

mt5.initialize()
if not mt5.initialize():
    print("Инициализация не прошла. Ошибка - ", mt5.last_error())
    quit()

symbol = "Si-3.21"
frame = mt5.TIMEFRAME_M30
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1500)


def get_rates():
    """

    :return: Возвращает значения баров за период от from_date до to_date

    """
    from_date = datetime(2021, 1, 25, 10)
    to_date = datetime(2021, 1, 30)
    res = mt5.copy_rates_range(symbol, frame, from_date, to_date)
    return res


# Выводим на печать массив значений баров в виде таблицы
rates_frame = pd.DataFrame(get_rates())
print(rates_frame)


def get_price():
    pass


def last_index():
    """

    :return: Возвращает индекс 0-го бара с начала массива

    """
    return len(get_rates()) - len(get_rates())


# Переназначаем переменные для упрощения написания дальнейших функций
rates = get_rates()
high = last_index()
print("high = ", high)


def fractal_up(high):
    for _ in rates:
        if rates[high + 2][2] > rates[high + 1][2] and \
                rates[high + 2][2] > rates[high][2] and \
                rates[high + 2][2] >= rates[high + 3][2] and \
                rates[high + 2][2] >= rates[high + 4][2]:
            print("Есть фрактал вверх. Точка фрактала = ", rates[high + 2][2])
            flag_by_fractal_up = True
            print("Flag Fractal BUY = ", flag_by_fractal_up)
            return rates[high + 2][2], flag_by_fractal_up, rates[high + 2][0]
        else:
            print("Нет фрактала")
            flag_by_fractal_up = False
            print("Flag Fractal BUY = ", flag_by_fractal_up)
            # print("Нет фрактала", rates[n + 2][2])
            high += 1


buy_price = fractal_up(high)

print("BUY PRICE = ", buy_price[0])
print("Flag BUY - ", buy_price[1])
print("Time, sec = ", buy_price[2])

if buy_price[1] == True:
    print("False")
else:
    print("True")
