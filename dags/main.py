from airflow import DAG
import pendulum
from datetime import datetime, timedelta
# import the trigger dag operator. used to trigger the next dag upon succeed of previous dag
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
#import get_playlist_id, get_video_id, extract_video_data and save_to_json
from api.video_stats import (
    get_playlist_id, 
    get_videos_id, 
    extract_video_data, 
    save_to_json
)

# import DWH modules
from datawarehouse.dwh import staging_table, core_table

# import data quality
from dataquality.soda import yt_elt_data_quality

# Define then local timezone
local_tz = pendulum.timezone("America/New_York")

# Default Args
default_args = {
    "owner": "jonotech Solutions",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "jonotechsolutions@gmail.com",
    "max_action_runs": 1,
    "dagrun_timeout": timedelta(hours=1),
    "start_date": datetime(2026, 9, 25, tzinfo=local_tz),
    #"end_date":
}

# Variable Declaration
staging_schema = "staging"
core_schema = "core"

# DAG to extract raw data and produce json
with DAG(
    dag_id='produce_json',
    default_args=default_args,
    description='DAG to produce JSON file with RAW data',
    schedule='0 10 * * *',
    catchup=False
) as dag_produce:

    # Define tasks
    playlist_id = get_playlist_id()
    video_ids = get_videos_id(playlist_id)
    extract_data = extract_video_data(video_ids)
    save_to_json_task = save_to_json(extract_data)

    trigger_update_db = TriggerDagRunOperator(
        task_id="trigger_update_db",
        trigger_dag_id="update_db",
    )

    # Define dependencies
    playlist_id >> video_ids >> extract_data >> save_to_json_task >> trigger_update_db

# DAG for data load in both staging and core schema
with DAG(
    dag_id='update_db',
    default_args=default_args,
    description='DAG to process JSON file and insert into both staging and core schema',
    schedule=None,
    catchup=False
) as dag_update_db:

    # Define tasks
    update_staging = staging_table()
    update_core =core_table()

    trigger_data_quality = TriggerDagRunOperator(
        task_id="trigger_data_quality",
        trigger_dag_id ="data_quality",
    )

    # Define dependencies
    update_staging >> update_core >> trigger_data_quality

# DAG for data quality
with DAG(
    dag_id='data_quality',
    default_args=default_args,
    description='DAG to check data quality on both layers in the db',
    schedule=None,
    catchup=False
) as dag_data_quality:

    # Define tasks
    soda_validate_staging = yt_elt_data_quality(staging_schema)
    soda_validate_core =yt_elt_data_quality(core_schema)

    # Define dependencies
    soda_validate_staging >> soda_validate_core