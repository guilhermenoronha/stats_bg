with

players as (select * from {{ ref('players') }}),
matches as (select * from {{ ref('matches') }}),

final as (
    select
        p.name,
        m.game_name,
        m.date
    from players p
    left join matches m on p.id = m.player_id
)

select * from final