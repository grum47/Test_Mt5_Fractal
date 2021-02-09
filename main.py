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

    :return: Возвращает индекс 3-го бара с конца массива
    Если в массиве 100 строк, то возвратит значение 97-й строки.
    0-й бар - текущий.

    """
    return len(get_rates()) - len(get_rates())


# Переназначаем переменные для упрощения написания дальнейших функций
rates = get_rates()
n = last_index()
print(n)


def fractal_up(n):
    for _ in rates:
        if rates[n + 2][2] > rates[n + 1][2] and \
                rates[n + 2][2] > rates[n][2] and \
                rates[n + 2][2] >= rates[n + 3][2] and \
                rates[n + 2][2] >= rates[n + 4][2]:
            print("Есть фрактал вверх. Точка фрактала = ", rates[n + 2][2])
            return rates[n + 2][2]
        else:
            print("Нет фрактала")
            # print("Нет фрактала", rates[n + 2][2])
            n += 1


buy_price = fractal_up(n)
# print(buy_price)
