import sqlalchemy
import requests
import pandas as pd
import json
import datetime
import sqlite3
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
import os

DATABASE_LOCATION = os.getenv("DATABASE_LOCATION")
USER_ID = os.getenv("USER_ID")
TOKEN = os.getenv("TOKEN")


def check_data(df: pd.DataFrame) -> bool:
    # to validate wheter the return is empty
    if df.empty:
        print("INFO: No songs downloaded. Finishing execution")
        return False
    # validate duplicates
    if pd.Series(df["played_at"]).is_unique:
        pass
    else:
        raise Exception("ERROR: Primary key violation.")

    # check for nulls
    if df.isnull().values.any():
        raise Exception("ERROR: Nulls values found.")

    # Check if there are another dates in the json:
    # yesterday = datetime.now() - timedelta(days=1)
    # yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    # # print("Yesterday: ", yesterday)
    # timestamps = df['timestamp'].tolist()
    # for timestamp in timestamps:
    #     if datetime.strptime(timestamp, "%Y-%m-%d") < yesterday:
    #         print('Timestamp:', timestamp)
    #         raise Exception("ERROR: At least one of the returned songs are not from the last 24 hours")

    return True


if __name__ == "__main__":

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token=TOKEN),
    }

    today = datetime.now()
    yesterday = today - timedelta(days=2)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    # r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp), headers=headers)
    r = requests.get(
        "https://api.spotify.com/v1/me/player/recently-played?after={time}".format(
            time=yesterday_unix_timestamp
        ),
        headers=headers,
    )

    data = r.json()

    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])

    song_dict = {
        "song_name": song_names,
        "artist_name": artist_names,
        "played_at": played_at_list,
        "timestamp": timestamps,
    }

    song_df = pd.DataFrame(
        song_dict, columns=["song_name", "artist_name", "played_at", "timestamp"]
    )

    if check_data(song_df):
        print("INFO: Downloaded data is valid, proceed to the Load steps")

    database_engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect("my_tracks.sqlite")
    cursor = conn.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS my_tracks(
        song_name VARCHAR(200),
        artist_name VARCHAR(200),
        played_at VARCHAR(200),
        timestamp VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)

    )"""
    cursor.execute(query)
    print("INFO: Opened database succesfully.")

    try:
        song_df.to_sql("my_tracks", database_engine, index=False, if_exists="append")
    except:
        print("INFO: Data already exists in the database.")

    conn.close()
    print("INFO: Close database successfully.")
