[![](https://img.shields.io/static/v1?label=python&message=3.11&color=blue&logo=python)](https://www.python.org/downloads/release/python-3110/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# STATS FOR THE CLUBE DO BOARDGAME DA ZOEIRA

This repo is intended to collect and analyze data about the game sessions realized into the Clube do Boardgame da Zoeira. The project has two main data sources: data manually annotated into the Google Sheets with sessions, games played, scores, and so on, and; the board game metadata scrapped from [Ludopedia](https://ludopedia.com.br) and [BoardGameGeek](https://boardgamegeek.com/). All the raw data is wrangled to convert the data into a structured one to be queried using SQL. Data is stored in a database using PostgreSQL. Finally, DBT is used to filter, aggregate, join, and test the data to create value to be consumed on Power BI. The following figure shows the architecture of the project.

<p align="center" width="100%">
    <img src="https://github.com/guilhermenoronha/stats_bg/assets/2208226/17379177-1311-4b5c-a5b1-a4b4c6cd3d98"> 
</p>

## OBJECTIVES

The main objectives from the data analysis from the sessions is to keep the club more organized. With the data, is possible to create and watch different KPIs to see if the club is healthy. It's possible, for example, to see which games are played most, who host most sessions, which persons attend more of the sessions, and so son. At the moment, the project has the following KPIs:

- TODO   

## HOW TO USE IT?
- TODO

All the tables are saved into a SQLite database to be used later into a DataViz tool or to be queried in any SQL Tool.
