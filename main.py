import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import pytz


mt5.initialize()
if not mt5.initialize():
    print("Инициализация не прошла. Ошибка - ", mt5.last_error())
    quit()

symbol = "Si-3.21"
frame = mt5.TIMEFRAME_M30
pd.set_option('display.max_columns', 500)  # Количество столбцов
pd.set_option('display.max_rows', 1000)  # Количество строк
pd.set_option('display.width', 1500)  # Макс. ширина таблицы для показа
timezone = pytz.timezone("Etc/UTC")

def get_rates():
    """

    :return: Возвращает значения баров за период от from_date до to_date

    """
    from_date = datetime(2021, 1, 25, 10, tzinfo=timezone)
    to_date = datetime(2021, 1, 30, tzinfo=timezone)
    res = mt5.copy_rates_range(symbol, frame, from_date, to_date)
    return res


# Выводим на печать массив значений баров в виде таблицы
rates_frame = pd.DataFrame(get_rates())
print(rates_frame)


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
            return rates[high + 2][2], flag_by_fractal_up, rates[high + 5][0], \
                   rates[last_index() + len(get_rates()) - 1][0]
        else:
            print("Нет фрактала")
            flag_by_fractal_up = False
            print("Flag Fractal BUY = ", flag_by_fractal_up)
            # print("Нет фрактала", rates[n + 2][2])
            high += 1


buy_price = fractal_up(high)
print("Проверка возврата значений функции fractal_up()")
print("BUY PRICE = ", buy_price[0])
print("Flag BUY - ", buy_price[1])
print("Date from ticks, sec = ", buy_price[2])
print("Date to ticks, sec = ", buy_price[3])


date_from_for_ticks = int(buy_price[2])             #datetime.strptime(str(buy_price[2]), "%Y.%m.%d")
date_to_for_ticks = int(buy_price[3])               #datetime.strptime(str(buy_price[3]), "%Y.%m.%d")
print("Проверка присваивания дат переменным")
print("Дата от - ", date_from_for_ticks)
print("Дата до - ", date_to_for_ticks)


def get_price():
    ticks_last = mt5.copy_ticks_from(symbol, date_from_for_ticks, date_to_for_ticks, mt5.COPY_TICKS_INFO)
    """
    if ticks_last == None:
        print(mt5.last_error())"""
    print("Получено тиков: ", len(ticks_last))
    return ticks_last


get_price()
# Выводим на печать массив значений тиков в виде таблицы
ticks_frame = pd.DataFrame(get_price())
ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')
print(ticks_frame)

"""if buy_price[1] == True:
    print("True")
else:
    print("False")
"""