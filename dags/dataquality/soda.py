import logging
from airflow.operators.bash import BashOperator

logger = logging.getLogger(__name__)

# Constant variable
SODA_PATH = "/opt/airflow/include/soda"
DATASOURCE = "my_datasource_pg"

# Func to exec soda scan for data quality
def yt_elt_data_quality(schema):
    try:
        task = BashOperator(
            task_id = f"soda_test_{schema}",
            bash_command = f"soda scan -d {DATASOURCE} -c {SODA_PATH}/configuration.yaml -v SCHEMA={schema} {SODA_PATH}/checks.yaml",
        )
        return task
    except Exception as e:
        logger.error(f"Error running data quality check for schema: {schema}")
        raise e

