WITH 

MATCHES AS (SELECT * FROM {{ source('bronze', 'MATCHES') }}),
GAMES AS (SELECT * FROM {{ source('bronze', 'GAMES') }}),

STEP_0 AS (
    SELECT
        TO_DATE(M."DATE", '%dd%mm%YY') AS DATE,
        M."PLAYER_ID"::INTEGER AS PLAYER_ID,
        M."GAME_ID"::INTEGER AS GAME_ID,
        M."SCORE"::INTEGER AS SCORE,
        M."ID"::INTEGER AS ID,
        G."NAME"::VARCHAR AS GAME_NAME
    FROM MATCHES M
    LEFT JOIN GAMES G ON G."ID" = M."GAME_ID"
),

FINAL AS (
    SELECT 
        S.*,
        (rank() over (partition by id order by score desc))::INTEGER AS RANK
    FROM STEP_0 S
)

SELECT * FROM FINAL