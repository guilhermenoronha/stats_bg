WITH CATEGORIES AS (
    SELECT
        "ID"::INTEGER AS ID,
        "NAME"::VARCHAR AS NAME,
        "URL"::VARCHAR AS URL
    FROM {{ source('bronze', 'CATEGORIES') }}        
)

SELECT * FROM CATEGORIES