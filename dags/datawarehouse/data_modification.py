import logging

logger = logging.getLogger(__name__)
table = "yt_api"

def insert_rows(cur,conn,schema,row):

    try:

        if schema == 'staging':

            video_id = 'video_id'

            cur.execute(
                f"""INSERT INTO {schema}.{table}("Video_ID","Video_Title","Upload_Date","Duration","Video_Views","Likes_Count","Comments_Count")
                VALUES (%(video_id)s,%(title)s,%(publishedAt)s,%(duration)s,%(viewCount)s,%(likeCount)s,%(commentCount)s);
                """,row
            )
        else:
            video_id = 'Video_ID'

            # Core table has "video_type" which makes it different from the stating table
            cur.execute(
                f"""INSERT INTO {schema}.{table}("Video_ID","Video_Title","Upload_Date","Duration","Video_Type","Video_Views","Likes_Count","Comments_Count")
                VALUES ((%(Video_ID)s,%(Video_Title)s,%(Upload_Date)s,%(Duration)s,%(Video_Type)s,%(Video_Views)s,%(Likes_Count)s,%(Likes_Count)s);)
                """,row
            )

        conn.commit()

        logger.info(f"Inserted row with Video_ID: {row[video_id]}")

    except Exception as e:
        logger.error(f"Error inserting row with video_ID: {row[video_id]}")


# Func update to update data in "staging" schema from row data in json then update "Core" schema from "staging schema"

def update_rows(cur,conn,schema,row):

    try:
        #staging:
        if schema == "staging":
            Video_ID = "video_id"
            Upload_Date = "publishedAt"
            Video_Title = "title"
            Video_Views = "viewCount"
            Likes_Count = "likeCount"
            Comments_Count = "commentCount"
        #Core    
        else:
            Video_ID = "Video_ID"
            Upload_Date = "Upload_Date"
            Video_Title = "title"
            Video_Views = "Video_Title"
            Likes_Count = "Likes_Count"
            Comments_Count = "Comments_Count"

        cur.execute(
            f"""UPDATE {schema}.{table} 
            SET "Video_Title" = %({Video_Title})s,
                "Video_Views" = %({Video_Views})s,
                "Likes_Count" = %({Likes_Count})s,
                "Comments_Count" = %({Comments_Count})s
            WHERE "Video_ID = %({Video_ID})s AND "Upload_Date" = %({Upload_Date})s;
            """,
            row
        )

        conn.commit()

        logger.info(f"Updated row with Video_ID: {row[Video_ID]}")

    except Exception as e:
        logger.error(f"Error updateing row vith Video_ID: {row[Video_ID]} - {e}")
        raise


# func delete
def delete_rows(cur,conn,schema,ids_to_delete):

    try:

        ids_to_delete = f"""({', '.join(f"'{id}'" for id in ids_to_delete)})"""

        cur.execute(
            f"""DELETE FROM {schema}.{table} 
            WHERE "Video_ID" IN {ids_to_delete};
            """
        )

        conn.commit()
        logger.info(f"Deleted rows with Video_ID: {ids_to_delete}")

    except Exception as e:
        logger.error(f"Error deleting rows with Video_IDs: {ids_to_delete} - {e}")

    