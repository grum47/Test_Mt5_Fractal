from datetime import datetime
import functools


import MetaTrader5 as mt5
import pandas as pd
import pytz

# Настройки тайм-зоны и датафреймов для показа (потом можно будет удалить)
timezone = pytz.timezone("Etc/UTC")
pd.set_option('display.max_columns', 15)  # Количество столбцов
pd.set_option('display.max_rows', 1500)  # Количество строк
pd.set_option('display.width', 500)  # Макс. ширина таблицы для показа

"""Устанавливаем соединение с терминалом MetaTrader 5
Вызов без параметров. Терминал для подключения будет найден автоматически. Предварительно надо подключитсья к счету.
Если несколько счетов, то надо переписать:
mt5.initialize(
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

"""Задаем параметры для тестирования (потом сделать интерфейс)"""
symbol_name = "Si-9.21"                                 # финансовый инструмент
from_date = datetime(2021, 5, 10, 17, tzinfo=timezone)  # дата, с которой запрашиваются бары (год, месяц, день, час)
to_date = datetime(2021, 7, 10, tzinfo=timezone)        # дата, по которую запрашиваются бары (год, месяц, день)
tp = 450                                                # размер Тейк-профит
sl = 150                                                # размер Стоп-лосс
frame = mt5.TIMEFRAME_M30                               # рабочий таймфрейм
frame_m1 = mt5.TIMEFRAME_M1                             # таймфрейм для работы по минутам (не меняем)
flags = mt5.COPY_TICKS_INFO                             # тип запрашиваемых тиков (не меняем)
...                                                     # Размер фрактала (5, 7, 9, 11 и т.д. свечей)

"""Печатаем информацию (после того, как сделаем интерфейс можно удалить)"""
print(f'Торгуемый инструмент - {symbol_name}')
print(f'Рабочий таймфрейм - {frame}')
print(f'От - {from_date}')
print(f'До - {to_date}')


def runtime_calculation(func):
    """
    Функция-декоратор для подсчета времени выполнения другой функции.
    :param func:
    :return:
    """
    import time
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        res = func(*args, **kwargs)
        end_time = time.monotonic()
        print(f'Прошло времени - {round((end_time - start_time), 4)} сек.')
        return res
    return wrapper


@runtime_calculation
def get_value_bars_main_timeframe(symbol_name, frame, from_date, to_date):
    """
    Функция получения баров в указанном диапазоне дат из терминала MetaTrader 5 по рабочему таймфрейму
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
    if bar_values is None:
        print(mt5.last_error())
    else:
        print(bar_values)
        return bar_values


def get_one_bars_main_timeframe(symbol_name, frame, from_date, count):
    """
    Функция Получения баров из терминала MetaTrader 5, начиная с указанной даты.
    НЕ ИСПОЛЬЗУЕТСЯ
    :param symbol_name: Имя финансового инструмента
    :param frame: Таймфрейм, для которого запрашиваются бары
    :param from_date: Дата открытия первого бара из запрашиваемой выборки.
                        Задается объектом datetime или в виде количества секунд, прошедших с 1970.01.01
    :param count: Количество баров, которое необходимо получить
    :return: Возвращает бары в виде массива numpy с именованными столбцами time, open, high, low, close, tick_volume,
            spread и real_volume. В случае ошибки возвращает None
    """

    bar_values = mt5.copy_rates_from(symbol_name, frame, from_date, count)
    if bar_values is None:
        print(mt5.last_error())
    else:
        print(bar_values)
        return bar_values[0][2]


@functools.lru_cache(maxsize=None)
@runtime_calculation
def get_value_bars_m1_timeframe(symbol_name, frame_m1, from_date, to_date):
    """
    Функция получения баров в указанном диапазоне дат из терминала MetaTrader 5 таймфрейм М1
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
    if bar_values_m1 is None:
        print(mt5.last_error())
    else:
        return bar_values_m1


@functools.lru_cache(maxsize=None)
@runtime_calculation
def get_ticks_values(symbol_name, from_date, to_date, flags):
    """
    Функция получения тиков в указанном диапазоне дат из терминала MetaTrader 5
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
    if ticks_values is None:
        print(mt5.last_error())
    else:
        return ticks_values


def fractal_detection_up(symbol_name, frame, from_date, to_date):
    """
    Функция определения фрактала на рабочем таймфрейме (5 свечей)
    :param symbol_name: Имя финансового инструмента
    :param frame:
    :param from_date:
    :param to_date:
    :return:
    """
    flag_by_fractal_detection_up = False                                   # Флаг определения бара как вершины фрактала
    for bars in get_value_bars_main_timeframe(symbol_name, frame, from_date, to_date):  # Перебираем бары на рабочем ТФ
        if not flag_by_fractal_detection_up:
            ...

# Функция тестирования
def tester():
    ...


# Область вызова функций

#print(pd.DataFrame(get_ticks_values(symbol_name, from_date, to_date, flags)))
#print(pd.DataFrame(mt5.copy_ticks_range(symbol_name, from_date, to_date, flags)))
#get_value_bars_main_timeframe(symbol_name, frame, from_date, to_date)
