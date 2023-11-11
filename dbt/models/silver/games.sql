{% set GAME_AVG_QRY %}
select ROUND(AVG("WEIGHT"::NUMERIC), 2) from {{ source('bronze', 'GAMES') }}
{% endset %}

{%- set GAME_AVG = dbt_utils.get_single_value(GAME_AVG_QRY) -%}

WITH GAMES AS (
    SELECT
        "ID"::INTEGER AS ID,
        "NAME"::VARCHAR AS NAME,
        "GAME_TYPE"::CHAR AS GAME_TYPE,
        "LUDOPEDIA_URL"::VARCHAR AS LUDOPEDIA_URL,
        "BGG_URL"::VARCHAR AS BGG_URL,
        "MIN_AGE"::INTEGER AS MIN_AGE,
        "PLAYING_TIME"::INTEGER AS PLAYING_TIME_MIN,
        "MIN_PLAYERS"::INTEGER AS MIN_PLAYERS,
        "MAX_PLAYERS"::INTEGER AS MAX_PLAYERS,
        TO_DATE("LST_DT_PLAYED", '%dd%mm%YY') AS LST_DT_PLAYED,
        COALESCE("WEIGHT", '{{ GAME_AVG }}')::FLOAT AS WEIGHT,
        "MIN_BEST_PLAYERS"::INTEGER AS MIN_BEST_PLAYERS,
        "MAX_BEST_PLAYERS"::INTEGER AS MAX_BEST_PLAYERS
    FROM {{ source('bronze', 'GAMES') }}
),

FINAL as (
    SELECT 
        G.*,
        (G."playing_time_min" * 2)::INTEGER AS PLAYING_TIME_REAL_MIN,
        (CURRENT_DATE - G."lst_dt_played")::INTEGER AS DAYS_SINCE_LST_PLAYED,
        ((G."min_best_players" + G."max_best_players")/2)::INTEGER AS BEST_PLAYERS_QTY
    FROM GAMES G
)

SELECT * FROM FINAL