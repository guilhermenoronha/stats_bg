WITH 

PLAYERS AS (SELECT * FROM {{ ref('players') }} ORDER BY name),
ATTENDANCES AS (SELECT * FROM {{ ref('attendances') }}),

NAMES_GROUPED AS(
	SELECT 
        STRING_AGG(P."name", ', ')::VARCHAR AS GROUP_NAME, 
        A."date"::DATE
	FROM PLAYERS P
	LEFT JOIN ATTENDANCES A ON P."id" = A."player_id"
	GROUP BY A."date"
)

SELECT * FROM NAMES_GROUPED