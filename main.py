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
    from_date = datetime(2021, 1, 25, 10)
    to_date = datetime(2021, 1, 30)
    rates = mt5.copy_rates_range(symbol, frame, from_date, to_date)
    return rates


rates_frame = pd.DataFrame(get_rates())
print(rates_frame)