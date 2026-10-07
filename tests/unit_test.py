# test assessment for API
def test_api_key(api_key):
    assert api_key == "MOCK_KEY123456"

# test assessment for channel_handle
def test_channel_handle(channel_handle):
    assert channel_handle == "MRCHEESE"

# test assessment for connection to POSTGRES_DB_YT_ELT
def test_postgres_conn(mock_postgres_conn_vars):
    conn = mock_postgres_conn_vars
    assert conn.login == "mock_username"
    assert conn.password == "mock_password"
    assert conn.host == "mock_host"
    assert conn.port == 1234
    assert conn.schema == "mock_db_name"

# test assessment for 
def test_dags_integrity(dagbag):
    # 1. test no import error
    assert dagbag.import_errors == {}, f"Import errors found: {dagbag.import_errors}"
    print("====================","\n",dagbag.import_errors)

    # 2. test to make sure all the dag are being load
    expected_ids = [
        "produce_json",
        "update_db",
        "data_quality"
    ]
    loaded_dags_ids = list(dagbag.dags.keys())
    print("====================","\n",dagbag.dags.keys())

    for dag_id in expected_ids:
        assert dag_id in loaded_dags_ids, f"DAG {dag_id} is missing."

    # 3. test the number of dags are correct
    assert dagbag.size() == len(expected_ids)
    print("===================","\n",f"Airflow has {dagbag.size()} DAGs")

    # 4. test each dags has the number of tasks expected
    expected_task_counts = {
        "produce_json": 4,
        "update_db": 2,
        "data_quality": 2,
    }
    print("=====================")
    for dag_id, dag in dagbag.dags.items():
        expected_count = expected_task_counts[dag_id]
        actual_count = len(dag.tasks)
        assert (
            expected_count == actual_count
            ), f"DAG {dag_id} has {actual_count} tasks, expected is {expected_count}."
        print(f"GAD ID of {dag_id} has {len(dag.tasks)} tasks")
        


