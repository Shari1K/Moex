import logging
from airflow.exceptions import AirflowFailException


from stocks.scripts.api import fetch_data_from_yfinance
from airflow.providers.postgres.hooks.postgres import PostgresHook


def fetch_data(stock, **kwargs):
    data_interval_start = kwargs["data_interval_start"].replace(tzinfo=None)
    data_interval_end = kwargs["data_interval_end"].replace(tzinfo=None)

    data = fetch_data_from_yfinance(stock, data_interval_start=data_interval_start, data_interval_end=data_interval_end)
    data = data.loc[data_interval_start:data_interval_start]
    data.reset_index(inplace=True)
    data.columns = data.columns.get_level_values(0)
    data.columns = [c.lower() for c in data.columns]
    data["ticker"] = stock
    data = data[["ticker", "date", "close", "high", "low", "open", "volume"]]
    rows = data.values.tolist()
    target_fields = data.columns.tolist()
    try:
        postgresHook = PostgresHook(postgres_conn_id="pg_1")
        postgresHook.insert_rows(table="stocks", rows=rows,
                                 target_fields=["ticker", "date", "close", "high", "low", "open", "volume"])
        # postgresHook.insert_rows(table="stocks", rows=rows,
        #                          target_fields=target_fields)
    except Exception as e:
        logging.info(rows)
        raise AirflowFailException("ошибка")
    return data.to_json(f"{stock}_{data_interval_start.strftime('%Y-%m-%d')}.json")




