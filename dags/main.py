from airflow import DAG
import pendulum
from datetime import datetime, timedelta
from api.video_stats import get_playlist_id, get_videos_id, extract_video_data, save_to_json

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

with DAG(
    dag_id='produce_json',
    default_args=default_args,
    description='DAG to produce JSON file with RAW data',
    schedule='0 10 * * *',
    catchup=False
) as dag:

    # Define tasks
    playlist_id = get_playlist_id()
    video_ids = get_videos_id(playlist_id)
    extract_data = extract_video_data(video_ids)
    save_to_json_task = save_to_json(extract_data)

    # Define dependencies
    playlist_id >> video_ids >> extract_data >> save_to_json_task

