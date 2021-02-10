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
"""pd.set_option('display.max_columns', 500)  # Количество столбцов
pd.set_option('display.max_rows', 1000)  # Количество строк
pd.set_option('display.width', 1500)  # Макс. ширина таблицы для показа"""

timezone = pytz.timezone("Etc/UTC")


def get_rates():
    """

    :return: Возвращает значения баров основного таймфрейма (М30) за период от from_date до to_date

    """
    from_date = datetime(2021, 1, 25, 10, tzinfo=timezone)
    to_date = datetime(2021, 1, 30, tzinfo=timezone)
    res = mt5.copy_rates_range(symbol, frame, from_date, to_date)
    return res


"""# Выводим на печать массив значений баров в виде таблицы
rates_frame = pd.DataFrame(get_rates())
rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
# print(rates_frame)"""


def last_index():
    """

    :return: Возвращает индекс 0-го бара с начала массива

    """
    return len(get_rates()) - len(get_rates())


# Переназначаем переменные для упрощения написания дальнейших функций
rates = get_rates()
high = last_index()


# print("high = ", high)


def fractal_up(high):
    """

    :param high: Индекс 0-го бара, для упрощения перебора индексов внутри массива
    :return: Возвращает:
                [0] - Значение наивысшей точки фрактала
                [1] - Условие обнаружения фрактала
                [2] - Значение времени в секундах, равное времени начала формирования третьего бара после [0].
                        С этого значения времени начинается перебор баров на ТФ М1.
                [3] - Знаение времени в секундах, равное времени окончания периода выборки для ТФ М30.

    """
    for _ in rates:
        if rates[high + 2][2] > rates[high + 1][2] and \
                rates[high + 2][2] > rates[high][2] and \
                rates[high + 2][2] >= rates[high + 3][2] and \
                rates[high + 2][2] >= rates[high + 4][2]:
            print("Есть фрактал вверх. Точка фрактала = ", rates[high + 2][2])
            # print(candle)
            flag_by_fractal_up = True
            # print("Flag Fractal BUY = ", flag_by_fractal_up)
            return rates[high + 2][2], flag_by_fractal_up, rates[high + 5][0], \
                   rates[last_index() + len(get_rates()) - 1][0]
        else:
            print("Нет фрактала. Current High = ", rates[high + 2][2])
            # print(candle)
            # flag_by_fractal_up = False
            # print("Flag Fractal BUY = ", flag_by_fractal_up)
            # print("Нет фрактала", rates[n + 2][2])
            high += 1


# Присваивание переменным значений, пролучаемых в функции fractal_up
buy_price = fractal_up(high)[0]
flag_by_fractal_up = fractal_up(high)[1]
date_from_for_m1 = int(fractal_up(high)[2])  # datetime.strptime(str(buy_price[2]), "%Y.%m.%d")
date_to_for_m1 = int(fractal_up(high)[3])  # datetime.strptime(str(buy_price[3]), "%Y.%m.%d")


# print("Проверка возврата значений функции fractal_up()")
# print("BUY PRICE = ", buy_price)
# print("Flag BUY - ", flag_by_fractal_up)
# print("Date from ticks, sec = ", date_from_for_m1)
# print("Date to ticks, sec = ", date_to_for_m1)

# print("Проверка присваивания дат переменным")
# print("Дата от - ", date_from_for_m1, datetime.fromtimestamp(date_from_for_m1-60*60*3))
# print("Дата до - ", date_to_for_m1, datetime.fromtimestamp(date_to_for_m1-60*60*3))


def get_price_m1():
    #
    price_last_m1 = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M1, date_from_for_m1, date_to_for_m1)
    # ticks_last = mt5.copy_ticks_range(symbol, date_from_for_m1, date_to_for_m1, mt5.COPY_TICKS_INFO)
    # for ticks in ticks_last:
    # print("Tick Last Price = ", ticks[3])
    return price_last_m1
    # return ticks_last


# print(len(get_price_m1()))
# index_rows = 0
# index_columns = 2
# last_high_m1 = get_price_m1()[index_rows][index_columns]
# print(last_high_m1)
# print("ТИП last_high_m1", last_high_m1, type(last_high_m1))
# print("ТИП BUY_PRICE", buy_price, type(buy_price))
# print(get_price_m1())

# Выводим на печать массив значений тиков в виде таблицы
ticks_frame = pd.DataFrame(get_price_m1())
ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')


# Печать значений тиков в виде таблицы
# print(ticks_frame)


# print(get_price_m1()[3])


def searches_bars_on_m1_before_activation():
    index_rows = 0
    index_columns = 2
    last_high_m1 = get_price_m1()[index_rows][index_columns]
    for _ in get_price_m1():
        if flag_by_fractal_up:
            # print("Начинаем перебор тиков")
            if last_high_m1 >= buy_price:
                flag_by_open_m1_buy = True
                print("!!!Пробитие на минутах!!! Дальше перебираем тики с предыдущего минутного бара",
                      "\n", "Точка входа =", buy_price, "\n" "High бара =", last_high_m1)  # , "Значения = ", ticks)
                # print(get_price_m1()[index_rows][0])
                return flag_by_open_m1_buy, get_price_m1()[index_rows - 1][0]
            else:
                print("Следующий бар.", "Бар №", index_rows, " High =", last_high_m1, "Точка входа = ", buy_price)
                index_rows += 1
                last_high_m1 = get_price_m1()[index_rows][index_columns]
                # print(index_rows, index_columns)


searches_bars_on_m1_before_activation()

flag_by_open_m1_by = searches_bars_on_m1_before_activation()[0]
print(flag_by_open_m1_by)
date_from_for_ticks = int(searches_bars_on_m1_before_activation()[1])
print(date_from_for_ticks)
date_to_for_ticks = date_to_for_m1
print(date_to_for_ticks)
print("Проверка присваивания дат переменным")
print("Дата от - ", date_from_for_ticks, datetime.fromtimestamp(date_from_for_ticks - 60 * 60 * 3))
print("Дата до - ", date_to_for_ticks, datetime.fromtimestamp(date_to_for_ticks - 60 * 60 * 3))

"""print(flag_by_open_by)
print(date_from_for_ticks)
print(date_to_for_ticks)"""


def get_price_ticks():
    #
    # price_ticks_last = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M1, date_from_for_ticks, date_to_for_ticks)
    price_ticks_last = mt5.copy_ticks_range(symbol, date_from_for_ticks, date_to_for_ticks, mt5.COPY_TICKS_INFO)
    # for ticks in ticks_last:
    # print("Tick Last Price = ", ticks[3])
    return price_ticks_last
    # return ticks_last


ticks_frame = pd.DataFrame(get_price_ticks())
ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')
print(ticks_frame)


def ticks_ver_near_the_entry_point_up():
    index_rows_ticks = 0
    index_columns_ticks = 3
    last_ticks = get_price_ticks()[index_rows_ticks][index_columns_ticks]
    for _ in get_price_ticks():
        if flag_by_open_m1_by:
            if last_ticks > buy_price:
                flag_by_open_position = True
                print("Позиция открыта", flag_by_open_position, last_ticks, index_rows_ticks)
                return flag_by_open_position
            else:
                print("Следующий тик", last_ticks, index_rows_ticks)
                index_rows_ticks +=1
                last_ticks = get_price_ticks()[index_rows_ticks][index_columns_ticks]


ticks_ver_near_the_entry_point_up()