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
to_date = datetime(2021, 1, 30, tzinfo=timezone)
print(to_date)
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


# def last_index():
#     """
#
#     :return: Возвращает индекс 0-го бара с начала массива
#
#     """
#     return len(get_value_bars_main_timeframe(symbol, frame, from_date, to_date)) - len(
#         get_value_bars_main_timeframe(symbol, frame, from_date, to_date))


# Переназначаем переменные для упрощения написания дальнейших функций

rates = get_value_bars_main_timeframe(symbol, frame, from_date, to_date)
rates_m1 = get_value_bars_m1_timeframe(symbol, from_date, to_date)
rates_ticks = get_ticks_values(symbol, from_date, to_date)


# Выводим на печать массив значений баров в виде таблицы

# rates_frame = pd.DataFrame(rates)
# rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
# print(rates_frame)

# rates_frame_m1 = pd.DataFrame(rates_m1)
# rates_frame_m1['time'] = pd.to_datetime(rates_frame_m1['time'], unit='s')
# print(rates_frame_m1)

# ticks_frame = pd.DataFrame(get_ticks_values(symbol, from_date, to_date))
# ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')
# print(ticks_frame)


def fractal_up(ind=2, tp=15, sl=60):
    """
    :param sl: Значение Стоп-лосс
    :param tp: Значение Тейк-профит
    :param ind: Значение индекса столбца HIGH
    :return:
    """
    flag_by_fractal_up = False
    # Начинаем перебор баров исторического периода
    for _ in rates:

        if not flag_by_fractal_up:

            # Условие определения фрактала ВВЕРХ
            if rates['high'][ind] > rates['high'][ind - 1] and \
                    rates['high'][ind] > rates['high'][ind - 2] and \
                    rates['high'][ind] >= rates['high'][ind + 1] and \
                    rates['high'][ind] >= rates['high'][ind + 2]:

                flag_by_fractal_up = True
                price_fractal_up = rates['high'][ind]
                time_fractal_up = rates['time'][ind]
                print("Есть фрактал вверх. Точка фрактала = ", price_fractal_up)
                # print(time_fractal_up)
                # print("Время фрактала, примерно - ", datetime.fromtimestamp(time_fractal_up - 60*60*3))
                # print("Время фрактала, примерно - ", datetime.fromtimestamp(time_fractal_up))
                time.sleep(1)

                # Флаг условия перебора свечей на таймфрейме М1
                flag_to_open_pos_m1 = False

                # Изменение периода выборки для таймфрейма М1 (начало выборки = моменту обнаружения фрактала)
                # Приходится прибавить 3 30-минутные свечи. Пока не понятно почему.
                from_date_m1 = datetime.fromtimestamp(time_fractal_up + 60*30*3)

                # print(from_date_m1)
                # print(datetime.timestamp(from_date_m1))
                # print(to_date)

                rates_m1 = get_value_bars_m1_timeframe(symbol, from_date_m1, to_date)

                # print(rates_m1)
                # rates_frame_m1 = pd.DataFrame(rates_m1)
                # rates_frame_m1['time'] = pd.to_datetime(rates_frame_m1['time'], unit='s')
                # print(rates_frame_m1)

                # Переход к следующему бару на М30
                ind += 1
                # Индекс начального бара на М1
                ind_m1 = 0

                for _ in rates_m1:

                    if not flag_to_open_pos_m1:
                        # Используется ind-1, т.к. мы уже находимся на следующей свече и максимум сместился на -1
                        if rates_m1['high'][ind_m1] > price_fractal_up:

                            # print(rates_m1['high'][ind_m1], '>', price_fractal_up)

                            flag_to_open_pos_m1 = True  # Отметка о том, что можно искать тиковый вход
                            time_candle_m1 = rates_m1['time'][ind_m1]
                            # Значения бара, который пересек линию price_fractal_by
                            print("М1 - Open -  ", rates_m1['open'][ind_m1])
                            print("М1 - High - ", rates_m1['high'][ind_m1])
                            print("М1 - Low - ", rates_m1['low'][ind_m1])
                            print("М1 - Close - ", rates_m1['close'][ind_m1])
                            print("Время открытия - ", time_candle_m1)
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

                            tp_buy = price_fractal_up + tp
                            sl_buy = price_fractal_up - sl
                            print("Тейк-Профит", tp_buy)
                            print("Стоп-лосс", sl_buy)

                            for _ in rates_ticks:
                                # ind_ticks - индекс тиковых значений

                                if not flag_to_open_pos_ticks:
                                    # print(rates_ticks['last'][ind_ticks])
                                    # print(rates['high'][ind-1])

                                    if rates_ticks['last'][ind_ticks] > price_fractal_up:

                                        last_price_to_ticks = rates_ticks['last'][ind_ticks]
                                        print("Пересечение на тиковом Графике", last_price_to_ticks)
                                        # print(*rates_ticks['last'], sep="\n")
                                        time.sleep(0)
                                        ind_ticks += 1

                                        if rates_ticks['last'][ind_ticks - 1] > tp_buy:

                                            time.sleep(1)
                                            print("Профит", rates_ticks['last'][ind_ticks - 1], ">", tp_buy)
                                            # from_date = rates_ticks['time'][ind_ticks-1]
                                            ind_ticks += 1
                                            flag_to_open_pos_ticks = True  # Отметка о том, что мы в позиции на тиковых данных

                                        elif rates_ticks['last'][ind_ticks] < sl_buy:

                                            time.sleep(1)
                                            print("Убыток", rates_ticks['last'][ind_ticks - 1], "<", sl_buy)
                                            ind_ticks += 1
                                            flag_to_open_pos_ticks = True  # Отметка о том, что мы в позиции на тиковых данных
                                        else:
                                            ind_ticks += 1

                                        flag_by_fractal_up = False

                                    else:
                                        ind_ticks += 1

                        else:
                            ind_m1 += 1
                            # print(rates_m1['high'][ind_m1])
            else:
                ind += 1


print(fractal_up(ind=2))
