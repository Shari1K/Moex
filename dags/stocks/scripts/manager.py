import logging
from airflow.exceptions import AirflowFailException
from stocks.scripts.api import fetch_data_from_yfinance
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow_clickhouse_plugin.hooks.clickhouse import ClickHouseHook


def data_to_pg(stock, **kwargs):
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
    # target_fields = data.columns.tolist()
    try:
        postgresHook = PostgresHook(postgres_conn_id="pg_1")
        postgresHook.insert_rows(table="stocks", rows=rows,
                                 target_fields=["ticker", "date", "close", "high", "low", "open", "volume"])
        # postgresHook.insert_rows(table="stocks", rows=rows,
        #                          target_fields=target_fields)
    except Exception as e:
        logging.info(rows)
        raise AirflowFailException("Ошибка")
    return data.to_json(f"{stock}_{data_interval_start.strftime('%Y-%m-%d')}.json")


def data_to_click(**kwargs):
    data_interval_start = kwargs["data_interval_start"]
    execution_date = data_interval_start.strftime('%Y-%m-%d')
    query = f"""
    INSERT INTO stock_2
    SELECT * FROM PG_to_Click
    WHERE date = toDate('{execution_date}')
    """
    hook = ClickHouseHook(clickhouse_conn_id="clickhouse_default")
    try:
        result = hook.execute(query)
        logging.info(f"Запрос выполнен успешно. Результат: {result}")
        return f"Загружено данных за {execution_date}: {result}"
    except Exception as e:
        logging.error(f"Ошибка при загрузке данных: {str(e)}")
        raise