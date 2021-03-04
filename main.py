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
frame = mt5.TIMEFRAME_M15
timezone = pytz.timezone("Etc/UTC")
from_date = datetime(2020, 1, 1, 10, tzinfo=timezone)
# print(from_date)
to_date = datetime(2020, 12, 1, tzinfo=timezone)
# print(to_date)
pd.set_option('display.max_columns', 500)  # Количество столбцов
pd.set_option('display.max_rows', 1000)  # Количество строк
pd.set_option('display.width', 1500)  # Макс. ширина таблицы для показа


def get_value_bars_main_timeframe(symbol, frame, from_date, to_date):
    """

    :return: Возвращает значения баров основного таймфрейма (М30) за период от from_date до to_date

    """

    rates = mt5.copy_rates_range(symbol, frame, from_date, to_date)
    return rates


# def get_one_bars_main_timeframe(symbol, frame, from_date, to_date):
#     """
#
#     :return: Возвращает значения баров основного таймфрейма (М30) за период от from_date до to_date
#
#     """
#
#     rates = mt5.copy_rates_from(symbol, frame, from_date, 1)
#     return rates[0][2]

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


# def last_index():
#     """
#
#     :return: Возвращает индекс 0-го бара с начала массива
#
#     """
#     return len(get_value_bars_main_timeframe(symbol, frame, from_date, to_date)) - len(
#         get_value_bars_main_timeframe(symbol, frame, from_date, to_date))


# Переназначаем переменные для упрощения написания дальнейших функций

# candle_m30 = get_one_bars_main_timeframe(symbol, frame, from_date, to_date)
rates = get_value_bars_main_timeframe(symbol, frame, from_date, to_date)
rates_m1 = get_value_bars_m1_timeframe(symbol, from_date, to_date)
rates_ticks = get_ticks_values(symbol, from_date, to_date)


# Выводим на печать массив значений баров в виде таблицы

# print(candle_m30)

# rates_frame = pd.DataFrame(rates)
# rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
# print(rates_frame)

# rates_frame_m1 = pd.DataFrame(rates_m1)
# rates_frame_m1['time'] = pd.to_datetime(rates_frame_m1['time'], unit='s')
# print(rates_frame_m1)

# ticks_frame = pd.DataFrame(get_ticks_values(symbol, from_date, to_date))
# ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')
# print(ticks_frame)


# def fractal_up_detection(ind):
#     flag_by_fractal_up_search = False
#     while not flag_by_fractal_up_search:
#         last_high_m30 = rates['high'][ind]
#         # print("last_high_m30 = ", last_high_m30)
#         if last_high_m30 > rates['high'][ind - 1] and \
#                 last_high_m30 > rates['high'][ind - 2] and \
#                 last_high_m30 >= rates['high'][ind + 1] and \
#                 last_high_m30 >= rates['high'][ind + 2]:
#             ind += 1
#             print(last_high_m30)
#             return last_high_m30
#         else:
#             ind += 1
#             flag_by_fractal_up_search = True
#             return flag_by_fractal_up_search
#
# print(fractal_up_detection(2))

def fractal_up_search(ind=2, tp=15, sl=200):
    """
    :param sl: Значение Стоп-лосс
    :param tp: Значение Тейк-профит
    :param ind: Значение индекса столбца HIGH
    :return:
    """
    flag_by_fractal_up_search = False
    # flag_move_orders = False
    # Начинаем перебор баров исторического периода

    profit = 0
    for _ in get_value_bars_main_timeframe(symbol, frame, from_date, to_date):

        if not flag_by_fractal_up_search:

            last_high_m30 = rates['high'][ind]
            # print("last_high_m30 = ", last_high_m30)
            # Условие определения фрактала ВВЕРХ
            if last_high_m30 > rates['high'][ind - 1] and \
                    last_high_m30 > rates['high'][ind - 2] and \
                    last_high_m30 >= rates['high'][ind + 1] and \
                    last_high_m30 >= rates['high'][ind + 2]:

                price_fractal_up_first = last_high_m30
                # print("price_fractal_up_first ================", price_fractal_up_first)
                time_fractal_up_first = rates['time'][ind]
                # print("time_fractal_up_first", time_fractal_up_first)
                # print("----------------------- Первый фрактал --------------------------------", price_fractal_up_first)
                # time.sleep(1)
                # ind += 1
                # print("ind", ind)
                ind_n = ind + 1
                # print("ind_n", ind_n)
                flag_by_fractal_up_search = True
                # from_date_next_fractal = time_fractal_up_first

                for _ in get_value_bars_main_timeframe(symbol, frame, from_date, to_date):

                    if flag_by_fractal_up_search:

                        last_high_m30_next = rates['high'][ind_n]
                        # print("last_high_m30_next", last_high_m30_next)

                        if last_high_m30_next > rates['high'][ind_n - 1] and \
                                last_high_m30_next > rates['high'][ind_n - 2] and \
                                last_high_m30_next >= rates['high'][ind_n + 1] and \
                                last_high_m30_next >= rates['high'][ind_n + 2]:

                            # print("======================= Новый фрактал =========================", last_high_m30_next)
                            # print('ind_n', ind_n)
                            ind_n += 1
                            ind = ind_n
                            # print('ind', ind)
                            flag_by_next_fractal_up_search = True
                            # flag_by_fractal_up_search = False
                            price_fractal_up_first = last_high_m30_next
                            time_fractal_up_first = rates['time'][ind_n]
                            # print("price_fractal_up_first =============================", price_fractal_up_first)

                            # for _ in get_value_bars_main_timeframe(symbol, frame, from_date, to_date):
                            #
                            #     if last_high_m30_next > price_fractal_up_first:
                            #         print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++пробитие")
                            #         ind_n += 1
                            #     else:
                            #         ind_n += 1
                            #     break

                        elif last_high_m30_next > price_fractal_up_first:
                            # print("------------------------------пересечение уровня фрактала------", last_high_m30_next)
                            ind_n += 1
                            # flag_by_fractal_up_search = False

                            # Флаг условия перебора свечей на таймфрейме М1
                            flag_to_open_pos_m1 = False

                            # Изменение периода выборки для таймфрейма М1 (начало выборки = моменту обнаружения фрактала)
                            # Приходится прибавить 3 30-минутные свечи. Пока не понятно почему.
                            from_date_m1 = datetime.fromtimestamp(time_fractal_up_first + 60 * 30 * 3 * 0)

                            # print(from_date_m1)
                            # print(datetime.timestamp(from_date_m1))
                            # print(to_date)

                            rates_m1 = get_value_bars_m1_timeframe(symbol, from_date_m1, to_date)

                            # print(rates_m1)
                            # rates_frame_m1 = pd.DataFrame(rates_m1)
                            # rates_frame_m1['time'] = pd.to_datetime(rates_frame_m1['time'], unit='s')
                            # print(rates_frame_m1)

                            # Индекс начального бара на М1
                            ind_m1 = 0

                            for _ in rates_m1:

                                if not flag_to_open_pos_m1:

                                    last_high_m1 = rates_m1['high'][ind_m1]
                                    # last_high_m30_next = candle_m30
                                    # print("что жто", price_fractal_up_first)
                                    if last_high_m1 > price_fractal_up_first:

                                        # print(rates_m1['high'][ind_m1], '>', price_fractal_up_first)

                                        flag_to_open_pos_m1 = True  # Отметка о том, что можно искать тиковый вход
                                        time_candle_m1 = rates_m1['time'][ind_m1]
                                        # Значения бара, который пересек линию price_fractal_by
                                        # print("М1 - Open -  ", rates_m1['open'][ind_m1])
                                        # print("М1 - High - ", rates_m1['high'][ind_m1])
                                        # print("М1 - Low - ", rates_m1['low'][ind_m1])
                                        # print("М1 - Close - ", rates_m1['close'][ind_m1])
                                        # print("Время открытия - ", time_candle_m1)
                                        # print("ind_m1", ind_m1)
                                        # ind_m1 - индекс свечи, которая пробила уровень фрактала
                                        time.sleep(1)
                                        # from_date = datetime.fromtimestamp(rates_m1['time'][ind_m1])
                                        flag_to_open_pos_ticks = False
                                        from_date_ticks = datetime.fromtimestamp(time_candle_m1)

                                        rates_ticks = get_ticks_values(symbol, from_date_ticks, to_date)

                                        # ticks_frame = pd.DataFrame(rates_ticks)
                                        # ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')
                                        # print(ticks_frame)

                                        ind_m1 += 1
                                        ind_ticks = 0
                                        ind_ticks_next = 0

                                        tp_buy = price_fractal_up_first + tp
                                        sl_buy = price_fractal_up_first - sl
                                        # print("Тейк-Профит", tp_buy)
                                        # print("Стоп-лосс", sl_buy)

                                        for _ in rates_ticks:
                                            # ind_ticks - индекс тиковых значений

                                            if not flag_to_open_pos_ticks:

                                                last_tick = rates_ticks['last'][ind_ticks]
                                                # ind_ticks_next = ind_ticks

                                                if last_tick > price_fractal_up_first:

                                                    # print("сработал BBBBBBBUUUUUUUYYYYYYY OOORRRRDDDEEEEEERRRRR")

                                                    buy_flag = True

                                                    if buy_flag:

                                                        last_tick_next = rates_ticks['last'][ind_ticks_next]
                                                        # print(last_tick_next)

                                                        if last_tick_next > tp_buy:

                                                            # time.sleep(0)
                                                            # print("Профит", last_tick_next, ">", tp_buy)
                                                            # from_date = rates_ticks['time'][ind_ticks-1]
                                                            ind_ticks_next += 1
                                                            # Отметки о выходе в основной цикл
                                                            ind = ind_n
                                                            profit += tp
                                                            print(profit)
                                                            flag_to_open_pos_ticks = True
                                                            flag_by_fractal_up_search = False
                                                            continue

                                                        elif last_tick_next < sl_buy:
                                                            # time.sleep(0.1)
                                                            # print("Убыток", last_tick, "<", sl_buy)
                                                            ind_ticks_next += 1
                                                            # Отметки о выходе в основной цикл
                                                            ind = ind_n
                                                            profit -= sl
                                                            print(profit)
                                                            flag_to_open_pos_ticks = True
                                                            flag_by_fractal_up_search = False
                                                            continue

                                                        else:
                                                            ind_ticks_next += 1
                                                        flag_by_fractal_up_search = False
                                                        # ind += 1

                                                else:
                                                    ind_ticks += 1
                                    else:
                                        ind_m1 += 1
                        else:
                            ind_n += 1
            else:
                ind += 1
        else:
            ind += 1
            flag_by_fractal_up_search = False


#                 # Флаг условия перебора свечей на таймфрейме М1
#                 flag_to_open_pos_m1 = False
#
#                 # Изменение периода выборки для таймфрейма М1 (начало выборки = моменту обнаружения фрактала)
#                 # Приходится прибавить 3 30-минутные свечи. Пока не понятно почему.
#                 from_date_m1 = datetime.fromtimestamp(time_fractal_up_first + 60*30*3)
#
#                 # print(from_date_m1)
#                 # print(datetime.timestamp(from_date_m1))
#                 # print(to_date)
#
#                 rates_m1 = get_value_bars_m1_timeframe(symbol, from_date_m1, to_date)
#
#                 # print(rates_m1)
#                 # rates_frame_m1 = pd.DataFrame(rates_m1)
#                 # rates_frame_m1['time'] = pd.to_datetime(rates_frame_m1['time'], unit='s')
#                 # print(rates_frame_m1)
#
#                 # Переход к следующему бару на М30
#                 ind += 1
#                 # Индекс начального бара на М1
#                 ind_m1 = 0
#
#                 for _ in rates_m1:
#
#                     if not flag_to_open_pos_m1:
#
#                         last_high_m1 = rates_m1['high'][ind_m1]
#                         # last_high_m30_next = candle_m30
#                         print(rates['high'][ind])
#                         if last_high_m1 > price_fractal_up_first:
#
#                             # print(rates_m1['high'][ind_m1], '>', price_fractal_up_first)
#
#                             flag_to_open_pos_m1 = True  # Отметка о том, что можно искать тиковый вход
#                             time_candle_m1 = rates_m1['time'][ind_m1]
#                             # Значения бара, который пересек линию price_fractal_by
#                             print("М1 - Open -  ", rates_m1['open'][ind_m1])
#                             print("М1 - High - ", rates_m1['high'][ind_m1])
#                             print("М1 - Low - ", rates_m1['low'][ind_m1])
#                             print("М1 - Close - ", rates_m1['close'][ind_m1])
#                             print("Время открытия - ", time_candle_m1)
#                             # ind_m1 - индекс свечи, которая пробила уровень фрактала
#                             time.sleep(1)
#                             # from_date = datetime.fromtimestamp(rates_m1['time'][ind_m1])
#                             flag_to_open_pos_ticks = False
#                             from_date_ticks = datetime.fromtimestamp(time_candle_m1)
#
#                             rates_ticks = get_ticks_values(symbol, from_date_ticks, to_date)
#
#                             # ticks_frame = pd.DataFrame(rates_ticks)
#                             # ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')
#                             # print(ticks_frame)
#
#                             ind_m1 += 1
#                             ind_ticks = 0
#
#                             tp_buy = price_fractal_up_first + tp
#                             sl_buy = price_fractal_up_first - sl
#                             print("Тейк-Профит", tp_buy)
#                             print("Стоп-лосс", sl_buy)
#
#                             for _ in rates_ticks:
#                                 # ind_ticks - индекс тиковых значений
#
#                                 if not flag_to_open_pos_ticks:
#
#                                     last_tick = rates_ticks['last'][ind_ticks]
#
#                                     if last_tick > price_fractal_up_first:
#
#                                         last_price_to_ticks = rates_ticks['last'][ind_ticks]
#                                         print("Тик - ", last_price_to_ticks)
#                                         time.sleep(0)
#
#                                         if last_tick > tp_buy:
#
#                                             time.sleep(1)
#                                             print("Профит", last_tick, ">", tp_buy)
#                                             # from_date = rates_ticks['time'][ind_ticks-1]
#                                             ind_ticks += 1
#                                             flag_to_open_pos_ticks = True  # Отметка о том, что мы в позиции на тиковых данных
#
#                                         elif rates_ticks['last'][ind_ticks] < sl_buy:
#
#                                             time.sleep(1)
#                                             print("Убыток", rates_ticks['last'][ind_ticks - 1], "<", sl_buy)
#                                             ind_ticks += 1
#                                             flag_to_open_pos_ticks = True  # Отметка о том, что мы в позиции на тиковых данных
#                                         else:
#                                             ind_ticks += 1
#                                         ind_ticks += 1
#                                         flag_by_fractal_up_search = False
#
#                                     else:
#                                         ind_ticks += 1
#                         # elif for
#                         #
#                         #     print("Место для поиска!!!!!!")
#                         #     # print(rates_m1['high'][ind_m1])
#                         else:
#                             ind_m1 += 1
#             else:
#                 ind += 1
#
#
print(fractal_up_search(ind=2))
