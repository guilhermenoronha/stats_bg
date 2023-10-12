WITH
 games AS (SELECT * FROM {{ ref('games') }}),
 bg_owners AS (SELECT * FROM {{ ref('bg_owners') }}),
 players AS (SELECT * FROM {{ ref('players') }}),

 final AS (
    SELECT
        p.name AS player, 
        g.name as game
        from games g 
        left join bg_owners bo on g.id = bo.game_id
        left join players p on p.id = bo.user_id
 )

 SELECT * FROM final