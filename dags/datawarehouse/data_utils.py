# import airflow postgres hook for connection to postgres
from airflow.providers.postgres.hooks.postgres import PostgresHook
# import cursor
from psycopg2.extras import RealDictCursor

table = "yt_api"

# Func to initialize the connection and cursor in postgres
def get_conn_cursor():
    hook = PostgresHook(postgres_conn_id="postgres_db_yt_elt", database="elt_db")
    conn = hook.get_conn()
    # initial cursor to execute sql in postgres
    cur = conn.cursor(cursor_factory=RealDictCursor)
    return conn, cur

# Func to close the cursor then the connection to postgres
def close_conn_cursor(conn,cur):
    cur.close()
    conn.close()

def create_schema(schema):
    conn,cur = get_conn_cursor()

    schema_create_sql = f"CREATE SCHEMA IF NOT EXISTS {schema};"

    cur.execute(schema_create_sql)

    conn.commit()

    close_conn_cursor(conn,cur)

def create_table(schema):
    conn, cur = get_conn_cursor()

    if schema =="staging":
        table_create_sql = f"""
                        CREATE TABLE IF NOT EXISTS {schema}.{table} (
                            "Video_ID" VARCHAR(11) PRIMARY KEY NOT NULL,
                            "Video_Title" TEXT NOT NULL,
                            "Upload_Date" TIMESTAMP NOT NULL,
                            "Duration" VARCHAR(20) NOT NULL,
                            "Video_Views" INT,
                            "Likes_Count" INT,
                            "Comments_Count" INT
                        );
                    """
    else:
        table_create_sql = f"""
                        CREATE TABLE IF NOT EXISTS {schema}.{table} (
                            "Video_ID" VARCHAR(11) PRIMARY KEY NOT NULL,
                            "Video_Title" TEXT NOT NULL,
                            "Upload_Date" TIMESTAMP NOT NULL,
                            "Duration" VARCHAR(20) NOT NULL,
                            "Video_Type" VARCHAR(10) NOT NULL,
                            "Video_Views" INT,
                            "Likes_Count" INT,
                            "Comments_Count" INT
                        );
                    """
    cur.execute(table_create_sql)

    conn.commit()

    close_conn_cursor(conn, cur)

# Func to get only the video ids from the tables (staging and core)
def get_video_ids(cur, schema):

    cur.execute(f"""SELECT "Video_ID" FROM {schema}.{table};""")
    ids = cur.fetchall()

    video_ids = [row["Video_ID"] for row in ids]

    return video_ids

