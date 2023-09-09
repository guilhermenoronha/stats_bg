WITH THEMES AS (
    SELECT
        "ID"::INTEGER AS ID,
        "NAME"::VARCHAR AS NAME,
        "URL"::VARCHAR AS URL
    FROM {{ source('bronze', 'THEMES') }}        
)

SELECT * FROM THEMES