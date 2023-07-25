[![](https://img.shields.io/static/v1?label=python&message=3.11&color=blue&logo=python)](https://www.python.org/downloads/release/python-3110/)
[![](https://img.shields.io/static/v1?label=version&message=1.4&color=green)](https://img.shields.io/static/v1?label=version&message=1.4&color=green)

# STATS FOR THE CLUBE DO BOARDGAME DA ZOEIRA

This repo is intended to collect and analyze data about the game sessions realized into the Clube do Boardgame da Zoeira. All the data is manually annotated onto the Google Sheets. Then, the current script does the data wrangling, converting all the data into a structured one to be queried using SQL. 

The current version of this project is: 1.3

## WHAT'S NEW?

- 1.1: Bugfixed the attendances table. See [#1](/../../issues/1).
- 1.2: Bugfixed the matches table. See [#2](/../../issues/2)
- 1.3: Implemented new columns. See [#3](/../../issues/3)  
- 1.4: Implemented Ludopedia scrapper. See[#4](/../../issues/4) 

## OBJECTIVES

The main objectives from the data analysis from the sessions is to keep the club more organized. With the data, is possible to create and watch different KPIs to see if the club is healthy. It's possible, for example, to see which games are played most, who host most sessions, which persons attend more of the sessions, and so son. At the moment, the project has the following KPIs:

- TODO   

## TABLES
At the moment, the data is distributed into four tables:

- PERSONS: with all players which attended to one or more sessions. This table has the following columns:
    - ID
    - NAME
    - LAST_DATE_ATTENDED
    - DAYS_SINCE_LAST_ATTENDANCE
- GAMES: the list of all games which were played into one or more sessions and its person's owners. This table has the following columns:
    - ID
    - OWNER_ID: the person id who owns the game.
    - NAME
    - LAST_DATE_PLAYED
    - DAYS_SINCE_LAST_PLAY
- ATTENDANCES: the list of every session registered. The attendances' table have the date, who was the host and the persons IDs. This table has the following columns:
    - DATE
    - IS_HOST: true or false
    - PERSON_ID 
- MATCHES: the list of every game that was played in every session. This table has the following columns:
    - ID
    - DATE
    - PERSON_ID
    - GAME_ID
    - SCORE

All the tables are saved into a SQLite database to be used later into a DataViz tool or to be queried in any SQL Tool.