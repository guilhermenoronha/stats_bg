with
    mechanics as (select * from {{ ref('mechanics') }}),
    bg_mechanics as (select * from {{ ref('bg_mechanics') }}),
    games as (select * from {{ ref('games') }}),

final AS (
    select distinct
        m."name" as mechanic,
        g."name" as game
    from mechanics m 
    left join bg_mechanics bm on m.id = bm.mechanic_id 
    left join games g on bm.game_id = g.id
    where g.game_type = 'B'    
)

select * from final