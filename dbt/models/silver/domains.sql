WITH DOMAINS AS (
    SELECT
        "ID"::INTEGER AS ID,
        "NAME"::VARCHAR AS NAME,
        "URL"::VARCHAR AS URL
    FROM {{ source('bronze', 'DOMAINS') }}        
)

SELECT * FROM DOMAINS