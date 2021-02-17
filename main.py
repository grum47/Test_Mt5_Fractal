from datetime import datetime
import time
import MetaTrader5 as mt5
import pandas as pd
import pytz

mt5.initialize()
if not mt5.initialize():
    print("Инициализация не прошла. Ошибка - ", mt5.last_error())
    quit()

symbol = "Si-3.21"
frame = mt5.TIMEFRAME_M30
timezone = pytz.timezone("Etc/UTC")
from_date = datetime(2021, 1, 25, 10, tzinfo=timezone)
print(from_date)
to_date = datetime(2021, 1, 27, tzinfo=timezone)
tp = 15
sl = 60
pd.set_option('display.max_columns', 500)  # Количество столбцов
pd.set_option('display.max_rows', 1000)  # Количество строк
pd.set_option('display.width', 1500)  # Макс. ширина таблицы для показа


def get_value_bars_main_timeframe(symbol, frame, from_date, to_date):
    """

    :return: Возвращает значения баров основного таймфрейма (М30) за период от from_date до to_date

    """

    rates = mt5.copy_rates_range(symbol, frame, from_date, to_date)
    return rates


def get_value_bars_m1_timeframe(symbol, from_date, to_date):
    """

    :param symbol: Используемый инструмент
    :param from_date: Дата начала периода
    :param to_date: Дата окончания периода
    :return: Возвращает массив значений свечей по ТФ М1
    """
    rates_m1 = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M1, from_date, to_date)
    return rates_m1


def get_ticks_values(symbol, from_date, to_date):
    """

    :param symbol:
    :param from_date:
    :param to_date:
    :return:
    """
    rates_ticks = mt5.copy_ticks_range(symbol, from_date, to_date, mt5.COPY_TICKS_INFO)
    return rates_ticks


def last_index():
    """

    :return: Возвращает индекс 0-го бара с начала массива

    """
    return len(get_value_bars_main_timeframe(symbol, frame, from_date, to_date)) - len(
        get_value_bars_main_timeframe(symbol, frame, from_date, to_date))


# Переназначаем переменные для упрощения написания дальнейших функций

rates = get_value_bars_main_timeframe(symbol, frame, from_date, to_date)
rates_m1 = get_value_bars_m1_timeframe(symbol, from_date, to_date)
rates_ticks = get_ticks_values(symbol, from_date, to_date)


# Выводим на печать массив значений баров в виде таблицы

# rates_frame = pd.DataFrame(rates)
# rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
# print(rates_frame)

rates_frame_m1 = pd.DataFrame(rates_m1)
rates_frame_m1['time'] = pd.to_datetime(rates_frame_m1['time'], unit='s')
print(rates_frame_m1)

# ticks_frame = pd.DataFrame(get_ticks_values(symbol, from_date, to_date))
# ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')
# print(ticks_frame)


def fractal_up(ind=2):
    """
    :param ind: Значение индекса столбца HIGH
    :return:
    """
    for _ in rates:
        flag_by_fractal_up = False
        if not flag_by_fractal_up:
            if rates['high'][ind] > rates['high'][ind - 1] and \
                    rates['high'][ind] > rates['high'][ind - 2] and \
                    rates['high'][ind] >= rates['high'][ind + 1] and \
                    rates['high'][ind] >= rates['high'][ind + 2]:
                print("Есть фрактал вверх. Точка фрактала = ", rates['high'][ind])
                # print("Время фрактала", datetime.fromtimestamp(rates['time'][ind]))
                # print("Время фрактала", rates['time'][ind])
                flag_to_open_pos_m1 = True
                flag_by_fractal_up = True
                time.sleep(1)
                ind += 1
                print(rates['time'][ind-1])
                print(rates['high'][ind-1])
                from_date = datetime.fromtimestamp(rates['time'][ind])
                if flag_by_fractal_up:
                    if flag_to_open_pos_m1:
                        rates_m1 = get_value_bars_m1_timeframe(symbol, from_date, to_date)
                        ind_m1 = 2
                        for high in rates_m1:
                            if rates_m1['high'][ind_m1] > rates['high'][ind-1]:
                                print("Пересечение на минутном графике - Open -  ", rates_m1['open'][ind_m1])
                                print("Пересечение на минутном графике - High - ", rates_m1['high'][ind_m1])
                                print("Пересечение на минутном графике - Low - ", rates_m1['low'][ind_m1])
                                print("Пересечение на минутном графике - Close - ", rates_m1['close'][ind_m1])
                                flag_to_open_pos_ticks = True
                                time.sleep(1)
                                print(rates_m1['time'][ind_m1])
                                from_date = datetime.fromtimestamp(rates_m1['time'][ind_m1])
                                ind_m1 += 1
                                if flag_to_open_pos_ticks:
                                    rates_ticks = get_ticks_values(symbol, from_date, to_date)
                                    ind_ticks = 2
                                    for price in rates_ticks:
                                        print(rates_ticks['last'][ind_ticks])
                                        print(rates['high'][ind-1])
                                        if rates_ticks['last'][ind_ticks] > rates['high'][ind-1]:
                                            print("Пересечение на тиковом Графике", price)
                                            print(rates_ticks['last'][ind_ticks])
                                            time.sleep(2)
                                            break
                                        else:
                                            ind_ticks += 1
                            else:
                                ind_m1 += 1
            else:
                ind += 1


print(fractal_up(ind=2))

"""
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


def get_value_bars_m1_timeframe():
    #
    rates_m1 = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M1, date_from_for_m1, date_to_for_m1)
    # ticks_last = mt5.copy_ticks_range(symbol, date_from_for_m1, date_to_for_m1, mt5.COPY_TICKS_INFO)
    # for ticks in ticks_last:
    # print("Tick Last Price = ", ticks[3])
    return rates_m1
    # return ticks_last


# print(len(get_value_bars_m1_timeframe()))
# index_rows = 0
# index_columns = 2
# last_high_m1 = get_value_bars_m1_timeframe()[index_rows][index_columns]
# print(last_high_m1)
# print("ТИП last_high_m1", last_high_m1, type(last_high_m1))
# print("ТИП BUY_PRICE", buy_price, type(buy_price))
# print(get_value_bars_m1_timeframe())

# Выводим на печать массив значений тиков в виде таблицы
ticks_frame = pd.DataFrame(get_value_bars_m1_timeframe())
ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')


# Печать значений тиков в виде таблицы
# print(ticks_frame)


# print(get_value_bars_m1_timeframe()[3])


def searches_bars_on_m1_before_activation():
    index_rows = 0
    index_columns = 2
    last_high_m1 = get_value_bars_m1_timeframe()[index_rows][index_columns]
    for _ in get_value_bars_m1_timeframe():
        if flag_by_fractal_up:
            # print("Начинаем перебор тиков")
            if last_high_m1 >= buy_price:
                flag_by_open_m1_buy = True
                print("!!!Пробитие на минутах!!! Дальше перебираем тики с предыдущего минутного бара",
                      "\n", "Точка входа =", buy_price, "\n" "High бара =", last_high_m1)  # , "Значения = ", ticks)
                # print(get_value_bars_m1_timeframe()[index_rows][0])
                return flag_by_open_m1_buy, get_value_bars_m1_timeframe()[index_rows][0], get_value_bars_m1_timeframe()[index_rows + 1][0]
            else:
                # print("Следующий бар.", "Бар №", index_rows, " High =", last_high_m1, "Точка входа = ", buy_price)
                index_rows += 1
                last_high_m1 = get_value_bars_m1_timeframe()[index_rows][index_columns]
                # print(index_rows, index_columns)


searches_bars_on_m1_before_activation()

flag_by_open_m1_by = searches_bars_on_m1_before_activation()[0]
# print(flag_by_open_m1_by)
date_from_for_ticks = int(searches_bars_on_m1_before_activation()[1])
# print(date_from_for_ticks)
date_to_for_ticks = int(searches_bars_on_m1_before_activation()[2])  # date_to_for_m1
# print(date_to_for_ticks)
# print("Проверка присваивания дат переменным")
# print("Дата от - ", date_from_for_ticks, datetime.fromtimestamp(date_from_for_ticks - 60 * 60 * 3))
# print("Дата до - ", date_to_for_ticks, datetime.fromtimestamp(date_to_for_ticks - 60 * 60 * 3))

print(flag_by_open_by)
print(date_from_for_ticks)
print(date_to_for_ticks)


def get_ticks_values():
    #
    # price_ticks_last = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M1, date_from_for_ticks, date_to_for_ticks)
    price_ticks_last = mt5.copy_ticks_range(symbol, date_from_for_ticks, date_to_for_ticks, mt5.COPY_TICKS_INFO)
    # for ticks in ticks_last:
    # print("Tick Last Price = ", ticks[3])
    return price_ticks_last
    # return ticks_last


ticks_frame = pd.DataFrame(get_ticks_values())
ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')


# print(ticks_frame)


def ticks_ver_near_the_entry_point_up():
    index_rows_ticks = 0
    index_columns_ticks = 3
    last_ticks = get_ticks_values()[index_rows_ticks][index_columns_ticks]
    tp: int = 15
    sl: int = 60

    for ticks in get_ticks_values():
        flag_by_open_position = False
        if flag_by_open_m1_by:
            if last_ticks > buy_price:
                flag_by_open_position = True
                tp = last_ticks + tp
                sl = last_ticks - sl
                print("Позиция открыта", flag_by_open_position, last_ticks, index_rows_ticks, tp, sl, ticks)
                #  return last_ticks, flag_by_open_position
            if flag_by_open_position:
                index_rows_ticks += 1
                last_ticks = get_ticks_values()[index_rows_ticks][index_columns_ticks]
                if last_ticks >= tp:
                    print("Позиция закрылась по Тейку")
                elif last_ticks <= sl:
                    print("Позиция закрылась по Стопу", index_rows_ticks)
            #  else:
            #  print("Иначе")
            else:
                print("Следующий тик", last_ticks, index_rows_ticks)
                index_rows_ticks += 1
                last_ticks = get_ticks_values()[index_rows_ticks][index_columns_ticks]


ticks_ver_near_the_entry_point_up()"""

"""def finding_the_exit_point():
    tp = 15
    sl = 60
    tp, sl = ticks_ver_near_the_entry_point_up()[0] + tp, ticks_ver_near_the_entry_point_up()[0] - sl
    #  sl = ticks_ver_near_the_entry_point_up()[0] - sl
    print("Уровень Тейк-Профит =", tp)
    print("Уровень Стоп-Лосс =", sl)


finding_the_exit_point()"""
