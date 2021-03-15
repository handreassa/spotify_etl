# Spotify Data ETL

**Intent**: Get data from Spotify through their public API and load the data into a sqlite database

- Steps on the project: reach the Spotify's "Recent played Tracks endpoint" and download data in JSON format, check if there are any errors before populating into an sqlite table. The table is composed by the following information (my last songs played for reference):

| songname      | artist_name | played_at | timestamp |
| ----------- | ----------- | ---: | ---: |
| Jump - 2015 Remaster |	Van Halen |	2021-03-14T22:44:49.770Z	| 2021-03-14 | 
| Sultans Of Swing	| Dire Straits	|2021-03-14T18:20:21.091Z	2021-03-14 |
| Hotel California - 2013 Remaster	| Eagles	| 2021-03-14T18:18:52.381Z	| 2021-03-14 |
| Smoke On The Water - Remastered 2012 |	Deep Purple	| 2021-03-14T18:12:20.720Z | 2021-03-14 |


#Project reference links:
* Implementation guided from [Karolina Sowinska's Youtube Channel](https://www.youtube.com/channel/UCAxnMry1lETl47xQWABvH7g)
 * Spotify API - reference page - [Spotify console](https://developer.spotify.com/console/)
 * Troubleshooting - installing Airflow on Windows 10 (WSL) -  [Medium](https://medium.com/@ryanroline/installing-apache-airflow-on-windows-10-5247aa1249ef)

#Notes about the configuration:
* Some configuration was left, and need to be solved either in main.py (replacing the env variables) or in .env file (removed in this repository):

The main.py code has the following lines that need to be altered:
```python
    DATABASE_LOCATION =  os.getenv('DATABASE_LOCATION')
    USER_ID = os.getenv("USER_ID")
    TOKEN = os.getenv("TOKEN")
```

