WITH MECHANICS AS (
    SELECT
        "ID"::INTEGER AS ID,
        "NAME"::VARCHAR AS NAME,
        "URL"::VARCHAR AS URL
    FROM {{ source('bronze', 'MECHANICS') }}        
)

SELECT * FROM MECHANICS