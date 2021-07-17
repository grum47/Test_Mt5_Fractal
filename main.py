from datetime import datetime
import time

import MetaTrader5 as mt5
import pandas as pd
import pytz

# Настройки тайм-зоны и датафреймов для показа (потом можно будет удалить)
timezone = pytz.timezone("Etc/UTC")
pd.set_option('display.max_columns', 500)  # Количество столбцов
pd.set_option('display.max_rows', 1000)  # Количество строк
pd.set_option('display.width', 1500)  # Макс. ширина таблицы для показа

# Устанавливаем соединение с терминалом MetaTrader 5
# Вызов без параметров. Терминал для подключения будет найден автоматически. Предварительно надо подключитсья к счету.
# Если несколько счетов, то надо переписать:
"""mt5.initialize(
   path,                     // путь к EXE-файлу терминала MetaTrader 5
   login=LOGIN,              // номер счета
   password="PASSWORD",      // пароль
   server="SERVER",          // имя сервера, как оно задано в терминале
   timeout=TIMEOUT,          // таймаут
   portable=False            // режим portable
   )"""
mt5.initialize()
if not mt5.initialize():
    print("Инициализация не прошла. Ошибка - ", mt5.last_error())
    quit()

# Задаем параметры для тестирования (потом сделать интерфейс):
# Финансовый инструмент
symbol_name = "Si-9.21"
# Размер Тейк-профит
tp = 450
# Размер Стоп-лосс
sl = 150

# Рабочий таймфрейм
frame = mt5.TIMEFRAME_M30
# Таймфрейм для работы по минутам (не меняем)
frame_m1 = mt5.TIMEFRAME_M1
# Тип запрашиваемых тиков (не меняем)
flags = mt5.COPY_TICKS_INFO

# Размер фрактала (5, 7, 9, 11 и т.д. свечей)
...

# Диапазон тестирования
# дата, с которой запрашиваются бары (год, месяц, день, час) возможно потом добавим минуты
from_date = datetime(2021, 5, 1, 10, tzinfo=timezone)
# дата, по которую запрашиваются бары (год, месяц, день) возможно потом добавим часы и минуты
to_date = datetime(2021, 7, 12, tzinfo=timezone)

# Печатаем информацию (после того, как сделаем интерфейс можно удалить)
print(f'Торгуемый инструмент - {symbol_name}')
print(f'Рабочий таймфрейм - {frame}')
print(f'От - {from_date}')
print(f'До - {to_date}')


# Функция получения баров в указанном диапазоне дат из терминала MetaTrader 5 по рабочему таймфрейму
def get_value_bars_main_timeframe(symbol_name, frame, from_date, to_date):
    """
    :param symbol_name: Имя финансового инструмента
    :param frame: Таймфрейм, для которого запрашиваются бары
    :param from_date: Дата, начиная с которой запрашиваются бары. Задается объектом datetime или в виде количества
            секунд, прошедших с 1970.01.01. Отдаются бары со временем открытия >= date_from
    :param to_date: Дата, по которую запрашиваются бары. Задается объектом datetime или в виде количества
            секунд, прошедших  с 1970.01.01. Отдаются бары со временем открытия <= date_to
    :return: Возвращает бары в виде массива numpy с именованными столбцами time, open, high, low, close, tick_volume,
            spread и real_volume. В случае ошибки возвращает None
    """

    bar_values = mt5.copy_rates_range(symbol_name, frame, from_date, to_date)
    return bar_values


# Функция Получения баров из терминала MetaTrader 5, начиная с указанной даты.
# НЕ ИСПОЛЬЗУЕТСЯ
def get_one_bars_main_timeframe(symbol_name, frame, from_date, count):
    """
    :param symbol_name: Имя финансового инструмента
    :param frame: Таймфрейм, для которого запрашиваются бары
    :param from_date: Дата открытия первого бара из запрашиваемой выборки.
                        Задается объектом datetime или в виде количества секунд, прошедших с 1970.01.01
    :param count: Количество баров, которое необходимо получить
    :return: Возвращает бары в виде массива numpy с именованными столбцами time, open, high, low, close, tick_volume,
            spread и real_volume. В случае ошибки возвращает None
    """

    bar_values = mt5.copy_rates_from(symbol_name, frame, from_date, count)
    return bar_values[0][2]


# Функция получения баров в указанном диапазоне дат из терминала MetaTrader 5 таймфрейму М1
def get_value_bars_m1_timeframe(symbol_name, frame_m1, from_date, to_date):
    """
    :param symbol_name: Имя финансового инструмента
    :param frame_m1: Таймфрейм, для которого запрашиваются бары (в данной функции только М1 - это необходимо для
                    большей точности в тестировании)
    :param from_date: Дата, начиная с которой запрашиваются бары. Задается объектом datetime или в виде количества
            секунд, прошедших с 1970.01.01. Отдаются бары со временем открытия >= date_from
    :param to_date: Дата, по которую запрашиваются бары. Задается объектом datetime или в виде количества
            секунд, прошедших  с 1970.01.01. Отдаются бары со временем открытия <= date_to
    :return: Возвращает бары в виде массива numpy с именованными столбцами time, open, high, low, close, tick_volume,
            spread и real_volume. В случае ошибки возвращает None
    """

    bar_values_m1 = mt5.copy_rates_range(symbol_name, frame_m1, from_date, to_date)
    return bar_values_m1


# Функция получения тиков в указанном диапазоне дат из терминала MetaTrader 5
def get_ticks_values(symbol_name, from_date, to_date, flags):
    """
    :param symbol_name: Имя финансового инструмента
    :param from_date: Дата, начиная с которой запрашиваются бары. Задается объектом datetime или в виде количества
            секунд, прошедших с 1970.01.01
    :param to_date: Дата, по которую запрашиваются бары. Задается объектом datetime или в виде количества
            секунд, прошедших  с 1970.01.01
    :param flags: Флаг, определяющий тип запрашиваемых тиков.
                COPY_TICKS_INFO – тики, вызванные изменениями Bid и/или Ask,
                COPY_TICKS_TRADE – тики с изменения Last и Volume,
                COPY_TICKS_ALL – все тики
    :return: Возвращает значения тиков за период от from_date до to_date
    """

    ticks_values = mt5.copy_ticks_range(symbol_name, from_date, to_date, flags)
    return ticks_values


# Переназначаем переменные для упрощения написания дальнейших функций

# candle_m30 = get_one_bars_main_timeframe(symbol_name, frame, from_date, to_date)
rates = get_value_bars_main_timeframe(symbol_name, frame, from_date, to_date)
rates_m1 = get_value_bars_m1_timeframe(symbol_name, from_date, to_date)
rates_ticks = get_ticks_values(symbol_name, from_date, to_date)


# Выводим на печать массив значений баров в виде таблицы

# print(candle_m30)

# rates_frame = pd.DataFrame(rates)
# rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
# print(rates_frame)

# rates_frame_m1 = pd.DataFrame(rates_m1)
# rates_frame_m1['time'] = pd.to_datetime(rates_frame_m1['time'], unit='s')
# print(rates_frame_m1)

# ticks_frame = pd.DataFrame(get_ticks_values(symbol_name, from_date, to_date))
# ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')
# print(ticks_frame)


def fractal_up_search(ind, tp, sl):
    """
    :param sl: Значение Стоп-лосс
    :param tp: Значение Тейк-профит
    :param ind: Значение индекса столбца HIGH
    :return:
    """
    flag_by_fractal_up_search = False
    # Начинаем перебор баров исторического периода
    print(f'Тейк-профит = {tp}')
    print(f'Стоп-лосс = {sl}')

    profit = 0
    for _ in get_value_bars_main_timeframe(symbol_name, frame, from_date, to_date):

        # now_time = '10:30'  # время выставления ордеров
        # print(f'now_time - {now_time}')
        # sleep_from = int('10')  # Время начала работы (часы)
        # print(f'sleep_from - {sleep_from}')
        # sleep_from_m = int('00')  # Время начала работы (минуты)
        # print(f'sleep_from_m - {sleep_from_m}')
        # sleep_to = int('18')  # Время окончания работы (часы)
        # print(f'sleep_to - {sleep_to}')
        # sleep_to_m = int('00')  # Время окончания работы (минуты)
        # print(f'sleep_to_m - {sleep_to_m}')

        ti = time.strftime('%H:%M', time.localtime(rates['time'][ind] - 60 * 60 * 3))
        print(f'Время = {ti}')

        h = int(ti.split(':')[0])
        m = int(ti.split(':')[1])
        # print(f'Time {h}:{m}')

        # while True:
        #     ti = time.strftime('%H:%M', time.localtime(time.time()))
        #     h = int(ti.split(':')[0])
        #     m = int(ti.split(':')[1])
        #     # if int(now_time.split(':')[0])==9 and int(now_time.split(':')[1])>44:
        #     if h == 9 and m > 44:
        #         flag_for_current_candle = True
        #     if ti == now_time:
        #         time.sleep(1)

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
                print("----- Первый фрактал -----", price_fractal_up_first)
                # time.sleep(1)
                # ind += 1
                # print("ind", ind)
                ind = ind + 1
                # print("ind", ind)
                flag_by_fractal_up_search = True
                # from_date_next_fractal = time_fractal_up_first

                for _ in get_value_bars_main_timeframe(symbol_name, frame, from_date, to_date):

                    if flag_by_fractal_up_search:

                        last_high_m30_next = rates['high'][ind]
                        # print("last_high_m30_next", last_high_m30_next)

                        if last_high_m30_next > rates['high'][ind - 1] and \
                                last_high_m30_next > rates['high'][ind - 2] and \
                                last_high_m30_next >= rates['high'][ind + 1] and \
                                last_high_m30_next >= rates['high'][ind + 2]:

                            print("===== Новый фрактал ====== переставление ", last_high_m30_next)
                            # print('ind', ind)
                            ind += 1
                            # print('ind', ind)
                            flag_by_next_fractal_up_search = True
                            # flag_by_fractal_up_search = False
                            price_fractal_up_first = last_high_m30_next
                            # print("price_fractal_up_first =============================", price_fractal_up_first)

                        elif last_high_m30_next > price_fractal_up_first:
                            tp_buy = price_fractal_up_first + tp
                            sl_buy = price_fractal_up_first - sl

                            flag_close = False
                            ind_open = ind
                            ind_clos = ind

                            # Значения бара, который пересек линию price_fractal_up_first
                            # print("Бар открытия:::::::::::::::::::::::::::::::")
                            # print("М15 - Open -  ", rates['open'][ind])
                            # print("М15 - High - ", rates['high'][ind])
                            # print("М15 - Low - ", rates['low'][ind])
                            # print("М15 - Close - ", rates['close'][ind])
                            # print("Время открытия - ", rates['time'][ind])

                            for _ in get_value_bars_main_timeframe(symbol_name, frame, from_date, to_date):

                                if not flag_close:

                                    closing_order_price = rates['high'][ind_clos]
                                    # print(ind_clos, closing_order_price)
                                    time.sleep(0)
                                    if closing_order_price > tp_buy:
                                        # ind_clos += 1
                                        # print('Закрытие по TP. Индекс бара закрытия ===============', ind_clos)
                                        flag_close = True
                                        ind = ind_clos
                                    elif closing_order_price < sl_buy:
                                        # ind_clos += 1
                                        # print('Закрытие по SL. Индекс бара закрытия ===============', ind_clos)
                                        flag_close = True
                                        ind = ind_clos
                                    else:
                                        ind_clos += 1
                                        flag_close = False

                            print("----- пересечение уровня фрактала -----")
                            # ind += 1
                            time_fractal_up_first = rates['time'][ind_open]

                            # flag_by_fractal_up_search = False

                            # Флаг условия перебора свечей на таймфрейме М1
                            flag_to_open_pos_m1 = False

                            # Изменение периода выборки для таймфрейма М1
                            # (начало выборки = моменту обнаружения фрактала)
                            # Приходится прибавить 3 30-минутные свечи. Пока не понятно почему.
                            from_date_m1 = datetime.fromtimestamp(time_fractal_up_first)
                            # print(from_date_m1)
                            # print(datetime.timestamp(from_date_m1))
                            # print(to_date)

                            rates_m1 = get_value_bars_m1_timeframe(symbol_name, from_date_m1, to_date)

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
                                        # print("Время открытия - ", datetime.fromtimestamp(time_candle_m1))
                                        # print("ind_m1", ind_m1)
                                        # ind_m1 - индекс свечи, которая пробила уровень фрактала
                                        # time.sleep(0)
                                        # from_date = datetime.fromtimestamp(rates_m1['time'][ind_m1])
                                        flag_to_open_pos_ticks = False
                                        from_date_ticks = datetime.fromtimestamp(time_candle_m1)

                                        rates_ticks = get_ticks_values(symbol_name, from_date_ticks, to_date)

                                        # ticks_frame = pd.DataFrame(rates_ticks)
                                        # ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')
                                        # print(ticks_frame)

                                        ind_m1 += 1
                                        ind_ticks = 0
                                        ind_ticks_next = 0

                                        print("Тейк-Профит", tp_buy)
                                        print("Стоп-лосс", sl_buy)

                                        for _ in rates_ticks:
                                            # ind_ticks - индекс тиковых значений

                                            if not flag_to_open_pos_ticks:

                                                last_tick = rates_ticks['last'][ind_ticks]
                                                # ind_ticks_next = ind_ticks

                                                if last_tick > price_fractal_up_first:

                                                    buy_flag = True

                                                    if buy_flag:

                                                        last_tick_next = rates_ticks['last'][ind_ticks_next]
                                                        # time_tick_next = datetime.fromtimestamp(
                                                        # rates_ticks['time'][ind_ticks_next])

                                                        # print('Тик', last_tick_next, 'Время', time_tick_next)
                                                        # time.sleep(0)
                                                        # print(datetime.fromtimestamp(rates_ticks['time'][ind_ticks_next]))

                                                        # time.sleep(0)

                                                        if last_tick_next > tp_buy:

                                                            # time.sleep(0)
                                                            print("Профит", last_tick_next, ">", tp_buy)
                                                            # print(ind)
                                                            # from_date = rates_ticks['time'][ind_ticks-1]
                                                            ind_ticks_next += 1
                                                            # Отметки о выходе в основной цикл
                                                            profit += tp
                                                            print('ПРОФИТ = ', profit)
                                                            flag_to_open_pos_ticks = True
                                                            flag_by_fractal_up_search = False
                                                            print(datetime.fromtimestamp(
                                                                rates_ticks['time'][ind_ticks_next] - 60 * 60 * 3))
                                                            # time.sleep(0)
                                                            continue

                                                        elif last_tick_next == 0.0:
                                                            # print('ПИЗДЕЦ НАХУЙ 0!!!!!!!!!!!!!! КАРЛ!!!!!!')
                                                            ind_ticks_next += 1
                                                            continue

                                                        elif last_tick_next < sl_buy:
                                                            # time.sleep(0.1)
                                                            print("Убыток", last_tick_next, "<", sl_buy)
                                                            ind_ticks_next += 1
                                                            # Отметки о выходе в основной цикл
                                                            profit -= sl
                                                            print('ПРОФИТ = ', profit)
                                                            flag_to_open_pos_ticks = True
                                                            flag_by_fractal_up_search = False
                                                            print(datetime.fromtimestamp(
                                                                rates_ticks['time'][ind_ticks_next] - 60 * 60 * 3))
                                                            # time.sleep(5)
                                                            continue

                                                        else:
                                                            ind_ticks_next += 1
                                                        flag_by_fractal_up_search = False
                                                else:
                                                    ind_ticks += 1
                                    else:
                                        ind_m1 += 1
                        else:
                            ind += 1
            else:
                ind += 1
        else:
            ind += 1
            flag_by_fractal_up_search = False


print(fractal_up_search(2, tp, sl))
