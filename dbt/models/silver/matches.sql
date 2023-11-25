{% set GAME_AVG_QRY %}
select ROUND(AVG("WEIGHT"::NUMERIC), 2) from {{ source('bronze', 'GAMES') }}
{% endset %}

{%- set GAME_AVG = dbt_utils.get_single_value(GAME_AVG_QRY) -%}

WITH 

MATCHES AS (SELECT * FROM {{ source('bronze', 'MATCHES') }}),
GAMES AS (SELECT * FROM {{ ref('games') }}),

STEP_0 AS (
    SELECT
        TO_DATE(M."DATE", '%dd%mm%YY') AS DATE,
        M."PLAYER_ID"::INTEGER AS PLAYER_ID,
        M."GAME_ID"::INTEGER AS GAME_ID,
        M."SCORE"::INTEGER AS SCORE,
        M."ID"::INTEGER AS ID,
        G."name"::VARCHAR AS GAME_NAME,
        G."weight"::FLOAT AS GAME_WEIGHT,
        G."playing_time_real_min"::INTEGER AS GAME_PLAYING_TIME_REAL_MIN
    FROM MATCHES M
    LEFT JOIN GAMES G ON G."id" = M."GAME_ID"
),

STEP_1 AS (
    SELECT 
        S.*,
        (rank() over (partition by id order by score desc))::INTEGER AS RANK
    FROM STEP_0 S
),

FINAL AS (
    SELECT
        S1.*,
        case when rank = max(rank) over(partition by id) then 0
        when rank = min(rank) over(partition by id) then 1 * game_weight
        else
            (1 - (rank/(max(rank) over(partition by id))::float)) * game_weight
        end as WEIGHTED_RANK
    FROM STEP_1 S1
)

SELECT * FROM FINAL