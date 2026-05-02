from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
import json
from datetime import datetime
from stocks.scripts.manager import Extract, Load
from stocks.config import TICKERS

# BASE_DIR = os.path.dirname(__file__)
# CFG_PATH = os.path.join(BASE_DIR, "cfg.yaml")
#
#
# with open(CFG_PATH) as f:
#     config = yaml.safe_load(f)
#
# stocks = config["data"]["stock"]

default_args = {
    "owner": "airflow",
    # "depends_on_past": True,
    # "start_date": datetime(2026, 1, 1),
    # "end_date": datetime(2026, 1, 7),
    # "schedule": "@daily"
}

with DAG(
        dag_id="dag_moex",
        default_args=default_args,
        max_active_runs=1,
        # start_date=datetime(2025, 12, 1),
        # end_date=datetime(2025, 12, 3),
        start_date=datetime(2026, 2, 4),
        end_date=datetime(2026, 2, 27),
        schedule="0 0 * * 1-5",
        catchup=True
) as dag:
    start = EmptyOperator(
        task_id=f"task_start")

    extract = []
    for stock in TICKERS:
        unload = PythonOperator(
            task_id=f"task_{stock}",
            python_callable=Extract,
            op_kwargs={"stock": stock}
        )
        extract.append(unload)

    load = PythonOperator(
        task_id=f"task_load_to_click",
        python_callable=Load,
    )

    end = EmptyOperator(
        task_id=f"task_end")

    start >> extract >> load >>end