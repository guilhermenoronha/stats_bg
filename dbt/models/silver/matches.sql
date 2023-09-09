WITH MATCHES AS (
    SELECT
        TO_DATE("DATE", '%dd%mm%YY') AS DATE,
        "PLAYER_ID"::INTEGER AS PLAYER_ID,
        "GAME_ID"::INTEGER AS GAME_ID,
        "SCORE"::INTEGER AS SCORE,
        "ID"::INTEGER AS ID 
    FROM {{ source('bronze', 'MATCHES') }}
)

SELECT * FROM MATCHES