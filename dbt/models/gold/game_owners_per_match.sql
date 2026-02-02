with

players as (select * from {{ ref('players') }}),
bg_owners as (select * from {{ ref('bg_owners') }}),
matches as (select * from {{ ref('matches') }}),
games as (select * from {{ ref('games') }}),

final as (
    select distinct
        p."name", 
        m."id" as match_id,
        m."date",
        g.name as game_name,
        dense_rank() over(partition by game_name, EXTRACT(YEAR FROM date) order by date, m."id") as dr
    from players p
    left join bg_owners bo on bo."user_id" = p."id"
    join matches m on m."game_id" = bo."game_id"
    left join games g on g."id"  = bo."game_id"
)

select 
  name, 
  match_id,
  game_name, 
  1/cast(dr as float) as sommelier_rank 
from final