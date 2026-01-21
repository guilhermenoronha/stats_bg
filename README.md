[![](https://img.shields.io/static/v1?label=python&message=3.11&color=blue&logo=python)](https://www.python.org/downloads/release/python-3110/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# STATS FOR THE CLUBE DO BOARDGAME DA ZOEIRA

This repo is intended to collect and analyze data about the game sessions realized into the Clube do Boardgame da Zoeira. The project has two main data sources: data manually annotated into the Google Sheets with sessions, games played, scores, and so on, and; the board game metadata scrapped from [Ludopedia](https://ludopedia.com.br) and [BoardGameGeek](https://boardgamegeek.com/). All the raw data is wrangled to convert the data into a structured one to be queried using SQL. Data is stored in a database using PostgreSQL. Finally, DBT is used to filter, aggregate, join, and test the data to create value to be consumed on Looker Studio. The following figure shows the architecture of the project.

<p align="center" width="100%">
    <img src="https://github.com/user-attachments/assets/50d2498d-85d5-4df4-b592-3ae7d9faf679"> 
</p>

## OBJECTIVES

The main objectives from the data analysis from the sessions is to keep the club more organized. With the data, is possible to create and watch different KPIs to see if the club is healthy. It's possible, for example, to see which games are played most, who host most sessions, which persons attend more of the sessions, and so son. At the moment, the project has the following KPIs:

- TODO   

## HOW TO USE IT?

### Prerequistes
- Have an account on Ludopedia and create and New App on https://ludopedia.com.br/aplicativos to get the access_key.
- Have PostgreSQL installed locally.

### Basic usage
- Clone this repo
- Create a database named stats_bg, and a schema named bronze.
- Create .env file with the following variables:
    - PG_USER=your_postgres_username
    - PG_PASSWD=your_postgres_password
    - HOST=postgres_host
    - PORT=postgres_port
    - DB=postgres_database
    - SCHEMA=bronze
    - SHEET_ID=your_google_sheet_id
    - ACCESS_KEY=your_ludopedia_acess_token(usuário)
- Open a terminal a type _poetry init_ to create a virtual env.
- Yet on terminal, type _python main.py_ (Also you may use the arg --mode with the following options):
    - players: process players table.
    - taxonomy: process themes, categories, domains, and mechanics tables.
    - boardgames: process games and bg_owners table.
    - metadata: process bg_domains, bg_themes, bg_categories, and bg_mechanics tables.
    - matches: process attendances and matches table.
- Export the following variables to the system to be used by DBT:
    - SET POSTGRES_USER=your_user
    - SET POSTGRES_PASSWD=your_password
    - SET POSTGRES_HOST=your_host
- run _cd dbt_ command
- run _dbt deps_ to install DBT dependencies.
- run _dbt build_ command to build all models.
