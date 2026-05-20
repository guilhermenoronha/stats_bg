{% set GAME_AVG_QRY %}
select round(avg("weight"::numeric), 2) from {{ ref('games') }}
{% endset %}

{% set GAME_TIME_AVG_QRY %}
select 
    to_char(
        avg("playing_time_real_hr"),
        'HH24:MI:SS'
    )
from {{ ref('games') }}
{% endset %}

{%- set GAME_AVG = dbt_utils.get_single_value(GAME_AVG_QRY) -%}
{%- set GAME_TIME_AVG = dbt_utils.get_single_value(GAME_TIME_AVG_QRY) -%}


with 

matches as (select * from {{ source('bronze', 'MATCHES') }}),
games as (select * from {{ ref('games') }}),
players as (select * from {{source('bronze', 'PLAYERS')}}),

final as (
    select
        to_date(m."date", '%yyyy%mm%dd') as date,
        m."host_name"::varchar as host_name,
        m."match_id"::integer as match_id,
        m."game_name"::varchar as game_name,
        m."game_owner"::varchar as game_owner,
        m."player_name"::varchar as player_name,
        m."score"::float as score,
        m."rank"::integer as rank,
        m."notes"::varchar as notes,
        p."ID"::integer as player_id,
        p2."ID"::integer as game_owner_id,
        coalesce(p."MEMBERSHIP", 'G')::varchar as player_membership,
        round(
            cast(
                case 
                    when rank = max(rank) over(partition by match_id) then 0
                    when rank = min(rank) over(partition by match_id) then 1 * coalesce(g."weight", {{ GAME_AVG }})
                    else (1 - (rank/(max(rank) over(partition by match_id))::float)) * coalesce(g."weight", {{ GAME_AVG }})
                end 
                as numeric
            )
            , 2
        ) as weighted_rank,
        coalesce(g."playing_time_real_hr"::interval, '{{ GAME_TIME_AVG }}'::interval) as game_playing_time_real_hr,
        g."id"::integer as game_id
    from matches m
    left join players p on m."player_name" = p."NAME"
    left join players p2 on m."game_owner" = p2."NAME"
    left join games g on g."name" = m."game_name"
)

select * from final
where game_name is not null