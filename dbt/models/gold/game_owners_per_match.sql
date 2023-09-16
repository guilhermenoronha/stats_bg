with

players as (select * from {{ ref('players') }}),
bg_owners as (select * from {{ ref('bg_owners') }}),
matches as (select * from {{ ref('matches') }}),
games as (select * from {{ ref('games') }}),

final as (
    select 
        p."name", 
        count(distinct m."id")::integer as total_matches, 
        count(distinct bo."game_id")::integer as total_games
    from players p
    left join bg_owners bo on bo."user_id" = p."id"
    join matches m on m."game_id" = bo."game_id"
    left join games g on g."id"  = bo."game_id"
    group by 1
)

select * from final