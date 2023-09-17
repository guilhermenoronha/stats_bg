with

players as (select * from {{ ref('players') }}),
bg_owners as (select * from {{ ref('bg_owners') }}),
matches as (select * from {{ ref('matches') }}),
games as (select * from {{ ref('games') }}),

final as (
    select 
        p."name", 
        m."id" as match_id, 
        g.name as game_name
    from players p
    left join bg_owners bo on bo."user_id" = p."id"
    join matches m on m."game_id" = bo."game_id"
    left join games g on g."id"  = bo."game_id"
)

select * from final