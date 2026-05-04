WITH 

    PLAYERS AS (SELECT * FROM {{source('bronze', 'PLAYERS')}}),
    
    ATTENDANCES AS (
        SELECT 
            *
            FROM (
                SELECT
                    *,
                    ROW_NUMBER() OVER(PARTITION BY PLAYER_ID ORDER BY DATE DESC) as rn
                FROM {{ ref("attendances") }}
            )
            WHERE rn = 1
    ),

FINAL AS(
    SELECT
        p."NAME"::VARCHAR AS NAME,
        p."LUDOPEDIA_NICKNAME"::VARCHAR AS LUDOPEDIA_NICKNAME,
        p."MEMBERSHIP"::CHAR AS MEMBERSHIP,
        p."ID"::INTEGER AS ID,
        a."date"::DATE AS LAST_ATTENDED_DATE
    FROM PLAYERS p
    LEFT JOIN ATTENDANCES a on p."ID" = a.player_id
)

SELECT * FROM FINAL