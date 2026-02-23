import logging
from datetime import timedelta
import yfinance as yf


def fetch_data_from_yfinance(stock, **context):
    start = (context["data_interval_start"] - timedelta(days=1)).strftime('%Y-%m-%d')
    end = context["data_interval_end"].strftime('%Y-%m-%d')
    df = yf.download(stock, start=start, end=end)
    # logging.info(f'''Выгрузилось
    # __________________________
    # {df}
    # __________________________
    # ''')
    # # df = df.loc[start:start + timedelta(days=1)]
    # logging.info(f"start={start}, end={end}")
    # logging.info(f'''Стало
    # __________________________
    # {df}
    # __________________________
    # ''')
    logging.info(f"print_api {df}")
    return df
