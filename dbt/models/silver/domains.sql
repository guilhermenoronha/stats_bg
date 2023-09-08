WITH DOMAINS AS (
    SELECT
        CAST("ID" AS INTEGER) AS ID,
        CAST("NAME" AS VARCHAR) AS NAME,
        CAST("URL" AS VARCHAR) AS URL
    FROM {{ source('bronze', 'DOMAINS') }}        
)

SELECT * FROM DOMAINS