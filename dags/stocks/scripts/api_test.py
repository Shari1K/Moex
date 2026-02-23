import sys

import yfinance as yf
from datetime import date, timedelta

data_start = date(2026, 1, 8)
days = 1

for day in range(days):
    data_interval_start = data_start + timedelta(days=day-1)
    data_interval_end = data_start + timedelta(days=day+1)
    print(data_interval_start, '    ', data_interval_end - timedelta(days=1))
    stock = yf.download("TSLA", start=data_interval_start, end=data_interval_end)
    # print(stock, end='\n'+'_'*100+'\n')
    # sys.exit()
    stock = stock.loc[data_interval_end - timedelta(days=1):data_interval_end - timedelta(days=1)]
    stock.reset_index(inplace=True)
    stock.columns = stock.columns.get_level_values(0)
    stock.columns = [c.lower() for c in stock.columns]
    stock["ticker"] = "TSLA"
    stock = stock[["ticker", "date", "close", "high", "low", "open", "volume"]]
    print(stock, end='\n'+'_'*100+'\n')


# data_interval_start = date(2026, 1, 1)
# data_interval_end = date(2026, 2, 22)
# stock = yf.download("TSLA", start=data_interval_start, end=data_interval_end)
# print(stock)
