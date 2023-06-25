# STATS FOR THE CLUBE DO BOARDGAME DA ZOEIRA

This repo is intended to collect and analyze data about the game sessions realized into the Clube do Boardgame da Zoeira. All the data is manually annotated onto the Google Sheets. Then, the current script does the data wrangling, converting all the data into a structured one to be queried using SQL. 

The current version of this project is: 1.0

## OBJECTIVES

The main objectives from the data analysis from the sessions is to keep the club more organized. With the data, is possible to create and watch different KPIs to see if the club is healthy. It's possible, for example, to see which games are played most, who host most sessions, which persons attend more of the sessions, and so son. At the moment, the project has the following KPIs:

- TODO   

## TABLES
At the moment, the data is distributed into four tables:

- PERSONS: with all players which attended to one or more sessions. This table has the following columns:
    - ID
    - NAME
- GAMES: the list of all games which were played into one or more sessions and its person's owners. This table has the following columns:
    - ID
    - OWNER_ID: the person id who owns the game.
    - NAME
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

# ABOUT THE CLUBE DO BOARDGAME DA ZOEIRA
Founded in 2015, the CLUBE DO BOARDGAME DA ZOEIRA is a club to play board games. It is hosted in Minas Gerais and was founded by the friends Guilherme, Frederico, Cezar, Daniel, Amilton, and Alfredo. As the years passed by, some former members left the club and another members joined. The core idea of the club was to build a board game library. The club implemented a consortium where every member paid a fee every month. The money collected was given to a different member each member who used to buy new board games. As the library grew larger, the consortium was abandoned and the members kept buying games independently.